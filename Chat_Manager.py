import redis
import threading
import redis
from datetime import datetime, timedelta



def dnd(connessione_redis, utente_corrente):
    stato_attuale = connessione_redis.hexists("dnd", utente_corrente)
    if stato_attuale:
        connessione_redis.hdel("dnd", utente_corrente)
        print("Modalità 'Do Not Disturb' disattivata.")
    else:
        connessione_redis.hset("dnd", utente_corrente, "attivato")
        print("Modalità 'Do Not Disturb' attivata.")

def dnd_attivo(connessione_redis, utente_destinatario):
    stato_attuale = connessione_redis.hexists("dnd", utente_destinatario)
    return stato_attuale


def ricevi_messaggi(connessione_redis, chiave_chat):
    while True:
        _, messaggio = connessione_redis.blpop(chiave_chat)
        print(messaggio.decode())

def invia_messaggio(connessione_redis, chiave_chat, utente_corrente, testo):
    messaggio = f"{utente_corrente}: {testo} [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]"
    connessione_redis.rpush(chiave_chat, messaggio)

def gestisci_chat(connessione_redis, utente_corrente, destinatario):
    chiave_chat = f"chat:{utente_corrente}:{destinatario}"

    messaggi_presenti = connessione_redis.exists(chiave_chat)

    if not messaggi_presenti:
        # Solo se la chat è appena stata creata
        print(f"\n>> Chat con {destinatario} <<")
        print("La chat è iniziata. Ora puoi scambiare messaggi.")

    # Avvia un thread per ricevere messaggi in modo asincrono
    thread_ricezione = threading.Thread(target=ricevi_messaggi, args=(connessione_redis, chiave_chat), daemon=True)
    thread_ricezione.start()

    while True:
        testo = input("\nInserisci il testo del messaggio (digita '9' per tornare al menu precedente): ")
        
        if testo.lower() == '9':
            break

        invia_messaggio(connessione_redis, chiave_chat, utente_corrente, testo)

    # Aspetta la fine del thread di ricezione prima di terminare
    thread_ricezione.join()



def visualizza_lista_chat(connessione_redis, utente_corrente):
    chiavi_chat = connessione_redis.keys(f"chat:{utente_corrente}:*")
    
    if chiavi_chat:
        print("\n>> Lista delle Chat <<")
        for chiave in chiavi_chat:
            destinatario = chiave.decode().split(":")[-1]
            print(destinatario)
    else:
        print("\nNessuna chat presente.")

