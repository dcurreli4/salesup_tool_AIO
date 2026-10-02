# DevOps Tool - All-in-one

## ⎇ Branches

### Cosa fa
Mostra tutti i branch dei repository di un progetto Azure DevOps in un'unica schermata, senza dover aprire i repository uno alla volta dal portale.

### Come si usa
**Connetti** — Si collega all'organizzazione Azure DevOps configurata in Impostazioni e carica l'elenco dei progetti. Se URL o PAT non sono configurati, viene mostrato un messaggio che rimanda alle Impostazioni.

**Progetto** — Dopo la connessione compare il selettore del progetto. Il bottone ⟳ Carica branch recupera tutti i repository del progetto e, per ognuno, l'elenco dei branch. L'avanzamento repository per repository è mostrato nella barra di stato.

### Risultati
Ogni repository è una sezione collassabile (clic sull'intestazione) con il numero di branch a destra. Il branch di default del repository è evidenziato con l'indicatore viola a sinistra e l'etichetta **default**. Se il caricamento di un singolo repository fallisce, la sezione viene mostrata vuota senza bloccare gli altri.

### Filtri
**Ricerca** — Il campo 🔍 filtra i branch per nome in tempo reale (non distingue maiuscole e minuscole). I repository senza branch corrispondenti vengono nascosti.

**Repository** — Il menu a tendina permette di mostrare un solo repository oppure tutti.

## ⚙ Impostazioni

### Cosa fa
Raccoglie le configurazioni del tool, organizzate in tab. Si apre dalla voce ⚙ Impostazioni in basso nella sidebar.

### Tab Branches
Sezione **Azure DevOps** con due campi:
- **Organization URL** — indirizzo dell'organizzazione Azure DevOps, precompilato con un valore di default
- **Personal Access Token** — nascosto; l'icona 👁 lo rende visibile

### Connetti e Salva
Il bottone ⟳ Connetti e Salva verifica le credenziali leggendo i progetti dell'organizzazione. I dati vengono salvati **solo se la connessione riesce**; in caso contrario il motivo dell'errore viene mostrato in rosso (URL o PAT mancanti, server non raggiungibile, timeout, PAT non valido o scaduto) e il file di configurazione resta invariato.

### Permessi del PAT
Il PAT deve avere almeno gli scope **Project and Team (Read)**, per elencare i progetti, e **Code (Read)**, per leggere repository e branch.

## 🔧 Configurazione

### File .env
URL e PAT sono salvati in un file `.env` locale nella cartella `config/`, esclusa da git tramite `.gitignore`: le credenziali non vengono mai pushate sul repository.

### Dipendenze
L'unica dipendenza esterna è `requests`. Viene verificata ad ogni avvio e, se manca, installata automaticamente tramite pip senza aprire finestre di console. Se l'installazione fallisce viene mostrato il comando da eseguire a mano.

### Splash screen
All'avvio una splash screen mostra l'avanzamento: verifica dipendenze, controllo aggiornamenti, caricamento interfaccia.

## ⬆ Aggiornamenti

### Controllo automatico
Ad ogni avvio il tool confronta la propria versione con l'ultima release pubblicata sul repository GitHub del progetto. Se ne trova una più recente mostra il badge **↑ vX.Y.Z** nell'header e apre il popup di aggiornamento.

### Installazione
Il bottone **Aggiorna ora** scarica il nuovo file `.pyw` dalla release, sostituisce quello attuale e riavvia il tool. **Più tardi** chiude il popup; il badge resta visibile nell'header per aggiornare in un secondo momento.

### Pubblicazione di una nuova versione
Il rilascio è automatico tramite GitHub Actions (`.github/workflows/release.yml`). Ad ogni push su `main` il workflow legge `VERSION` dal file e, se il tag `v<versione>` non esiste ancora, crea tag e release allegando il `.pyw`. Per pubblicare basta aumentare `VERSION` e fare push; i push con versione invariata non creano release.
