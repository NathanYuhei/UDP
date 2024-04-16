import hashlib
import socket

PACKET_LOSS = False
FILE = ''
HOST = '127.0.0.1'
PORT = 1234
BUFFER = 1040

def checksum(checksum_data):
    checksum = checksum_data[:16] # pq 16
    data = checksum_data[16:]
    novoChecksum = hashlib.md5(data).digest()

    return checksum == novoChecksum


bytes = str.encode('GET/ ' + FILE)
receivedFile = ''
newFile = 'receivedFile.txt'
packets = 0

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.sendto(bytes, (HOST, PORT))

while True:
    checksum_data, address = clientSocket.recvfrom(BUFFER)

    if not checksum_data:
        print('Arquivo finalizado!')
        break
    if checksum_data.startswith('ERROR'.encode('utf-8')):
        print(checksum_data.decode('utf-8'))
        exit()

    packets += 1

    if checksum(checksum_data):
        receivedFile += checksum_data[16:].decode('utf-8')
        print(f'Pacote {packets} enviado!')
        check = 'OK'.encode('utf-8')
    else:
        print(f'Erro de checksum no pacote {packets}. Uma parte do arquivo foi perdida.\nRequisitando reenvio.')
        check = 'NOK'.encode('utf-8')

    clientSocket.sendto(check, (HOST, PORT))

print(f'Escrevendo dados no arquivo {newFile}')
with open(newFile, 'w') as file:
    file.write(receivedFile)

print("Finalizado. Fechando conexão com o servidor.")
clientSocket.close()
