# menu_manager.py
from User_Manager import *
from Chat_Manager import *
import redis
from colorama import init, Fore

def connetti_a_redis():
    return redis.Redis(
        host='redis-15124.c135.eu-central-1-1.ec2.cloud.redislabs.com',
        port=15124,
        password='vZnU3ir0plHo4dvCrSBd3ILtTDJTUDNX'
    )

def menu_iniziale():
    print("\nMenù Iniziale:")
    print("1. Registrazione utente")
    print("2. Login")
    print("3. Esci")

def gestisci_scelta_iniziale(scelta_iniziale, connessione_redis):
    if scelta_iniziale == '1':
        registrazione_utente(connessione_redis)
    elif scelta_iniziale == '2':
        esegui_login(connessione_redis)
    elif scelta_iniziale == '3':
        print("Uscita dal programma.")
    else:
        print("Scelta non valida. Riprova.")

def esegui_login(connessione_redis,):

    utente_corrente = None
    while utente_corrente is None:
        utente_corrente = login_utente(connessione_redis,)
        stato_dnd = "Attiva" if dnd_attivo(connessione_redis, utente_corrente) else "Disattiva"
    menu_dopo_login(connessione_redis, utente_corrente, stato_dnd)

def menu_dopo_login(connessione_redis, utente_corrente, stato_dnd):
    init(autoreset=True)

    while True:
        stato_dnd = "Attiva" if dnd_attivo(connessione_redis, utente_corrente) else "Disattiva"
        colore_stato = Fore.RED if stato_dnd == "Attiva" else Fore.GREEN
        print("\nHome")
        print(f'\nUser: {utente_corrente}')
        print(f"{colore_stato}0. 'Do Not Disturb': {stato_dnd}\n")

        print("1. Gestione Contatti")
        print('2. Chat')
        print("8. Torna al Menù Iniziale")

        scelta_dopo_login = input("Seleziona un'opzione (1/2/3/4/5/6/7/8): ")

        gestisci_scelta_dopo_login(scelta_dopo_login, connessione_redis, utente_corrente)

        if scelta_dopo_login == '8':
            break

def menu_aggiungi_contatto(connessione_redis, utente_corrente):
    while True:
        print("\nMenù Aggiunta Contatto:")
        print("1. Aggiungi un utente alla tua lista contatti")
        print("2. Torna al Menù principale")

        scelta_aggiunta_contatto = input("Seleziona un'opzione (1/2): ")

        if scelta_aggiunta_contatto == '1':
            aggiungi_contatto(connessione_redis, utente_corrente)

            lista_contatti_aggiornata = connessione_redis.hget("lista_contatti", utente_corrente)
            if lista_contatti_aggiornata:
                print(f"Lista Contatti Aggiornata: {lista_contatti_aggiornata.decode()}")
            else:
                print("Lista Contatti Aggiornata: vuota")

        elif scelta_aggiunta_contatto == '2':
            break
        else:
            print("Scelta non valida. Riprova.")


def gestisci_scelta_dopo_login(scelta_dopo_login, connessione_redis, utente_corrente):
    if scelta_dopo_login == '1':
        gestione_contatti_menu(connessione_redis, utente_corrente)
    elif scelta_dopo_login == '0':
        dnd(connessione_redis, utente_corrente)
    elif scelta_dopo_login == '2':
        menu_chat(connessione_redis, utente_corrente)
    else:
        print("Scelta non valida. Riprova.")

def gestione_contatti_menu(connessione_redis, utente_corrente):
    while True:
        print("\nMenù Gestione Contatti:")
        print("1. Visualizza lista contatti")
        print("2. Ricerca utenti")
        print("3. Aggiungi un utente alla tua lista contatti")
        print("4. Torna al Menù precedente")

        scelta_gestione_contatti = input("Seleziona un'opzione (1/2/3/4): ")

        if scelta_gestione_contatti == '1':
            visualizza_lista_contatti(connessione_redis, utente_corrente)
        elif scelta_gestione_contatti == '2':
            ricerca_utenti(connessione_redis)
        elif scelta_gestione_contatti == '3':
            menu_aggiungi_contatto(connessione_redis, utente_corrente)
        elif scelta_gestione_contatti == '4':
            break
        else:
            print("Scelta non valida. Riprova.")

def menu_chat(connessione_redis, utente_corrente):
    while True:
        print("\nSotto-Menù Chat:")
        print("1. Avvia una nuova chat")
        print("2. Visualizza lista chat")
        print("3. Torna al Menù principale")

        scelta_chat = input("Seleziona un'opzione (1/2/3): ")

        if scelta_chat == '1':
            destinatario = input("\nInserisci il nome utente del destinatario: ")
            gestisci_chat(connessione_redis, utente_corrente, destinatario)
        elif scelta_chat == '2':
            visualizza_lista_chat(connessione_redis, utente_corrente)
            destinatario = input("\nSeleziona una chat (inserisci il nome utente):\n'3' per tornare indietro ")
            if destinatario == '0':
                break  # Aggiunto per uscire dal loop
            elif connessione_redis.exists(f"chat:{utente_corrente}:{destinatario}"):
                gestisci_chat(connessione_redis, utente_corrente, destinatario)
            else:
                print(f"\nLa chat con {destinatario} non esiste.")
        elif scelta_chat == '3':
            break  # Aggiunto per uscire dal loop
        else:
            print("Scelta non valida. Riprova.")



                  
def main():
    connessione_redis = connetti_a_redis()

    while True:
        menu_iniziale()
        scelta_iniziale = input("Seleziona un'opzione (1/2/3): ")
        gestisci_scelta_iniziale(scelta_iniziale, connessione_redis)

        if scelta_iniziale == '3':
            break


if __name__ == "__main__":
    main()

