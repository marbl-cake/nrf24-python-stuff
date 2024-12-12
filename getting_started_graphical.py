import time
import struct
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
from pyrf24 import RF24, RF24_PA_LOW, RF24_DRIVER, RF24_250KBPS
import threading

# Configurazione del modulo RF24
CSN_PIN = 0
if RF24_DRIVER == "MRAA":
    CE_PIN = 15  # per GPIO22
elif RF24_DRIVER == "wiringPi":
    CE_PIN = 3  # per GPIO22
else:
    CE_PIN = 22
radio = RF24(CE_PIN, CSN_PIN)

# Variabili globali
payload = [0.0]
address = [b"00001", b"00001"]
radio_number = 0  # Imposta 0 o 1 a seconda della radio (modifica a mano)
radio.begin()
radio.open_tx_pipe(address[radio_number])
radio.open_rx_pipe(1, address[not radio_number])
radio.payload_size = struct.calcsize("<f")
radio.setChannel(100)
radio.setDataRate(RF24_250KBPS)

# Creazione della finestra principale
root = tk.Tk()
root.title("RF24 Communication")
root.geometry("800x400")

# Frame per i pulsanti a sinistra
left_frame = tk.Frame(root, width=200, height=400, bg="lightgrey")
left_frame.pack(side="left", fill="y")

# Aggiunta dei pulsanti
def transmit():
    output_text.insert(tk.END, "Starting transmission...\n")
    threading.Thread(target=master, args=(5,)).start()

def receive():
    output_text.insert(tk.END, "Starting reception...\n")
    threading.Thread(target=slave, args=(6,)).start()

def quit_program():
    output_text.insert(tk.END, "Quitting program...\n")
    radio.power = False
    root.quit()

button_transmit = tk.Button(left_frame, text="Transmit", command=transmit)
button_transmit.pack(pady=20)

button_receive = tk.Button(left_frame, text="Receive", command=receive)
button_receive.pack(pady=20)

button_quit = tk.Button(left_frame, text="Quit", command=quit_program)
button_quit.pack(pady=20)

# Frame per l'output a destra (dove era l'immagine, ora c'è un widget Text)
right_frame = tk.Frame(root, width=600, height=400, bg="white")
right_frame.pack(side="right", fill="both", expand=True)

# Widget per mostrare l'output (testo)
output_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=60, height=20)
output_text.pack(padx=20, pady=20)

# Funzione per aggiornare il widget di testo
def update_output(text):
    output_text.insert(tk.END, text + "\n")
    output_text.yview(tk.END)  # Scrolla automaticamente verso il basso

# Funzione per la trasmissione
def master(count: int = 5):
    radio.listen = False
    while count:
        buffer = struct.pack("<f", payload[0])
        start_timer = time.monotonic_ns()
        result = radio.write(buffer)
        end_timer = time.monotonic_ns()
        if not result:
            update_output("Transmission failed or timed out")
        else:
            update_output(f"Transmission successful! Sent: {payload[0]}")
            payload[0] += 0.01
        time.sleep(1)
        count -= 1

# Funzione per la ricezione
def slave(timeout: int = 6):
    radio.listen = True
    start = time.monotonic()
    while (time.monotonic() - start) < timeout:
        has_payload, pipe_number = radio.available_pipe()
        if has_payload:
            length = radio.payload_size
            received = radio.read(length)
            payload[0] = struct.unpack("<f", received[:4])[0]
            update_output(f"Received: {payload[0]}")
            start = time.monotonic()
    radio.listen = False

# Avvio dell'applicazione
root.mainloop()