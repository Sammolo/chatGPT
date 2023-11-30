key=""
documento = "fileProva.pdf"

from openai import OpenAI #importo libreria OpenAI

client = OpenAI(api_key=key)


def creaAssistente( doc ): #1- creo l'assistente

  #Creo il file
  file = client.files.create(
    file=open(doc, "rb"),  #do il file in input
    purpose='assistants'
  )

  #Creo l'assistente  
  assistant = client.beta.assistants.create(
    name="Primo assistente di test", #ignorabile
    instructions="Analizza il file e fornisci risposte basandoti sul file stesso, citando frasi del file stesso se possibile", #qui specifico come l'assistente dovrebbe comportarsi o rispondere
    tools=[{"type": "retrieval"}], #modalità per prendere file come input
    model="gpt-3.5-turbo-1106", #specifico quale gpt usare 
    file_ids=[file.id] #assegno il file da elaborare
  )

  return file, assistant

#assegno la domanda alla chat
def eseguiAssistente(idFile, idAssistente, domanda):

  thread = client.beta.threads.create( #2- creo il thread per la conversazione
    #creo il messaggio
    messages = [
      {
        "role": "user",
        "content": domanda,
        "file_ids": [idFile]
      }
    ]
  )

  run = client.beta.threads.runs.create( #3- eseguo il thread
    thread_id= thread.id,
    assistant_id= idAssistente
  )

  return thread, run

#ottengo la risposta alla domanda
def getRisposta(thread, run):
  while(run.status != "completed"): #FONDAMENTALE
    run = client.beta.threads.runs.retrieve(
      thread_id = thread.id,
      run_id = run.id
    )
  
  messages = client.beta.threads.messages.list(
    thread_id = thread.id
  )

  contenutoMessaggio = messages.data[0].content[0].text.value

  return contenutoMessaggio

#interagisco più volte con l'assistente
def chatta(idFile, idAssistente):

  print("Sto analizzando il file...")
  while(True):
    domanda = input("\n Scrivi la domanda a cui vuoi che io risponda o digita 'esci' per fermarti\n")
    if(domanda == "esci"):
      break
    else:
      thread, objRun = eseguiAssistente(idFile, idAssistente, domanda)
      messaggio = getRisposta(thread, objRun)
      print(messaggio) #stampo il messaggio
  
  print("\n Alla prossima!")



#PROGRAMMA
file, assistente = creaAssistente(documento) #creo l'assistente
chatta(file.id, assistente.id)