key=""
documento = "file.pdf"

from openai import OpenAI #importo libreria OpenAI

client = OpenAI(api_key=key)


def creaAssistente(): #1- creo l'assistente

  #Creo il file
  file = client.files.create(
    file=open(documento, "rb"),  #do il file in input
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


def eseguiAssistente(idFile, idAssistente):

  domanda = str(input("\nCosa vuoi chiedere? \n")) #faccio scrivere all'utente la domanda da fare

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







#PROGRAMMA
file, assistente = creaAssistente()
thread, objRun = eseguiAssistente(file.id, assistente.id)
messaggio = getRisposta(thread, objRun)
print(messaggio) #stampo il messaggio