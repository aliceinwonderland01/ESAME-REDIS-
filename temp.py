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
                # Dopo il login, mostra il secondo menù
                while True:
                    print("\nMenù Dopo Login:")
                    print("1. Ricerca utenti")
                    print("2. Torna al Menù Iniziale")

                    scelta_dopo_login = input("Seleziona un'opzione (1/2): ")

                    if scelta_dopo_login == '1':
                        ricerca_utenti(r)
                    elif scelta_dopo_login == '2':
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