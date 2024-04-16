import socket
import hashlib

PORT = 1234
HOST = '127.0.0.1'
BUFFER = 50

def sendFile(file, address):
    try: # Abre o arquivo em modo binário
        with open(file, 'rb') as file:
            while data := file.read(1024):
                checksum = hashlib.md5(data).digest()

                check = 'NOK'

                while check == 'NOK':
                    serverSocket.sendto(checksum + data, address)
                    check = serverSocket.recvfrom(BUFFER)
                    check = check[0].decode('utf-8')
                    if check == 'NOK':
                        print('NOK recebido. Reenviando parte do arquivo.')
    except FileNotFoundError:
        server_socket.sendto('ERROR File Not Found.'.encode('utf-8'), address)

    print(f'Arquivo {file} enviado em {address}')
    serverSocket.sendto(b'', address)

def getFile(message, address):
    messageUTF = message.decode('utf-8')

    if messageUTF.startswith('GET'):
        file = messageUTF[4:]
        sendFile(file, address)


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind((HOST, PORT))

print(f"Server {HOST}:{PORT}")


while True:
    message, address = serverSocket.recvfrom(BUFFER)
    getFile(message, address)
    serverSocket.sendto(message, address)


