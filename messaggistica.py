import redis
from datetime import datetime, timedelta

def login_utente(redis_conn):
    nome_utente = input("Inserisci il nome utente: ")
    password = input("Inserisci la password: ")

    if not redis_conn.hexists("utenti", nome_utente):
        print("Utente non registrato. Effettuare la registrazione prima di effettuare il login.")
        return None

    stored_password = redis_conn.hget("utenti", nome_utente).decode()
    if password == stored_password:
        print("Login effettuato con successo.")
        return nome_utente
    else:
        print("Password errata. Riprova.")
        return None

def registrazione_utente(redis_conn):
    nome_utente = input("Inserisci il nome utente: ")
    password = input("Inserisci la password: ")

    if redis_conn.hexists("utenti", nome_utente):
        print("Nome utente già registrato. Scegliere un altro nome utente.")
        return False

    redis_conn.hset("utenti", nome_utente, password)
    print("Registrazione completata con successo.")
    return True

def ricerca_utenti2(redis_conn, nome_utente_parziale):
    utenti_trovati = []
    for utente in redis_conn.hkeys("utenti"):
        if nome_utente_parziale.lower() in utente.decode().lower():
            utenti_trovati.append(utente.decode())
    return utenti_trovati

def ricerca_utenti(redis_conn):
    nome_utente_parziale = input("Inserisci il nome utente da cercare (anche parziale): ")
    utenti_trovati = ricerca_utenti2(redis_conn, nome_utente_parziale)

    if utenti_trovati:
        print("Utenti trovati:", utenti_trovati)
    else:
        print("Nessun utente trovato.")

def aggiungi_contatto(redis_conn, utente_corrente):
    nome_contatto = input("Inserisci il nome utente da aggiungere alla tua lista contatti: ")

    if nome_contatto == utente_corrente:
        print("Non puoi aggiungere te stesso alla lista contatti.")
        return

    lista_contatti = redis_conn.hget("lista_contatti", utente_corrente)
    if lista_contatti and nome_contatto in lista_contatti.decode().split(','):
        print(f"{nome_contatto} è già presente nella tua lista contatti.")
        return

    if not redis_conn.hexists("utenti", nome_contatto):
        print(f"L'utente {nome_contatto} non esiste.")
        return

    if lista_contatti:
        lista_contatti = f"{lista_contatti.decode()},{nome_contatto}"
    else:
        lista_contatti = nome_contatto

    redis_conn.hset("lista_contatti", utente_corrente, lista_contatti)
    print(f"{nome_contatto} aggiunto alla lista contatti.")

def menu_aggiungi_contatto(redis_conn, utente_corrente):
    while True:
        print("\nMenù Aggiunta Contatto:")
        print("1. Aggiungi un utente alla tua lista contatti")
        print("2. Torna al Menù principale")

        scelta_aggiunta_contatto = input("Seleziona un'opzione (1/2): ")

        if scelta_aggiunta_contatto == '1':
            aggiungi_contatto(redis_conn, utente_corrente)

            lista_contatti_aggiornata = redis_conn.hget("lista_contatti", utente_corrente)
            if lista_contatti_aggiornata:
                print(f"Lista Contatti Aggiornata: {lista_contatti_aggiornata.decode()}")
            else:
                print("Lista Contatti Aggiornata: vuota")

        elif scelta_aggiunta_contatto == '2':
            break
        else:
            print("Scelta non valida. Riprova.")

def dnd_attivo(redis_conn, utente_corrente):
    return redis_conn.hexists("dnd", utente_corrente)

def attiva_disattiva_dnd(redis_conn, utente_corrente):
    stato_attuale = dnd_attivo(redis_conn, utente_corrente)

    if stato_attuale:
        redis_conn.hdel("dnd", utente_corrente)
        print("Modalità 'Do Not Disturb' disattivata.")
    else:
        redis_conn.hset("dnd", utente_corrente, "attivato")
        print("Modalità 'Do Not Disturb' attivata.")

