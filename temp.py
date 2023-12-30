import redis

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
    utenti_disponibili = [utente.decode() for utente in redis_conn.hkeys("utenti")]
    if not utenti_disponibili:
        print("Nessun utente disponibile.")
        return

    print("Elenco degli utenti disponibili:")
    for i, utente in enumerate(utenti_disponibili, start=1):
        print(f"{i}. {utente}")

    while True:
        try:
            indice_utente = int(input("Seleziona il numero corrispondente all'utente da aggiungere: "))
            if 1 <= indice_utente <= len(utenti_disponibili):
                nome_contatto = utenti_disponibili[indice_utente - 1]
                break
            else:
                print("Numero non valido. Riprova.")
        except ValueError:
            print("Inserire un numero valido. Riprova.")

    redis_conn.hset("lista_contatti", utente_corrente, nome_contatto)
    print(f"{nome_contatto} aggiunto alla lista contatti.")

def menu_aggiungi_contatto(redis_conn, utente_corrente):

    while True:
        print("\nMenù Aggiunta Contatto:")
        print("1. Visualizza utenti e aggiungi alla lista contatti")
        print("2. Torna al Menù Dopo Login")

        scelta_aggiunta_contatto = input("Seleziona un'opzione (1/2): ")

        if scelta_aggiunta_contatto == '1':
            aggiungi_contatto(redis_conn, utente_corrente)
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

def main():
    r = redis.Redis(
        host='redis-15124.c135.eu-central-1-1.ec2.cloud.redislabs.com',
        port=15124,
        password='vZnU3ir0plHo4dvCrSBd3ILtTDJTUDNX'
    )

    utente_corrente = None

    while True:
        print("\nMenù Iniziale:")
        print("1. Registrazione utente")
        print("2. Login")
        print("3. Esci")

        scelta_iniziale = input("Seleziona un'opzione (1/2/3): ")

        if scelta_iniziale == '1':
            registrazione_utente(r)

        elif scelta_iniziale == '2':
            utente_corrente = login_utente(r)
            if utente_corrente is not None:
                while True:
                    stato_attuale_dnd = "Attiva" if dnd_attivo(r, utente_corrente) else "Disattiva"
                    print("\nMenù Dopo Login:")
                    print(f"0. Modalità Do Not Disturb: {stato_attuale_dnd}")
                    print("1. Ricerca utenti")
                    print("2. Aggiungi un utente alla tua lista contatti")
                    print("3. Attiva/Disattiva Modalità Do Not Disturb")
                    print("4. Torna al Menù Iniziale")

                    scelta_dopo_login = input("Seleziona un'opzione (1/2/3/4): ")

                    if scelta_dopo_login == '1':
                        ricerca_utenti(r)
                    elif scelta_dopo_login == '2':
                        menu_aggiungi_contatto(r, utente_corrente)
                    elif scelta_dopo_login == '0':
                        attiva_disattiva_dnd(r, utente_corrente)
                    elif scelta_dopo_login == '4':
                        break
                    else:
                        print("Scelta non valida. Riprova.")

        elif scelta_iniziale == '3':
            print("Uscita dal programma.")
            break

        else:
            print("Scelta non valida. Riprova.")

if __name__ == "__main__":
    main()