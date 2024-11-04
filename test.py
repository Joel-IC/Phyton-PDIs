from scapy.all import sniff
import matplotlib.pyplot as plt
from collections import deque
import numpy as np

# Configura la interfaz de red que deseas monitorear
# Asegúrate de reemplazar "eth0" con el nombre de tu propia interfaz de red
interface = 'Ethernet'

# Variables para almacenar datos de la gráfica en tiempo real
packet_info = deque(maxlen=50)  # Almacena la información de los últimos 50 paquetes
time_points = deque(maxlen=50)  # Almacena los puntos temporales correspondientes

# Inicializa la figura
plt.figure()

# Función de callback que se llama para cada paquete capturado
def packet_handler(packet):
    length = len(packet)
    port = getattr(packet, 'sport', 'Unknown')  # Puerto de origen del paquete, o 'Unknown' si no está presente
    packet_info.append((port, length))
    time_points.append(time_points[-1] + 1 if time_points else 0)  # Incrementa el tiempo

    # Genera una lista de colores para las barras
    colors = np.random.rand(len(packet_info), 3)

    # Limita los datos a las últimas 15 barras
    if len(packet_info) > 20:
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
    plt.pause(5.0)  # Pausa para permitir la actualización de la gráfica

# Inicia la captura de paquetes y llama a la función de callback para cada paquete capturado
plt.ion()  # Modo interactivo para la gráfica en tiempo real
sniff(iface=interface, prn=packet_handler, store=0)  # Usa store=0 para no almacenar los paquetes capturados
