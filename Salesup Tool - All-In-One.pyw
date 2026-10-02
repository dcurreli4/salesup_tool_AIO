"""
Salesup Tool - All-In-One.pyw  —  DevOps Tool - All-in-one
Doppio clic per avviare su Windows (nessuna console).
"""

import importlib
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json
from base64 import b64encode
from pathlib import Path

VERSION = "1.0.0"

# Repository GitHub ("owner/repo") da cui leggere le release; vuoto = nessun controllo
_UPDATE_REPO = "dcurreli4/salesup_tool_AIO"

_REQUIRED = {"requests": "requests"}

# ── Splash screen ─────────────────────────────────────────────────────────────

class _Splash:

    def __init__(self):
        self._root = tk.Tk()
        self._root.overrideredirect(True)
        self._root.configure(bg="#0f1117")
        self._root.attributes("-topmost", True)
        W, H = 380, 200
        x = (self._root.winfo_screenwidth()  - W) // 2
        y = (self._root.winfo_screenheight() - H) // 2
        self._root.geometry(f"{W}x{H}+{x}+{y}")

        outer = tk.Frame(self._root, bg="#2a2d3e", bd=1)
        outer.pack(fill="both", expand=True, padx=1, pady=1)
        inner = tk.Frame(outer, bg="#0f1117")
        inner.pack(fill="both", expand=True, padx=1, pady=1)

        logo = tk.Frame(inner, bg="#0f1117")
        logo.pack(pady=(28, 8))
        tk.Label(logo, text="DevOps", font=("Consolas", 14, "bold"),
                 fg="#4f8ef7", bg="#0f1117").pack(side="left")
        tk.Label(logo, text="|", font=("Consolas", 14),
                 fg="#2a2d3e", bg="#0f1117", padx=2).pack(side="left")
        tk.Label(logo, text="AIO", font=("Consolas", 14, "bold"),
                 fg="#f0f2ff", bg="#0f1117").pack(side="left")

        tk.Frame(inner, bg="#2a2d3e", height=1).pack(fill="x", padx=24, pady=(8, 0))

        bar_bg = tk.Frame(inner, bg="#1a1d27", height=4)
        bar_bg.pack(fill="x", padx=24, pady=(10, 0))
        bar_bg.pack_propagate(False)
        self._bar = tk.Canvas(bar_bg, bg="#1a1d27", height=4,
                              highlightthickness=0, bd=0)
        self._bar.pack(fill="both", expand=True)
        self._bar_fill = self._bar.create_rectangle(0, 0, 0, 4, fill="#4f8ef7", outline="")

        self._msg_var = tk.StringVar(value="Avvio in corso...")
        tk.Label(inner, textvariable=self._msg_var, bg="#0f1117", fg="#8892b0",
                 font=("Consolas", 9), pady=8).pack()

        tk.Label(inner, text=f"v{VERSION}", bg="#0f1117", fg="#2a2d3e",
                 font=("Consolas", 8)).pack(side="bottom", pady=8)

        self._root.update()

    def set(self, msg: str):
        self._msg_var.set(msg)
        self._root.update()

    def progress(self, value: float):
        value = max(0.0, min(1.0, value))
        self._root.update_idletasks()
        w = self._bar.winfo_width()
        self._bar.coords(self._bar_fill, 0, 0, int(w * value), 4)
        self._root.update()

    def destroy(self):
        self._root.destroy()


_splash = _Splash()

# ── Auto-install dipendenze ──────────────────────────────────────────────────

