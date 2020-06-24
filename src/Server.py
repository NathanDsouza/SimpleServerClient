from socket import *
import sys


def findOpenPort(serverSocket):
    serverSocket.bind(('', 0))
    return serverSocket.getsockname()[1]


def append_to_messages(message, port):
    f = open("serverMessages.txt", "a")
    f.write(str(port) + ": " + message + "\n")
    f.close()


def write_port_to_file(port):
    f = open("server.txt", "w")
    f.write("SERVER_PORT: " + str(port))
    f.close()


def send_past_messages(clientAddress, udpSocket):
    print("fuck")


def create_messages_file():
    f = open("serverMessages.txt", "a")
    f.close()

def get_messages():
    f = open("serverMessages.txt")
    messages = f.readlines()
    f.close()
    return messages

def open_udp(udpSocket, port):
    action, clientAddress = udpSocket.recvfrom(2048)
    allMessages = get_messages()
    for line in allMessages:
        udpSocket.sendto(line.encode(), clientAddress)
    udpSocket.sendto("No MSG".encode(), clientAddress)
    messageToAdd, clientAddress = udpSocket.recvfrom(2048)
    messageDecoded = messageToAdd.decode()
    if messageDecoded != "TERMINATE":
        append_to_messages(messageDecoded, port)
    udpSocket.close()
    return 1 if messageDecoded == "TERMINATE" else 0


if len(sys.argv) != 2:
    print("you silly silly goose, input the req_code")
    quit()

reqCode = sys.argv[1]
serverSocket = socket(AF_INET, SOCK_STREAM)
nPort = findOpenPort(serverSocket)
write_port_to_file(nPort)
create_messages_file()
serverSocket.listen(1)
print("The server is ready to receive")
while True:
    connectionSocket, addr = serverSocket.accept()
    givenCode = connectionSocket.recv(1024).decode()
    if givenCode != reqCode:
        message = "0"
        print("GET OUT OF MA SWAMP")
        connectionSocket.send(message.encode())
    else:
        udpSocket = socket(AF_INET, SOCK_DGRAM)
        rPort = findOpenPort(udpSocket)
        connectionSocket.send(str(rPort).encode())
        if open_udp(udpSocket, rPort) == 1:
            break
print("Closing Server")
connectionSocket.close()
