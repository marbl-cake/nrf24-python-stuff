import time
from pyrf24 import RF24, RF24_PA_MAX, RF24_250KBPS

# Inizializza il modulo NRF24L01+
radio = RF24(22, 0)  # Usa i pin 22 (CE) e 0 (CSN) del Raspberry Pi (modifica se necessario)

# Configura il modulo NRF24L01+
if not radio.begin():
    raise OSError("nRF24L01 hardware isn't responding")

radio.setPALevel(RF24_PA_MAX)  # Imposta la potenza di trasmissione
radio.setDataRate(RF24_250KBPS)
radio.setChannel(100)  # Imposta il canale (modifica se necessario)
radio.open_rx_pipe(1, b'00001')  # Imposta il pipe di lettura (modifica l'indirizzo se necessario)
radio.listen = True  # Avvia l'ascolto
radio.set_auto_ack(False)

# Variabili per il calcolo dei pacchetti al secondo (pps)
packet_count = 0
start_time = time.time()

radio.print_pretty_details()

print("In attesa di pacchetti...")

last_received_time = time.time()

no_data_timeout = 5

# Ciclo principale
while True:
    if radio.available():
        # Se ci sono pacchetti disponibili, leggi i dati
        if radio.read(6):  # Leggi il pacchetto (32 byte, puoi adattarlo alla tua dimensione del pacchetto)
            packet_count += 1
            last_received_time = time.time()  # Aggiorna il tempo dell'ultimo pacchetto ricevuto
    else:
        # Se non ci sono pacchetti, controlla se è passato troppo tempo senza ricevere
        elapsed_time = time.time() - last_received_time
        if elapsed_time >= no_data_timeout:
            # Se non ricevi pacchetti da 'no_data_timeout' secondi, resetta il conteggio
            if packet_count > 0:
                print(f"Pacchetti ricevuti: {packet_count} pps")
            packet_count = 0  # Resetta il conteggio dei pacchetti
            last_received_time = time.time()  # Aggiorna il tempo per il prossimo controllo

    # Calcola e stampa i pacchetti ricevuti ogni secondo
    elapsed_time = time.time() - start_time
    if elapsed_time >= 1:
        #if packet_count > 0:
        print(f"Pacchetti ricevuti: {packet_count} pps")
        packet_count = 0
        start_time = time.time()  # Resetta il timer per il calcolo dei pps
