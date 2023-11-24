key=""

from openai import OpenAI #importo libreria OpenAI

client = OpenAI(api_key=key)

#L'assistente si divide in 4 parti
#1- creo l'assistente
#NB: l'assistente prende 4 parametri che saranno fondamentali per la risposta che darà
assistant = client.beta.assistants.create(
    name="Primo assistente di test", #ignorabile
    instructions="You are a data analyst. From a file draw a graphic", #qui specifico come l'assistente dovrebbe comportarsi o rispondere
    model="gpt-4-32k-0314", #specifico quale gpt usare
    tools=[{"type": "retrieval"}] #modalità per prendere file come input
)


#2- creo il tread quando l'utente inizia la conversazione
thread = client.beta.threads.create()

#3- aggiungo la domanda dell'utente come messaggio al tread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=input("Scrivi la domanda che vuoi fare all'assistente riguardo il file che hai caricato /n")
)


#4- faccio eseguire l'assistente sul tread per avere la risposta alla domanda
#NB: per questo specifico assistente creo anche il codice per inserire il file che poi andrà ad analizzare
file = client.files.create(
  file=open("fileProva.pdf", "rb"),
  purpose='assistants'
)

run = client.beta.threads.runs.create( #assegno l'assistente al tread
  thread_id=thread.id,
  assistant_id=assistant.id
)

#eseguo
run = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)

messages = client.beta.threads.messages.list(
  thread_id=thread.id
)



#print(completion.choices[0].message)