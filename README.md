# SalesUp Tool - All-in-one

Applicazione desktop Windows che raccoglie più strumenti in un'unica interfaccia dark-themed. La sidebar è organizzata in macro-sezioni collassabili: **DevOps**, con lo strumento Branches per consultare Azure DevOps, e **Files**, con lo strumento MD Converter per trasformare documenti Word in Markdown.

## Avvio

Doppio clic su `Salesup Tool - All-In-One.pyw` (nessuna console). Le dipendenze mancanti vengono installate automaticamente all'avvio, con l'avanzamento mostrato nella splash screen.

## Strumenti disponibili

| Sezione | Strumento | Descrizione |
|---------|-----------|-------------|
| **DevOps** | Branches | Elenca i branch di tutti i repository di un progetto Azure DevOps, con evidenza del branch di default, ricerca per nome e filtro per repository |
| **Files** | MD Converter | Converte documenti Word (`.docx`) in Markdown (`.md`) mantenendo titoli, formattazione, elenchi e tabelle; lista con drag & drop e output in cartella dedicata |
| | Impostazioni | Configurazione di Organization URL e Personal Access Token, con verifica della connessione prima del salvataggio |
| | About | Documentazione del tool e versione corrente, consultabili direttamente nell'interfaccia |

## Configurazione

L'URL dell'organizzazione Azure DevOps e il Personal Access Token si impostano da **⚙ Impostazioni → Branches** e vengono salvati in un file di configurazione locale, escluso da git: le credenziali non vengono mai pushate.

Il PAT deve avere almeno i permessi di lettura su progetti e codice.

## Aggiornamenti e release

All'avvio il tool controlla l'ultima release di questo repository e, se è disponibile una versione più recente, propone di scaricarla e riavviarsi.

Per pubblicare una nuova versione:
1. aumenta `VERSION` in `Salesup Tool - All-In-One.pyw`
2. aggiungi la voce in `CHANGELOG.md`
3. fai push su `main`

Il workflow GitHub Actions crea automaticamente tag e release `v<VERSION>` con il `.pyw` allegato. I push con versione invariata non creano release.

## Documentazione

- [`ABOUT.md`](ABOUT.md) — funzionamento dettagliato di ogni sezione
- [`CHANGELOG.md`](CHANGELOG.md) — storico delle versioni

## Dipendenze principali

- `requests` — chiamate alle API REST di Azure DevOps e GitHub
- `tkinterdnd2` — trascinamento dei file (drag & drop)
- `mammoth` — conversione da Word a Markdown

## Requisiti

- Windows 10/11
- Python 3.x con `pip`