def _ensure_dependencies():
    steps = len(_REQUIRED) + 2
    missing = []
    for i, (module, package) in enumerate(_REQUIRED.items(), 1):
        _splash.set(f"Verifica {module}...")
        _splash.progress(i / steps)
        try:
            importlib.import_module(module)
        except ImportError:
            missing.append(package)

    failed = []
    for i, package in enumerate(missing, 1):
        _splash.set(f"Installazione {package} ({i}/{len(missing)})...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package],
            capture_output=True, text=True,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        if result.returncode != 0:
            failed.append(package)

    if failed:
        _splash.set(f"✗ Installazione fallita: {', '.join(failed)}")
        messagebox.showerror(
            "Errore installazione",
            "Impossibile installare:\n\n  • " + "\n  • ".join(failed) +
            f"\n\nEsegui manualmente:\n  pip install {' '.join(failed)}"
        )
        sys.exit(1)
    importlib.invalidate_caches()

_ensure_dependencies()
import requests

# ── Controllo aggiornamenti ──────────────────────────────────────────────────
_UPDATE_INFO = None  # (latest_version, download_url) oppure None

def _vtuple(v):
    try:
        return tuple(int(x) for x in v.split("."))
    except ValueError:
        return (0,)

def _check_update_available():
    global _UPDATE_INFO
    if not _UPDATE_REPO:
        return
    try:
        resp = requests.get(
            f"https://api.github.com/repos/{_UPDATE_REPO}/releases/latest", timeout=5)
        if resp.status_code != 200:
            return
        data = resp.json()
        latest = data.get("tag_name", "").lstrip("v")
        if not latest or _vtuple(latest) <= _vtuple(VERSION):
            return
        url = next((a["browser_download_url"] for a in data.get("assets", [])
                    if a["name"].endswith(".pyw")), None)
        if url:
            _UPDATE_INFO = (latest, url)
    except Exception:
        pass

_splash.set("Controllo aggiornamenti...")
_splash.progress((len(_REQUIRED) + 1) / (len(_REQUIRED) + 2))
_check_update_available()

_splash.set("Caricamento interfaccia...")
_splash.progress(1.0)

# ── Palette colori (identica a HUB Tool) ────────────────────────────────────
BG        = "#0f1117"
BG_CARD   = "#1a1d27"
BG_CARD2  = "#141720"
BG_HOVER  = "#22263a"
BG_INPUT  = "#0d1020"
ACCENT    = "#4f8ef7"
SUCCESS   = "#22c55e"
WARNING   = "#f59e0b"
ERROR_C   = "#ef4444"
TEXT_PRI  = "#f0f2ff"
TEXT_SEC  = "#8892b0"
BORDER    = "#2a2d3e"

_SB_BG       = "#0d1020"
_SB_BG_SEL   = "#1a1d27"
_SB_ITEM_BG  = "#131628"
_SB_ACCENT   = "#4f8ef7"
_SB_ACCENT2  = "#7c3aed"
_SB_TEXT     = "#8892b0"
_SB_TEXT_SEL = "#f0f2ff"
_SB_BORDER   = "#2a2d3e"

FONT_MONO = ("Consolas", 9)
FONT_MONO_BOLD = ("Consolas", 9, "bold")
FONT_MONO_LG = ("Consolas", 11, "bold")
FONT_MONO_SM = ("Consolas", 8)

# ── Configurazione (.env) ─────────────────────────────────────────────────────
_ENV = Path(__file__).parent / "config" / ".env"

_DEFAULT_ORG_URL = "https://dev.azure.com/DevOps-Applications-EGL"

def _azdo_test_connection(values: dict) -> tuple:
    """Ritorna (ok, messaggio) provando a leggere i progetti dell'organizzazione."""
    org = values.get("DEVOPS_ORG_URL", "").strip().rstrip("/")
    pat = values.get("DEVOPS_PAT", "").strip()
    if not org or not pat:
        return False, "Inserisci URL e PAT"
    token = b64encode(f":{pat}".encode()).decode()
    try:
        resp = requests.get(f"{org}/_apis/projects?api-version=7.1",
                            headers={"Authorization": f"Basic {token}"},
                            timeout=15, verify=False)
    except requests.exceptions.ConnectionError:
        return False, "Server non raggiungibile — controlla URL e rete"
    except requests.exceptions.Timeout:
        return False, "Timeout — il server non risponde"
    # Con PAT errato Azure DevOps può rispondere 203 con la pagina di login HTML
    if resp.status_code in (401, 203) or "json" not in resp.headers.get("Content-Type", ""):
        return False, "PAT non valido o scaduto"
    if not resp.ok:
        return False, f"Errore HTTP {resp.status_code}"
    n = len(resp.json().get("value", []))
    return True, f"Connesso — {n} progetto/i trovato/i"


# (titolo tab, [(titolo sezione, [(chiave, etichetta, is_password)], validatore)])
# Con validatore: niente autosave, i dati si salvano solo se il validatore va a buon fine
SETTINGS_TABS = [
    ("⎇  Branches", [
        ("Azure DevOps", [
            ("DEVOPS_ORG_URL", "Organization URL",      False),
            ("DEVOPS_PAT",     "Personal Access Token", True),
        ], _azdo_test_connection),
    ]),
]


def _read_env_raw() -> dict:
    result = {}
    if not _ENV.exists():
        return result
    for line in _ENV.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        result[k.strip()] = v.strip().strip('"').strip("'")
    return result


def _write_env(data: dict):
    original = _ENV.read_text(encoding="utf-8").splitlines() if _ENV.exists() else []
    updated, new_lines = set(), []
    for line in original:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            k = stripped.partition("=")[0].strip()
            if k in data:
                new_lines.append(f"{k}={data[k]}")
                updated.add(k)
                continue
        new_lines.append(line)
    for k, v in data.items():
        if k not in updated:
            new_lines.append(f"{k}={v}")
    _ENV.parent.mkdir(parents=True, exist_ok=True)
    _ENV.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def _get_org_url() -> str:
    return (_read_env_raw().get("DEVOPS_ORG_URL") or _DEFAULT_ORG_URL).strip().rstrip("/")

# ── Scrollbar style ───────────────────────────────────────────────────────────
def _setup_scrollbar_style():
    s = ttk.Style()
    s.theme_use("clam")
    for name in ("Dark.Vertical.TScrollbar", "Dark.Horizontal.TScrollbar"):
        s.configure(name,
                    background=BORDER, troughcolor=BG_CARD,
                    arrowcolor=TEXT_SEC, bordercolor=BG_CARD,
                    darkcolor=BG_CARD, lightcolor=BG_CARD,
                    relief="flat", arrowsize=12)
        s.map(name, background=[("active", TEXT_SEC), ("pressed", ACCENT)])


# ════════════════════════════════════════════════════════════════════════════
# PANNELLO BRANCHES
# ════════════════════════════════════════════════════════════════════════════

class BranchesPanel(tk.Frame):

    def __init__(self, master):
        super().__init__(master, bg=BG)
        self._all_data   = []   # lista di dict {repo, branches:[{name, is_default}]}
        self._projects   = []
        self._org        = ""
        self._pat        = ""
        self._status_var = tk.StringVar()
        self._build()

    # ── Layout ───────────────────────────────────────────────────────────────

    def _build(self):
        # ── Card connessione (URL e PAT si configurano in Impostazioni) ──────
        cfg = tk.Frame(self, bg=BG_CARD, bd=0,
                       highlightthickness=1, highlightbackground=BORDER)
        cfg.pack(fill="x", padx=20, pady=(20, 0))

        tk.Label(cfg, text="Connessione", bg=BG_CARD, fg=ACCENT,
                 font=FONT_MONO_BOLD, pady=10, padx=16, anchor="w").pack(fill="x")
        tk.Frame(cfg, bg=BORDER, height=1).pack(fill="x", padx=16)

        btn_row = tk.Frame(cfg, bg=BG_CARD)
        btn_row.pack(fill="x", padx=16, pady=12)

        self._connect_btn = tk.Button(
            btn_row, text="⟳  Connetti", command=self._on_connect,
            bg=ACCENT, fg="#ffffff", font=FONT_MONO_BOLD,
            relief="flat", padx=14, pady=5, cursor="hand2",
            activebackground=ACCENT, activeforeground="#ffffff"
        )
        self._connect_btn.pack(side="left")

        self._status_lbl = tk.Label(btn_row, textvariable=self._status_var,
                                    bg=BG_CARD, fg=TEXT_SEC, font=FONT_MONO)
        self._status_lbl.pack(side="left", padx=(12, 0))

        # ── Progetto selector (nascosto inizialmente) ─────────────────────
        self._proj_frame = tk.Frame(self, bg=BG_CARD, bd=0,
                                    highlightthickness=1, highlightbackground=BORDER)

        tk.Label(self._proj_frame, text="Progetto", bg=BG_CARD, fg=ACCENT,
                 font=FONT_MONO_BOLD, pady=10, padx=16, anchor="w").pack(fill="x")
        tk.Frame(self._proj_frame, bg=BORDER, height=1).pack(fill="x", padx=16)

        prow = tk.Frame(self._proj_frame, bg=BG_CARD)
        prow.pack(fill="x", padx=16, pady=10)
        prow.columnconfigure(0, weight=1)

        self._proj_var = tk.StringVar()
        self._proj_combo = ttk.Combobox(prow, textvariable=self._proj_var,
                                        state="readonly", font=FONT_MONO)
        self._proj_combo.grid(row=0, column=0, sticky="ew")

        self._load_btn = tk.Button(
            prow, text="⟳  Carica branch", command=self._on_load_branches,
            bg=BG_CARD2, fg=ACCENT, font=FONT_MONO_BOLD,
            relief="flat", padx=12, pady=5, cursor="hand2",
            activebackground=BG_HOVER, activeforeground=TEXT_PRI
        )
        self._load_btn.grid(row=0, column=1, padx=(10, 0))

        # ── Toolbar ricerca/filtro (nascosta inizialmente) ────────────────
        self._toolbar = tk.Frame(self, bg=BG)

        tk.Label(self._toolbar, text="🔍", bg=BG, fg=TEXT_SEC,
                 font=("Consolas", 12)).pack(side="left", padx=(20, 4))

        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._render())
        search_entry = tk.Entry(self._toolbar, textvariable=self._search_var,
                                bg=BG_INPUT, fg=TEXT_PRI,
                                insertbackground=TEXT_PRI,
                                relief="flat", font=FONT_MONO,
                                highlightthickness=1,
                                highlightbackground=BORDER,
                                highlightcolor=ACCENT)
        search_entry.pack(side="left", fill="x", expand=True, padx=(0, 8), ipady=4)

        tk.Label(self._toolbar, text="Repository:", bg=BG, fg=TEXT_SEC,
                 font=FONT_MONO).pack(side="left")
        self._repo_var = tk.StringVar(value="Tutti")
        self._repo_combo = ttk.Combobox(self._toolbar, textvariable=self._repo_var,
                                         state="readonly", font=FONT_MONO, width=24)
        self._repo_combo.bind("<<ComboboxSelected>>", lambda *_: self._render())
        self._repo_combo.pack(side="left", padx=(4, 20))

        # ── Scrollable area risultati ─────────────────────────────────────
        self._results_host = tk.Frame(self, bg=BG)
        self._results_canvas = tk.Canvas(self._results_host, bg=BG,
                                         highlightthickness=0)
        vsb = ttk.Scrollbar(self._results_host, orient="vertical",
                             command=self._results_canvas.yview,
                             style="Dark.Vertical.TScrollbar")

        def _scroll_set(first, last):
            if float(first) <= 0.0 and float(last) >= 1.0:
                if vsb.winfo_ismapped(): vsb.pack_forget()
            else:
                if not vsb.winfo_ismapped():
                    vsb.pack(side="right", fill="y", before=self._results_canvas)
            vsb.set(first, last)

        self._results_canvas.configure(yscrollcommand=_scroll_set)
        vsb.pack(side="right", fill="y")
        self._results_canvas.pack(side="left", fill="both", expand=True)

        self._inner = tk.Frame(self._results_canvas, bg=BG)
        self._win_id = self._results_canvas.create_window(
            (0, 0), window=self._inner, anchor="nw"
        )

        def _on_inner_cfg(e):
            self._results_canvas.update_idletasks()
            ch = self._inner.winfo_reqheight()
            cv = self._results_canvas.winfo_height()
            if ch <= cv:
                self._results_canvas.configure(scrollregion=(0, 0, 0, cv))
            else:
                self._results_canvas.configure(
                    scrollregion=self._results_canvas.bbox("all"))

        def _on_canvas_cfg(e):
            self._results_canvas.itemconfig(self._win_id, width=e.width)
            _on_inner_cfg(None)

        self._inner.bind("<Configure>", _on_inner_cfg)
        self._results_canvas.bind("<Configure>", _on_canvas_cfg)
        self._results_canvas.bind(
            "<Enter>", lambda e: self._results_canvas.bind_all(
                "<MouseWheel>",
                lambda ev: self._results_canvas.yview_scroll(-1*(ev.delta//120), "units")
            )
        )
        self._results_canvas.bind(
            "<Leave>", lambda e: self._results_canvas.unbind_all("<MouseWheel>")
        )

    # ── Helpers UI ────────────────────────────────────────────────────────────

    def pack_results_area(self):
        """Mostra la toolbar e il canvas risultati."""
        self._toolbar.pack(fill="x", pady=(12, 8))
        self._results_host.pack(fill="both", expand=True)

    def _set_status(self, msg, color=TEXT_SEC):
        self._status_var.set(msg)
        self._status_lbl.configure(fg=color)

    def _auth_header(self):
        token = b64encode(f":{self._pat}".encode()).decode()
        return {"Authorization": f"Basic {token}", "Content-Type": "application/json"}

    # ── API calls ─────────────────────────────────────────────────────────────

    def _on_connect(self):
        org = _get_org_url()
        pat = _read_env_raw().get("DEVOPS_PAT", "").strip()
        if not org or not pat:
            self._set_status("✗  Configura URL e PAT in Impostazioni", ERROR_C)
            return
        self._org, self._pat = org, pat
        self._connect_btn.configure(state="disabled", text="⟳  Connessione...")
        self._set_status("Connessione in corso...", TEXT_SEC)
        threading.Thread(target=self._fetch_projects, args=(org,), daemon=True).start()

    def _fetch_projects(self, org):
        try:
            resp = requests.get(
                f"{org}/_apis/projects?api-version=7.1",
                headers=self._auth_header(), timeout=15, verify=False
            )
            if resp.status_code == 401:
                self.after(0, lambda: self._set_status("✗  PAT non valido o scaduto", ERROR_C))
                self.after(0, lambda: self._connect_btn.configure(state="normal", text="⟳  Connetti"))
                return
            resp.raise_for_status()
            projects = resp.json().get("value", [])
            if not projects:
                self.after(0, lambda: self._set_status("Nessun progetto trovato", WARNING))
                self.after(0, lambda: self._connect_btn.configure(state="normal", text="⟳  Connetti"))
                return
            self._projects = projects
            self.after(0, lambda: self._on_projects_loaded(projects))
        except Exception as ex:
            msg = str(ex)
            self.after(0, lambda: self._set_status(f"✗  {msg}", ERROR_C))
            self.after(0, lambda: self._connect_btn.configure(state="normal", text="⟳  Connetti"))

    def _on_projects_loaded(self, projects):
        names = [p["name"] for p in projects]
        self._proj_combo["values"] = names
        self._proj_combo.current(0)
        self._proj_frame.pack(fill="x", padx=20, pady=(10, 0))
        self._connect_btn.configure(state="normal", text="⟳  Connetti")
        self._set_status(f"✓  {len(projects)} progetto/i trovato/i", SUCCESS)

    def _on_load_branches(self):
        proj_name = self._proj_var.get().strip()
        if not proj_name:
            return
        org = self._org
        self._load_btn.configure(state="disabled", text="⟳  Caricamento...")
        self._set_status("Recupero repository...", TEXT_SEC)
        self._clear_results()
        threading.Thread(
            target=self._fetch_repos,
            args=(org, proj_name),
            daemon=True
        ).start()

    def _fetch_repos(self, org, project):
        try:
            resp = requests.get(
                f"{org}/{project}/_apis/git/repositories?api-version=7.1",
                headers=self._auth_header(), timeout=15, verify=False
            )
            resp.raise_for_status()
            repos = resp.json().get("value", [])
            total = len(repos)
            self.after(0, lambda: self._set_status(
                f"Caricamento branch di {total} repository...", TEXT_SEC))
            all_data = []
            for i, repo in enumerate(repos):
                try:
                    br_resp = requests.get(
                        f"{org}/{project}/_apis/git/repositories/"
                        f"{repo['id']}/refs?filter=heads/&api-version=7.1",
                        headers=self._auth_header(), timeout=15, verify=False
                    )
                    br_resp.raise_for_status()
                    default_raw = (repo.get("defaultBranch") or "").replace("refs/heads/", "")
                    branches = []
                    for b in br_resp.json().get("value", []):
                        name = b["name"].replace("refs/heads/", "")
                        branches.append({
                            "name": name,
                            "is_default": name == default_raw
                        })
                    all_data.append({"repo": repo["name"], "branches": branches})
                except Exception:
                    all_data.append({"repo": repo["name"], "branches": []})

                progress = f"Repository {i+1}/{total}: {repo['name']}..."
                self.after(0, lambda p=progress: self._set_status(p, TEXT_SEC))

            self._all_data = all_data
            self.after(0, self._on_data_ready)
        except Exception as ex:
            msg = str(ex)
            self.after(0, lambda: self._set_status(f"✗  {msg}", ERROR_C))
            self.after(0, lambda: self._load_btn.configure(
                state="normal", text="⟳  Carica branch"))

    def _on_data_ready(self):
        # Popola filtro repo
        repo_names = ["Tutti"] + [d["repo"] for d in self._all_data]
        self._repo_combo["values"] = repo_names
        self._repo_var.set("Tutti")

        # Mostra toolbar e area risultati
        self.pack_results_area()
        self._render()

        total_branches = sum(len(d["branches"]) for d in self._all_data)
        self._set_status(
            f"✓  {len(self._all_data)} repository · {total_branches} branch", SUCCESS)
        self._load_btn.configure(state="normal", text="⟳  Carica branch")

    # ── Render risultati ──────────────────────────────────────────────────────

    def _clear_results(self):
        for w in self._inner.winfo_children():
            w.destroy()

    def _render(self):
        self._clear_results()
        search = self._search_var.get().lower().strip()
        repo_filter = self._repo_var.get()

        filtered = [
            d for d in self._all_data
            if repo_filter == "Tutti" or d["repo"] == repo_filter
        ]

        if not filtered:
            tk.Label(self._inner, text="Nessun risultato.",
                     bg=BG, fg=TEXT_SEC, font=FONT_MONO,
                     pady=30).pack()
            return

        for d in filtered:
            branches = d["branches"]
            if search:
                branches = [b for b in branches if search in b["name"].lower()]
                if not branches and search:
                    continue

            self._build_repo_section(d["repo"], branches)

        # Spacer finale
        tk.Frame(self._inner, bg=BG, height=20).pack()

    def _build_repo_section(self, repo_name, branches):
        # Header repo (collassabile)
        section = tk.Frame(self._inner, bg=BG)
        section.pack(fill="x", padx=20, pady=(12, 0))

        # Stato aperto/chiuso
        is_open = [True]
        branch_container = [None]

        hdr = tk.Frame(section, bg=BG_CARD, bd=0,
                        highlightthickness=1, highlightbackground=BORDER,
                        cursor="hand2")
        hdr.pack(fill="x")

        chev = tk.Label(hdr, text="▼", bg=BG_CARD, fg=_SB_TEXT,
                        font=FONT_MONO_SM, padx=8, pady=8)
        chev.pack(side="left")

        tk.Label(hdr, text="🗄", bg=BG_CARD, fg=ACCENT,
                 font=("Consolas", 12)).pack(side="left", padx=(0, 6), pady=8)

        tk.Label(hdr, text=repo_name, bg=BG_CARD, fg=TEXT_PRI,
                 font=FONT_MONO_BOLD, anchor="w").pack(side="left", fill="x",
                                                        expand=True, pady=8)

        count_lbl = tk.Label(hdr,
                             text=f"{len(branches)} branch",
                             bg=BG_CARD2, fg=TEXT_SEC,
                             font=FONT_MONO_SM, padx=8, pady=3,
                             relief="flat")
        count_lbl.pack(side="right", padx=10, pady=8)

        def _toggle(event=None):
            if is_open[0]:
                branch_container[0].pack_forget()
                chev.configure(text="▶")
            else:
                branch_container[0].pack(fill="x")
                chev.configure(text="▼")
            is_open[0] = not is_open[0]

        for w in (hdr, chev, count_lbl):
            w.bind("<Button-1>", _toggle)
            w.bind("<Enter>", lambda e, h=hdr: h.configure(highlightbackground=ACCENT))
            w.bind("<Leave>", lambda e, h=hdr: h.configure(highlightbackground=BORDER))

        # Lista branch
        bc = tk.Frame(section, bg=BG_CARD, bd=0,
                       highlightthickness=1, highlightbackground=BORDER)
        bc.pack(fill="x")
        branch_container[0] = bc

        if not branches:
            tk.Label(bc, text="  Nessun branch trovato.",
                     bg=BG_CARD, fg=TEXT_SEC, font=FONT_MONO,
                     pady=8, anchor="w").pack(fill="x", padx=16)
        else:
            for i, b in enumerate(branches):
                self._build_branch_row(bc, b, i)

    def _build_branch_row(self, parent, branch, index):
        bg_row = BG_CARD if index % 2 == 0 else BG_CARD2
        row = tk.Frame(parent, bg=bg_row)
        row.pack(fill="x")

        # Indicatore laterale (accent se default)
        ind_color = _SB_ACCENT2 if branch["is_default"] else bg_row
        tk.Frame(row, bg=ind_color, width=3).pack(side="left", fill="y")

        tk.Label(row, text="⎇", bg=bg_row, fg=TEXT_SEC,
                 font=("Consolas", 11), padx=8, pady=6).pack(side="left")

        tk.Label(row, text=branch["name"], bg=bg_row, fg=TEXT_PRI,
                 font=FONT_MONO, anchor="w").pack(side="left", fill="x",
                                                    expand=True, pady=6)

        if branch["is_default"]:
            tk.Label(row, text="default", bg=bg_row, fg=_SB_ACCENT,
                     font=FONT_MONO_SM, padx=8).pack(side="right", padx=(0, 12))

        # Hover
        def _enter(e, r=row, ind=ind_color):
            for c in [row] + list(row.winfo_children()):
                try: c.configure(bg=BG_HOVER)
                except: pass
        def _leave(e, r=row, bg=bg_row, ind=ind_color):
            for c in [row] + list(row.winfo_children()):
                try: c.configure(bg=bg)
                except: pass
            # ripristina indicatore
            row.winfo_children()[0].configure(bg=ind_color)

        for w in [row] + list(row.winfo_children()):
            w.bind("<Enter>", _enter)
            w.bind("<Leave>", _leave)


# ════════════════════════════════════════════════════════════════════════════
# PANNELLO IMPOSTAZIONI
# ════════════════════════════════════════════════════════════════════════════

class SettingsPanel(tk.Frame):

    def __init__(self, master):
        super().__init__(master, bg=BG)
        self._status_var = tk.StringVar()
        self._build()

    def _build(self):
        style = ttk.Style()
        style.configure("SettingsTab.TNotebook",
                        background=BG, borderwidth=0, tabmargins=[0, 0, 0, 0])
        style.configure("SettingsTab.TNotebook.Tab",
                        background=BG_CARD, foreground=TEXT_SEC,
                        font=("Consolas", 9), padding=[14, 3], borderwidth=0)
        style.map("SettingsTab.TNotebook.Tab",
                  background=[("selected", BG_CARD2), ("!selected", BG_CARD)],
                  foreground=[("selected", TEXT_PRI), ("!selected", TEXT_SEC)],
                  font=[("selected", ("Consolas", 9, "bold"))],
                  padding=[("selected", [14, 5]), ("!selected", [14, 3])])

        tk.Label(self, textvariable=self._status_var, bg=BG, fg=TEXT_SEC,
                 font=FONT_MONO_SM, anchor="w").pack(side="bottom", fill="x",
                                                     padx=16, pady=4)

        nb = ttk.Notebook(self, style="SettingsTab.TNotebook")
        nb.pack(fill="both", expand=True, padx=20, pady=(12, 0))

        env = _read_env_raw()
        defaults = {"DEVOPS_ORG_URL": _DEFAULT_ORG_URL}

        for tab_label, sections in SETTINGS_TABS:
            tab = tk.Frame(nb, bg=BG)
            nb.add(tab, text=f"  {tab_label}  ")

            for section_title, fields, validator in sections:
                card = tk.Frame(tab, bg=BG_CARD, bd=0,
                                highlightthickness=1, highlightbackground=BORDER)
                card.pack(fill="x", padx=16, pady=(12, 0))
                tk.Label(card, text=section_title, bg=BG_CARD, fg=ACCENT,
                         font=("Consolas", 10, "bold"), pady=10, padx=16,
                         anchor="w").pack(fill="x")
                tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=16)

                grid = tk.Frame(card, bg=BG_CARD)
                grid.pack(fill="x", padx=16, pady=8)
                grid.columnconfigure(1, weight=1)

                section_vars = {}
                for row_i, (key, label, is_pw) in enumerate(fields):
                    tk.Label(grid, text=label, bg=BG_CARD, fg=TEXT_SEC,
                             font=("Consolas", 10), anchor="w", width=22
                             ).grid(row=row_i, column=0, sticky="w", pady=4)

                    var = tk.StringVar(value=env.get(key) or defaults.get(key, ""))
                    entry = tk.Entry(grid, textvariable=var, show="•" if is_pw else "",
                                     bg=BG_INPUT, fg=TEXT_PRI, insertbackground=TEXT_PRI,
                                     relief="flat", font=("Consolas", 10),
                                     highlightthickness=1, highlightbackground=BORDER,
                                     highlightcolor=ACCENT)
                    entry.grid(row=row_i, column=1, sticky="ew", pady=4,
                               padx=(8, 0), ipady=3)
                    section_vars[key] = var
                    if validator is None:
                        entry.bind("<FocusOut>", lambda e, k=key, v=var: self._autosave(k, v))
                        entry.bind("<Return>",   lambda e, k=key, v=var: self._autosave(k, v))

                    if is_pw:
                        eye = tk.Label(grid, text="👁", bg=BG_CARD, fg=TEXT_SEC,
                                       cursor="hand2", font=("Consolas", 11))
                        eye.grid(row=row_i, column=2, padx=(6, 0))

                        def _toggle(e, ent=entry, el=eye):
                            hidden = ent.cget("show") == "•"
                            ent.config(show="" if hidden else "•")
                            el.config(fg=ACCENT if hidden else TEXT_SEC)
                        eye.bind("<Button-1>", _toggle)

                if validator is not None:
                    self._build_validate_row(card, section_vars, validator)

    def _build_validate_row(self, card, section_vars, validator):
        row = tk.Frame(card, bg=BG_CARD)
        row.pack(fill="x", padx=16, pady=(0, 12))

        result_var = tk.StringVar()
        result_lbl = tk.Label(row, textvariable=result_var, bg=BG_CARD, fg=TEXT_SEC,
                              font=FONT_MONO, anchor="w")
        result_lbl.pack(side="left", fill="x", expand=True)

        btn = tk.Button(row, text="⟳  Connetti e Salva",
                        bg=ACCENT, fg="#ffffff", font=FONT_MONO_BOLD,
                        relief="flat", padx=14, pady=5, cursor="hand2",
                        activebackground=ACCENT, activeforeground="#ffffff")
        btn.pack(side="right")

        def _done(ok, msg, values):
            btn.configure(state="normal", text="⟳  Connetti e Salva")
            if ok:
                try:
                    _write_env(values)
                    result_var.set(f"✓  {msg} — dati salvati")
                    result_lbl.configure(fg=SUCCESS)
                except Exception as e:
                    result_var.set(f"✗  Connesso ma salvataggio fallito: {e}")
                    result_lbl.configure(fg=ERROR_C)
            else:
                result_var.set(f"✗  {msg} — dati non salvati")
                result_lbl.configure(fg=ERROR_C)

        def _worker(values):
            try:
                ok, msg = validator(values)
            except Exception as e:
                ok, msg = False, str(e)
            self.after(0, _done, ok, msg, values)

        def _on_click():
            values = {k: v.get().strip() for k, v in section_vars.items()}
            btn.configure(state="disabled", text="⟳  Connessione...")
            result_var.set("Verifica in corso...")
            result_lbl.configure(fg=TEXT_SEC)
            threading.Thread(target=_worker, args=(values,), daemon=True).start()

        btn.configure(command=_on_click)

    def _autosave(self, key, var):
        val = var.get().strip()
        if _read_env_raw().get(key, "") == val:
            return
        try:
            _write_env({key: val})
            self._status_var.set(f"✓ Salvato: {key}")
        except Exception as e:
            self._status_var.set(f"✗ Errore salvataggio: {e}")
        self.after(2000, lambda: self._status_var.set(""))


# ════════════════════════════════════════════════════════════════════════════
# LAUNCHER PRINCIPALE
# ════════════════════════════════════════════════════════════════════════════

def _setup_combo_style():
    s = ttk.Style()
    s.configure("TCombobox",
                fieldbackground=BG_INPUT, background=BG_CARD,
                foreground=TEXT_PRI, arrowcolor=TEXT_SEC,
                selectbackground=BG_CARD, selectforeground=TEXT_PRI,
                insertcolor=TEXT_PRI, relief="flat",
                borderwidth=1, padding=4)
    s.map("TCombobox",
          fieldbackground=[("readonly", BG_INPUT)],
          foreground=[("readonly", TEXT_PRI)],
          selectbackground=[("readonly", BG_CARD)])


class AzdoTool(tk.Tk):

    def __init__(self):
        super().__init__()
        _setup_scrollbar_style()
        _setup_combo_style()

        self.title("DevOps Tool - All-in-one")
        self.configure(bg=_SB_BG)
        self.resizable(True, True)
        self.minsize(860, 560)

        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "DevOps.Tool.AIO.1")
        except Exception:
            pass

        self._current_key = None
        self._frames      = {}
        self._nav_btns    = {}

        self._build_sidebar()

        right_col = tk.Frame(self, bg=BG)
        right_col.pack(side="left", fill="both", expand=True)

        self._build_header(right_col)

        self._content = tk.Frame(right_col, bg=BG)
        self._content.pack(side="top", fill="both", expand=True)

        self._select("branches")

        self.update_idletasks()
        try:
            import ctypes
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            self._apply_dark_titlebar(hwnd)
        except Exception:
            pass

        W, H = 1060, 680
        x = (self.winfo_screenwidth()  - W) // 2
        y = (self.winfo_screenheight() - H) // 2
        self.geometry(f"{W}x{H}+{x}+{y}")

    def _apply_dark_titlebar(self, hwnd):
        try:
            import ctypes
            dwm = ctypes.windll.dwmapi
            DWMWA_DARK = 20
            val = ctypes.c_int(1)
            dwm.DwmSetWindowAttribute(hwnd, DWMWA_DARK,
                                      ctypes.byref(val), ctypes.sizeof(val))
            r, g, b = 0x0f, 0x11, 0x17
            colorref = ctypes.c_uint32(r | (g << 8) | (b << 16))
            dwm.DwmSetWindowAttribute(hwnd, 35,
                                      ctypes.byref(colorref), ctypes.sizeof(colorref))
        except Exception:
            pass

    # ── Header ────────────────────────────────────────────────────────────────

    def _build_header(self, parent):
        hdr = tk.Frame(parent, bg=BG, pady=12)
        hdr.pack(fill="x", padx=20)

        title_col = tk.Frame(hdr, bg=BG)
        title_col.pack(side="left")
        self._hdr_title = tk.Label(title_col, text="", bg=BG, fg=TEXT_PRI,
                                   font=("Consolas", 15, "bold"), anchor="w")
        self._hdr_title.pack(anchor="w")

        self._hdr_version = tk.Label(hdr, text=f"v{VERSION}", bg=BG,
                                     fg=TEXT_SEC, font=FONT_MONO_SM, padx=8)
        self._hdr_version.pack(side="right", anchor="center")

        if _UPDATE_INFO:
            badge = tk.Label(hdr, text=f"↑ v{_UPDATE_INFO[0]}", bg=ACCENT, fg="#ffffff",
                             font=FONT_MONO_BOLD, padx=10, pady=3, cursor="hand2")
            badge.bind("<Button-1>", lambda e: _show_update_dialog(self))
            badge.bind("<Enter>", lambda e: badge.configure(bg="#3a7ee8"))
            badge.bind("<Leave>", lambda e: badge.configure(bg=ACCENT))
            badge.pack(side="right", padx=(0, 8))

        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=20)

    # ── Sidebar ───────────────────────────────────────────────────────────────

    def _build_sidebar(self):
        sb = tk.Frame(self, bg=_SB_BG, width=170)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        # Logo
        top = tk.Frame(sb, bg=_SB_BG)
        top.pack(fill="x")
        logo = tk.Frame(top, bg=_SB_BG)
        logo.pack(pady=13)
        txt = tk.Frame(logo, bg=_SB_BG)
        txt.pack(side="left")
        tk.Label(txt, text="DevOps", font=("Consolas", 13, "bold"),
                 fg=_SB_ACCENT, bg=_SB_BG).pack(side="left")
        tk.Label(txt, text="|", font=("Consolas", 13),
                 fg=_SB_BORDER, bg=_SB_BG, padx=2).pack(side="left")
        tk.Label(txt, text="AIO", font=("Consolas", 13, "bold"),
                 fg=_SB_TEXT_SEL, bg=_SB_BG).pack(side="left")

        tk.Frame(sb, bg=_SB_BORDER, height=1).pack(fill="x")

        # Voci di navigazione
        nav = tk.Frame(sb, bg=_SB_BG)
        nav.pack(fill="x")

        _NAV_ITEMS = [
            ("branches", "⎇", "Branches"),
            # futuri pannelli qui
        ]

        for key, icon, label in _NAV_ITEMS:
            self._make_nav_item(nav, key, icon, label, bg=_SB_ITEM_BG)

        # Footer sidebar
        tk.Frame(sb, bg=_SB_BORDER, height=1).pack(side="bottom", fill="x")
        tk.Label(sb, text=f"v{VERSION}", bg=_SB_BG, fg=_SB_TEXT,
                 font=FONT_MONO_SM, anchor="center", pady=4
                 ).pack(side="bottom", fill="x")
        tk.Frame(sb, bg=_SB_BORDER, height=1).pack(side="bottom", fill="x")

        bottom_nav = tk.Frame(sb, bg=_SB_BG)
        bottom_nav.pack(side="bottom", fill="x")
        self._make_nav_item(bottom_nav, "settings", "⚙", "Impostazioni", bg=_SB_BG)

    def _make_nav_item(self, parent, key, icon_text, label_text, bg=_SB_ITEM_BG):
        btn_frame = tk.Frame(parent, bg=bg, cursor="hand2")
        btn_frame.pack(fill="x")

        indicator = tk.Frame(btn_frame, bg=bg, width=3)
        indicator.pack(side="left", fill="y")

        icon_lbl = tk.Label(btn_frame, text=icon_text, bg=bg, fg=_SB_TEXT,
                            font=("Consolas", 14), padx=6, width=2, anchor="center")
        icon_lbl.pack(side="left", fill="y")

        lbl = tk.Label(btn_frame, text=label_text, bg=bg, fg=_SB_TEXT,
                       font=FONT_MONO, anchor="w", pady=10)
        lbl.pack(side="left", fill="x", expand=True)

        self._nav_btns[key] = (icon_lbl, lbl, indicator, btn_frame)

        def _click(e, k=key):
            self._select(k)

        def _enter(e, b=btn_frame, ic=icon_lbl, lb=lbl, k=key):
            if self._current_key == k:
                return
            for w in (b, ic, lb):
                w.configure(bg=BG_HOVER)

        def _leave(e, b=btn_frame, ic=icon_lbl, lb=lbl, k=key):
            cur_bg = _SB_BG_SEL if self._current_key == k else bg
            for w in (b, ic, lb):
                w.configure(bg=cur_bg)

        for w in (btn_frame, icon_lbl, lbl):
            w.bind("<Button-1>", _click)
            w.bind("<Enter>",    _enter)
            w.bind("<Leave>",    _leave)

    def _select(self, key):
        if key == self._current_key:
            return
        self._current_key = key

        # Aggiorna aspetto bottoni
        for k, (icon_lbl, label_lbl, indicator, btn_frame) in self._nav_btns.items():
            if k == key:
                indicator.configure(bg=_SB_ACCENT2)
                for w in (btn_frame, icon_lbl):
                    w.configure(bg=_SB_BG_SEL)
                icon_lbl.configure(fg=_SB_TEXT_SEL)
                label_lbl.configure(bg=_SB_BG_SEL, fg=_SB_ACCENT)
            else:
                bg = _SB_BG if k == "settings" else _SB_ITEM_BG
                indicator.configure(bg=bg)
                for w in (btn_frame, icon_lbl, label_lbl):
                    w.configure(bg=bg)
                icon_lbl.configure(fg=_SB_TEXT)
                label_lbl.configure(fg=_SB_TEXT)

        # Nasconde tutto il contenuto corrente
        for f in self._content.winfo_children():
            f.pack_forget()

        # Crea o mostra il frame
        if key not in self._frames:
            if key == "branches":
                frame = BranchesPanel(self._content)
            elif key == "settings":
                frame = SettingsPanel(self._content)
            else:
                frame = tk.Frame(self._content, bg=BG)
                tk.Label(frame, text=f"Sezione '{key}' — coming soon",
                         bg=BG, fg=TEXT_SEC, font=FONT_MONO).pack(pady=40)
            frame.pack(fill="both", expand=True)
            self._frames[key] = frame
        else:
            self._frames[key].pack(fill="both", expand=True)

        titles = {"branches": "Branches", "settings": "Impostazioni"}
        self._hdr_title.configure(text=titles.get(key, key.title()))


