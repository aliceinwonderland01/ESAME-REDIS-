import redis

def registrazione_utente(redis_conn, nome_utente, password):
    if redis_conn.hexists("utenti", nome_utente):
        print("Nome utente già registrato. Scegliere un altro nome utente.")
        return False

    redis_conn.hset("utenti", nome_utente, password)
    print("Registrazione completata con successo.")
    return True

def main():
    r = redis.Redis(
        host='redis-15124.c135.eu-central-1-1.ec2.cloud.redislabs.com',
        port=15124,
        password='vZnU3ir0plHo4dvCrSBd3ILtTDJTUDNX'
    )

    nome_utente = input("Inserisci il nome utente: ")
    password = input("Inserisci la password: ")

    registrazione_utente(r, nome_utente, password)

if __name__ == "__main__":
    main()



