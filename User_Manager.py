import redis


def login_utente(connessione_redis):
    nome_utente = input("Inserisci il nome utente: ")
    password = input("Inserisci la password: ")

    if not connessione_redis.hexists("utenti", nome_utente):
        print("Utente non registrato. Effettuare la registrazione prima di effettuare il login.")
        return None

    stored_password = connessione_redis.hget("utenti", nome_utente).decode()
    if password == stored_password:
        print("Login effettuato con successo.")
        return nome_utente
    else:
        print("Password errata. Riprova.")
        return None

def registrazione_utente(connessione_redis):
    nome_utente = input("Inserisci il nome utente: ")
    password = input("Inserisci la password: ")

    if connessione_redis.hexists("utenti", nome_utente):
        print("Nome utente già registrato. Scegliere un altro nome utente.")
        return False

    connessione_redis.hset("utenti", nome_utente, password)
    print("Registrazione completata con successo.")
    return True

def ricerca_utenti2(connessione_redis, nome_utente_parziale):
    utenti_trovati = []
    for utente in connessione_redis.hkeys("utenti"):
        if nome_utente_parziale.lower() in utente.decode().lower():
            utenti_trovati.append(utente.decode())
    return utenti_trovati

def ricerca_utenti(connessione_redis):
    nome_utente_parziale = input("Inserisci il nome utente da cercare (anche parziale): ")
    utenti_trovati = ricerca_utenti2(connessione_redis, nome_utente_parziale)

    if utenti_trovati:
        print("Utenti trovati:", utenti_trovati)
    else:
        print("Nessun utente trovato.")

def aggiungi_contatto(connessione_redis, utente_corrente):
    nome_contatto = input("Inserisci il nome utente da aggiungere: ")

    if nome_contatto == utente_corrente:
        print("Non puoi aggiungere te stesso alla lista contatti.")
        return

    lista_contatti = connessione_redis.hget("lista_contatti", utente_corrente)
    if lista_contatti and nome_contatto in lista_contatti.decode().split(','):
        print(f"{nome_contatto} è già presente nella tua lista contatti.")
        return

    if not connessione_redis.hexists("utenti", nome_contatto):
        print(f"L'utente {nome_contatto} non esiste.")
        return

    if lista_contatti:
        lista_contatti = f"{lista_contatti.decode()},{nome_contatto}"
    else:
        lista_contatti = nome_contatto

    connessione_redis.hset("lista_contatti", utente_corrente, lista_contatti)
    print(f"{nome_contatto} aggiunto alla lista contatti.")
import redis

def visualizza_lista_contatti(connessione_redis, utente_corrente):
    # Ottenere il valore corrispondente al field "utente corrente" dall'hash "lista_contatti"
    valore_utente_corrente = connessione_redis.hget('lista_contatti', utente_corrente)

    # Verificare se l'utente ha contatti
    if not valore_utente_corrente:
        print(f"Nessun contatto trovato per l'utente {utente_corrente}.")
        return

    # Visualizzare il valore corrispondente all'utente corrente
    valori = valore_utente_corrente.decode('utf-8').split(',')
    print(f"\nValori per l'utente {utente_corrente}:\n")
    for valore in valori:
        print(valore)