# ── Aggiornamento ─────────────────────────────────────────────────────────────

def _show_update_dialog(app):
    if not _UPDATE_INFO:
        return
    latest, url = _UPDATE_INFO

    popup = tk.Toplevel(app)
    popup.title("Aggiornamento disponibile")
    popup.configure(bg=BG)
    popup.resizable(False, False)
    popup.grab_set()
    W, H = 420, 210
    x = app.winfo_x() + (app.winfo_width()  - W) // 2
    y = app.winfo_y() + (app.winfo_height() - H) // 2
    popup.geometry(f"{W}x{H}+{x}+{y}")

    outer = tk.Frame(popup, bg=BORDER, bd=1)
    outer.pack(fill="both", expand=True, padx=1, pady=1)
    inner = tk.Frame(outer, bg=BG)
    inner.pack(fill="both", expand=True, padx=1, pady=1)

    tk.Label(inner, text="Aggiornamento disponibile",
             bg=BG, fg=TEXT_PRI, font=("Consolas", 12, "bold")).pack(pady=(20, 4))
    tk.Label(inner, text=f"Versione attuale:  {VERSION}",
             bg=BG, fg=TEXT_SEC, font=("Consolas", 10)).pack()
    tk.Label(inner, text=f"Nuova versione:    {latest}",
             bg=BG, fg=SUCCESS, font=("Consolas", 10, "bold")).pack(pady=(2, 16))
    tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", padx=20)

    status_var = tk.StringVar()
    tk.Label(inner, textvariable=status_var, bg=BG, fg=TEXT_SEC,
             font=FONT_MONO).pack(pady=(8, 0))

    btn_row = tk.Frame(inner, bg=BG)
    btn_row.pack(pady=(6, 16))

    def _do_update():
        btn_update.configure(state="disabled")
        btn_later.configure(state="disabled")
        status_var.set("Download in corso...")
        popup.update()
        try:
            import shutil
            resp = requests.get(url, timeout=60, stream=True)
            resp.raise_for_status()
            current = Path(__file__).resolve()
            tmp = current.with_suffix(".pyw.new")
            with open(tmp, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            shutil.move(str(tmp), str(current))
            status_var.set("Aggiornato. Riavvio in corso...")
            popup.update()
            subprocess.Popen([sys.executable, str(current)])
            sys.exit(0)
        except Exception as e:
            status_var.set(f"Errore: {e}")
            btn_later.configure(state="normal")

    btn_update = tk.Button(btn_row, text="Aggiorna ora", command=_do_update,
                           bg=ACCENT, fg="#ffffff", font=("Consolas", 10, "bold"),
                           relief="flat", padx=18, pady=6, cursor="hand2",
                           activebackground=ACCENT, activeforeground="#ffffff")
    btn_update.pack(side="left", padx=(0, 10))

    btn_later = tk.Button(btn_row, text="Più tardi", command=popup.destroy,
                          bg=BG_CARD, fg=TEXT_SEC, font=("Consolas", 10),
                          relief="flat", padx=18, pady=6, cursor="hand2",
                          activebackground=BG_HOVER, activeforeground=TEXT_PRI)
    btn_later.pack(side="left")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore")
    _splash.set("Pronto.")
    _splash._root.after(300, _splash.destroy)
    _splash._root.mainloop()
    app = AzdoTool()
    app.lift()
    app.attributes("-topmost", True)
    app.after(200, lambda: app.attributes("-topmost", False))
    app.focus_force()
    if _UPDATE_INFO:
        app.after(500, lambda: _show_update_dialog(app))
    app.mainloop()
