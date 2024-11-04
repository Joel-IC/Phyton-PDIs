import psutil

def conexiones_por_puerto(puerto):
    # Obtener todas las conexiones de red
    conexiones_red = psutil.net_connections()

    # Filtrar las conexiones que tienen el puerto especificado como puerto local o remoto
    conexiones_por_puerto = [conexion for conexion in conexiones_red if conexion.laddr.port == puerto or (conexion.raddr and conexion.raddr.port == puerto)]

    # Imprimir detalles de las conexiones asociadas al puerto
    for conexion in conexiones_por_puerto:
        print("PID:", conexion.pid)
        print("Familia de dirección:", conexion.family)
        print("Tipo de socket:", conexion.type)
        print("Dirección local:", conexion.laddr)
        print("Dirección remota:", conexion.raddr)
        print("Estado:", conexion.status)
        print("--------------------------------------")

# Especifica el número de puerto para buscar conexiones asociadas
puerto = 49358  # Cambia este número al puerto que deseas verificar

# Llama a la función para obtener detalles de las conexiones asociadas al puerto especificado
conexiones_por_puerto(puerto)
