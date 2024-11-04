import os
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
from scapy.all import sniff

# Configura la interfaz de red que deseas monitorear
interface = 'Ethernet'

# Variables para almacenar datos de la gráfica en tiempo real
packet_info = deque(maxlen=30)  # Almacena la información de los últimos # paquetes
time_points = deque(maxlen=30)  # Almacena los puntos temporales correspondientes
port_log = []  # Almacena los puertos vistos durante la captura

# Inicializa la figura
plt.figure()

# Función de callback que se llama para cada paquete capturado
def packet_handler(packet):
    length = len(packet)
    port = getattr(packet, 'sport', 'Unknown')  # Puerto de origen del paquete, o 'Unknown' si no está presente
    packet_info.append((port, length))
    time_points.append(time_points[-1] + 1 if time_points else 0)  # Incrementa el tiempo

    # Agrega el puerto al registro si es nuevo
    if port not in port_log:
        port_log.append(port)

    # Genera una lista de colores para las barras
    colors = np.random.rand(len(packet_info), 3)

    # Limita los datos a las últimas N barras
    if len(packet_info) > 15:
        packet_info.popleft()
        time_points.popleft()

    # Actualiza la gráfica en tiempo real
    plt.clf()  # Borra la gráfica anterior
    bars = plt.bar(time_points, [info[1] for info in packet_info], color=colors, width=0.8)

    # Agrega etiquetas de texto a cada barra
    for bar, info in zip(bars, packet_info):
        port, length = info
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{length} Port: ({port})', ha='center', va='bottom', fontsize=8)

    plt.xlabel('Tiempo', fontsize=12)
    plt.ylabel('Longitud del paquete', fontsize=12)
    plt.title('Tráfico de red en tiempo real', fontsize=14)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()  # Ajusta el diseño para evitar superposiciones
    plt.pause(0.2)  # Pausa para permitir la actualización de la gráfica

# Función para capturar y guardar la figura junto con el registro de puertos y longitudes de paquetes
def capture_and_save():
    filename = "caps/traffic_capture.png"
    log_filename = "caps/port_log.txt"
    try:
        os.makedirs("caps", exist_ok=True)  # Crea la carpeta "caps" si no existe
        plt.savefig(filename)
        with open(log_filename, "w") as f:
            f.write("Puertos vistos durante la captura:\n")
            for port in port_log:
                f.write(f"{port}\n")
            f.write("\nLongitudes de paquetes:\n")
            for port, length in packet_info:
                f.write(f"Port: {port}, Length: {length}\n")
        messagebox.showinfo("Captura guardada", f"La captura y el registro se guardaron correctamente en {filename} y {log_filename}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar la captura y el registro: {str(e)}")

# Crear la ventana principal
root = tk.Tk()
root.title("Captura de tráfico de red")

# Crear el botón de inicio
start_button = tk.Button(root, text="Iniciar Rastreador", command=lambda: sniff(iface=interface, prn=packet_handler, store=0))  # Usa una función lambda para evitar que el sniff se ejecute al cargar el script
start_button.pack(pady=5)

# Crear el botón de captura y guardado
capture_button = tk.Button(root, text="Capturar", command=capture_and_save)
capture_button.pack(pady=5)

root.mainloop()
