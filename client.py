import hashlib
import random
import socket
import time

PACKET_LOSS = True
HOST = '127.0.0.1'
PORT = 1234
BUFFER = 1040

LEFT = random.randrange(16, 1024) #Início de um pacote de dados = 16, fim = 1023
RIGHT = random.randrange(LEFT + 1, 1024)

def checksum(checksum_data):
    checksum = checksum_data[:16]
    data = checksum_data[16:]
    new_checksum = hashlib.md5(data).digest()

    return checksum == new_checksum


filename = input('Insira o nome do arquivo + extensão \".txt\"\n')
request = str.encode('GET/' + filename)

receivedFile = ''
newFile = f'receivedFile{str(random.randint(100, 1000))}.txt'
packets = 0

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.sendto(request, (HOST, PORT))

while True:
    checksum_data, address = clientSocket.recvfrom(BUFFER)
   # time.sleep(0.1)
    if not checksum_data:
        print('Arquivo finalizado!')
        break
    if checksum_data.startswith('ERROR'.encode('utf-8')):
        print(checksum_data.decode('utf-8'))
        exit()

    packets += 1

    if PACKET_LOSS and random.randint(1, 4) == 1:
        checksum_data = checksum_data[:16] + checksum_data[16:LEFT] # + checksum_data[LEFT + 1:RIGHT]

    if checksum(checksum_data):
        receivedFile += checksum_data[16:].decode('utf-8')
        print(f'Pacote {packets} recebido!')
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
