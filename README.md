# ViaLibera — Banche dati quiz ministeriali

Repository pubblico con **sole domande e figure di esercitazione** per l'app Android ViaLibera. Non ospita dati personali né progressi degli utenti.

## Prima pubblicazione

1. Scarica il file `ViaLibera_Feed_Aggiornamenti.zip` dalla conversazione ChatGPT.
2. Apri [Carica i file nel repository](https://github.com/matteofronzi199076-dev/ViaLibera-Quiz-Updates/upload/main).
3. Trascina **lo ZIP intero**, senza estrarlo; mantieni il nome esatto `ViaLibera_Feed_Aggiornamenti.zip`.
4. Premi **Commit changes**. Il workflow «Pubblica banche dati quiz» verifica contenuto, risposte, immagini, conteggi e SHA-256, poi pubblica automaticamente `manifest.json` e cinque file JSON.
5. Apri [GitHub Actions](https://github.com/matteofronzi199076-dev/ViaLibera-Quiz-Updates/actions) e controlla che il workflow termini in verde.

## Configurazione nell'app

Nella versione **ViaLibera 1.1**, apri *Ministero → Aggiornamenti*. Inserisci l'indirizzo:

```
https://raw.githubusercontent.com/matteofronzi199076-dev/ViaLibera-Quiz-Updates/main/manifest.json
```

Attiva «Controllo automatico» e premi «Controlla ora». Quando configurato, l'app controlla le nuove versioni ogni 7 giorni all'apertura, con una connessione internet disponibile. Le banche dati integrate restano consultabili offline.

## Origine e limitazioni

- **AM:** 2.035 quesiti (PDF del 04/04/2025).
- **A/B:** 7.106 quesiti (PDF del 23/04/2025).
- **Patenti superiori:** 3.456 quesiti (PDF del 04/04/2025).
- **CQC:** 5.528 quesiti (PDF del 25/11/2025).
- **CAP KB:** 514 gruppi di quesiti a scelta (PDF fornito).

**Totale: 18.639 unità di esercitazione.** Il formato CAP non equivale a 514 singole affermazioni vero/falso.

I dati provengono dai PDF ministeriali forniti dall'utente, non da un'API ufficiale di aggiornamento in tempo reale. La pubblicazione automatica verifica **integrità tecnica e coerenza**, ma non dimostra che i quesiti siano l'ultima versione pubblicata dal Ministero. Eventuali nuove edizioni devono essere estratte e confrontate con il Portale dell'Automobilista prima di essere pubblicate.

**Revisioni e ADR:** non ancora presenti nei cinque file JSON. L'app può mostrare le sezioni predisposte, ma non inventa quesiti mancanti.

Il monitor nel repository privato ViaLibera-Android può segnalare variazioni di collegamenti ministeriali. **Non sostituisce automaticamente i quiz senza una nuova banca dati verificata.**

I file pubblicati sono liberamente leggibili da Internet; non inserire password, file privati o informazioni identificative nei JSON.
