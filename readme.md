# Guida per utilizzare il codice

1. installare il pacchetto di OpenAI <br>
<code> pip install --upgrade openai </code>

2. generare e scaricare dal sito di [openAI](https://platform.openai.com/api-keys) la chiave ed inserirla tra le virgolette nella riga di codice<br>
<code>key="inserisci qui la chiave che hai generato"</code>

3. inserire il percorso del file alla riga di codice **32** <br> 
NB: [questi](https://platform.openai.com/docs/assistants/tools/supported-files) sono i file supportati al momento (colonna di destra) <br>
<code>file = client.files.create( <br>
  file=open("INSERISCI QUI IL TUO FILE.pdf", "rb"), <br>
  purpose='assistants' <br>
)</code>