### v1.0.3 — 2026-10-16
- **MD Converter — conversione**: ripristinato il comportamento di conversione iniziale, più aderente alla struttura dell'elenco così come definita nel documento Word di partenza

### v1.0.2 — 2026-10-16
- **MD Converter — qualità della conversione**: i titoli di sezione che nel documento Word sono numerati vengono riconosciuti e resi come titoli Markdown; gli elenchi numerati mantengono una numerazione progressiva corretta anziché ripartire sempre da uno
- **MD Converter — pulizia output**: a ogni conversione la cartella di output viene svuotata dai file della conversione precedente, così rimangono solo i risultati più recenti
- **Configurazione**: all'avvio, se la cartella di configurazione e il file `.env` non esistono, vengono creati automaticamente (file vuoto, senza sovrascrivere eventuali impostazioni già presenti)
- **Aggiornamenti**: con l'aggiornamento vengono ora scaricati anche i file di documentazione (CHANGELOG, ABOUT, README), così restano allineati e vengono creati anche se non presenti in locale
- **Aggiornamenti — changelog post-update**: dopo un aggiornamento, al riavvio viene mostrato un popup con le novità della versione appena installata
- **About**: nuova sezione nella sidebar (in basso) che mostra la documentazione del tool e la versione corrente
- **Header**: in alto a destra il badge di versione compare solo quando è disponibile un aggiornamento; la versione corrente resta indicata in fondo alla sidebar

### v1.0.1 — 2026-10-16
- **Rebranding**: l'applicazione è stata rinominata da "DevOps Tool" a **SalesUp Tool - All-in-one** — aggiornati titolo finestra, logo, splash screen, AppUserModelID e chiavi di configurazione (`SALESUP_ORG_URL`, `SALESUP_PAT`)
- **Navigazione**: la sidebar è ora organizzata in macro-sezioni collassabili — **DevOps** (che contiene Branches) e **Files** (che contiene MD Converter)
- **MD Converter**: nuovo strumento nella sezione Files che converte file Word (`.docx`) in Markdown (`.md`) — lista file con drag & drop, controllo del formato e dei duplicati tramite percorso, rimozione singola o totale, pannello di log e barra di stato
- **MD Converter**: la conversione preserva la struttura del documento (titoli, grassetto, corsivo, liste puntate e numerate, tabelle, link e immagini) producendo Markdown pulito; i file generati vengono salvati in `output/md converter/` e la cartella viene aperta al termine
- **Dipendenze**: aggiunte `tkinterdnd2` (drag & drop) e `mammoth` (conversione Word→Markdown), installate automaticamente all'avvio

### v1.0.0 — 2026-10-02
- **Branches**: visualizzazione di tutti i branch dei repository di un progetto Azure DevOps — connessione all'organizzazione, selezione progetto, sezioni collassabili per repository, evidenziazione del branch di default
- **Branches**: ricerca branch per nome in tempo reale e filtro per singolo repository
- **Branches**: URL e PAT non più inseriti nel pannello — letti da `config/.env` al click su ⟳ Connetti, con rimando alle Impostazioni se mancanti
- **Impostazioni**: nuova sezione nella sidebar in basso, organizzata in tab; tab **Branches** con sezione Azure DevOps (Organization URL, Personal Access Token con toggle 👁)
- **Impostazioni — Connetti e Salva**: verifica delle credenziali prima del salvataggio — i dati vengono scritti nel file di configurazione locale solo se la connessione riesce; gestiti URL/PAT mancanti, server non raggiungibile, timeout, PAT non valido (anche risposta 203 con pagina di login)
- **Splash screen**: schermata di avvio con barra di avanzamento — verifica dipendenze, controllo aggiornamenti, caricamento interfaccia
- **Dipendenze**: installazione automatica via pip dei pacchetti mancanti senza finestre di console; in caso di errore popup con il comando manuale
- **Aggiornamenti**: controllo all'avvio dell'ultima release su GitHub — badge nell'header, popup con download, sostituzione del `.pyw` e riavvio automatico
- **Release**: workflow GitHub Actions che ad ogni push su `main` crea tag e release `v<VERSION>` se non esistono già, allegando il `.pyw`
- **Git**: `.gitignore` che esclude `config/` e i file `.env` — le credenziali non vengono mai pushate
- **Refactoring**: rimossa la doppia inizializzazione dello stile combobox e l'elemento duplicato nelle tuple dei bottoni di navigazione