def invia_messaggio(redis_conn, mittente, destinatario, testo):
    lista_contatti = redis_conn.hget("lista_contatti", mittente)
    if lista_contatti and destinatario not in lista_contatti.decode().split(','):
        print(f"Impossibile inviare messaggi a {destinatario}. Non è presente nella tua lista contatti.")
        return

    if dnd_attivo(redis_conn, destinatario):
        print(f"Impossibile inviare messaggi a {destinatario}. La modalità 'Do Not Disturb' è attiva.")
        return
    istante_invio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    messaggio = f"{mittente}: {testo} [{istante_invio}]"

    chiave_mittente = f"chat:{mittente}:{destinatario}"
    chiave_destinatario = f"chat:{destinatario}:{mittente}"

    redis_conn.rpush(chiave_mittente, messaggio)
    redis_conn.rpush(chiave_destinatario, messaggio)
    print(f"Messaggio inviato a {destinatario}: {testo} [{istante_invio}]")

def leggi_chat(redis_conn, utente_corrente, destinatario):
    chiave_chat = f"chat:{utente_corrente}:{destinatario}"

    lista_messaggi = redis_conn.lrange(chiave_chat, 0, -1)

    print(f"\n>> Chat con {destinatario} <<")

    lista_messaggi.sort(key=lambda x: x.decode().split("[")[1])

    for messaggio in lista_messaggi:
        messaggio_decodificato = messaggio.decode()
        prefisso = ">" if messaggio_decodificato.startswith(f"{utente_corrente}:") else "<"

        dati_messaggio = messaggio_decodificato.split("[")
        testo_messaggio = dati_messaggio[0].strip()
        data_istante_invio = dati_messaggio[1].strip("]")

        print(f"{prefisso} {testo_messaggio}\t[{data_istante_invio}]")

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

def esegui_login(connessione_redis):
    utente_corrente = None
    while utente_corrente is None:
        utente_corrente = login_utente(connessione_redis)
    menu_dopo_login(connessione_redis, utente_corrente)

def menu_dopo_login(connessione_redis, utente_corrente):
    chat_tempo_attiva = False
    chiave_chat_tempo = None

    while True:
        print("\nMenù principale:")
        print("1. Ricerca utenti")
        print("2. Aggiungi un utente alla tua lista contatti")
        print("3. Modalità Do Not Disturb")
        print("4. Scrivi messaggio")
        print("5. leggi chat")
        print("6. Torna al Menù Iniziale")

        scelta_dopo_login = input("Seleziona un'opzione (1/2/3/4/5/6/7): ")

        gestisci_scelta_dopo_login(scelta_dopo_login, connessione_redis, utente_corrente, chat_tempo_attiva,
                                   chiave_chat_tempo)

        if scelta_dopo_login == '8':
            break

def gestisci_dnd(connessione_redis, utente_corrente):
    while True:
        stato_attuale_dnd = "Attiva" if dnd_attivo(connessione_redis, utente_corrente) else "Disattiva"
        print(f"\nMenù Modalità Do Not Disturb:")
        print(f"1. Stato attuale: {stato_attuale_dnd}")
        print("2. Attiva/Disattiva Modalità Do Not Disturb")
        print("3. Torna al Menù principale")

        scelta_dnd = input("Seleziona un'opzione (1/2/3): ")

        if scelta_dnd == '1':
            print(f"Stato attuale: {stato_attuale_dnd}")
        elif scelta_dnd == '2':
            attiva_disattiva_dnd(connessione_redis, utente_corrente)
            print("Modalità Do Not Disturb attivata/disattivata.")
        elif scelta_dnd == '3':
            break
        else:
            print("Scelta non valida. Riprova.")

def gestisci_scelta_dopo_login(scelta_dopo_login, connessione_redis, utente_corrente, chat_tempo_attiva, chiave_chat_tempo):
    if scelta_dopo_login == '1':
        ricerca_utenti(connessione_redis)
    elif scelta_dopo_login == '2':
        menu_aggiungi_contatto(connessione_redis, utente_corrente)
    elif scelta_dopo_login == '3':
        gestisci_dnd(connessione_redis, utente_corrente)
    elif scelta_dopo_login == '4':
        destinatario = input("Inserisci il nome utente del destinatario: ")
        testo = input("Inserisci il testo del messaggio: ")
        invia_messaggio(connessione_redis, utente_corrente, destinatario, testo)
    elif scelta_dopo_login == '5':
        destinatario = input("Inserisci il nome utente del destinatario: ")
        leggi_chat(connessione_redis, utente_corrente, destinatario)
    elif scelta_dopo_login == '6':
        menu_iniziale(connessione_redis)
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
