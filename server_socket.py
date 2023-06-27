import socket

HOST = '127.0.0.1'  # Dirección IP del servidor
PORT = 12345  # Puerto utilizado para la comunicación

# Crea un socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asocia el socket al host y puerto especificados
server_socket.bind((HOST, PORT))

# Escucha conexiones entrantes
server_socket.listen()
print('Esperando conexión del cliente...')

# Acepta la conexión entrante del cliente
client_socket, address = server_socket.accept()
print('Cliente conectado:', address)

while True:
    # Recibe los datos del cliente
    data = client_socket.recv(1024).decode()
    if not data:
        break
    print('Mensaje del cliente:', data)

    # Envía una respuesta al cliente
    response = 'Respuesta recibida: ' + data.upper()
    client_socket.sendall(response.encode())

# Cierra la conexión con el cliente
client_socket.close()

# Cierra el socket del servidor
server_socket.close()
