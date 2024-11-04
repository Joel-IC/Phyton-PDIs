import psutil

def detalles_proceso(pid):
    # Intentar obtener información sobre el proceso con el PID dado
    try:
        proceso = psutil.Process(pid)
        print("Nombre:", proceso.name())
        print("Executable:", proceso.exe())
        print("Directorio de trabajo:", proceso.cwd())
        print("Estado:", proceso.status())
        print("Usuario:", proceso.username())
        print("Tiempo de creación:", proceso.create_time())
        print("Memoria utilizada:", proceso.memory_info().rss)
        print("CPU utilizado:", proceso.cpu_percent(interval=1))
    except psutil.NoSuchProcess:
        print(f"No existe ningún proceso con el PID {pid}")

# Especifica el PID del proceso del que deseas obtener detalles
pid = 4348  # Cambia esto al PID del proceso que deseas inspeccionar

# Llama a la función para obtener detalles del proceso especificado
detalles_proceso(pid)
