from pyrf24 import RF24, RF24_PA_MAX, RF24_250KBPS

# Inizializza il modulo NRF24L01+
radio = RF24(22, 0)  # Usa i pin 22 (CE) e 0 (CSN) del Raspberry Pi (modifica se necessario)

# Configura il modulo NRF24L01+
if not radio.begin():
    raise OSError("nRF24L01 hardware isn't responding")

address = [b"00001", b"00001"]
radio_number = 0

radio.setPALevel(RF24_PA_MAX)  # Imposta la potenza di trasmissione
radio.setDataRate(RF24_250KBPS)
radio.setChannel(100)  # Imposta il canale (modifica se necessario)
radio.set_auto_ack(False)

# set TX address of RX node into the TX pipe
radio.open_tx_pipe(address[radio_number])  # always uses pipe 0

# set RX address of TX node into an RX pipe
radio.open_rx_pipe(1, address[not radio_number])  # using pipe 1


radio.listen = False  # Avvia l'ascolto

payload = b'12345'

radio.print_pretty_details()

# Ciclo principale
while True:
    radio.write(payload)
