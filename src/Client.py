from socket import *
import sys

def open_udp(port, serverName, message):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.sendto("GET".encode(), (serverName, port))
    pastMessagesEncoded, addr = clientSocket.recvfrom(2048)
    pastMessages = pastMessagesEncoded.decode()
    f = open("client.txt", "a")
    sentence = "r_port: " + str(port) + "\n"
    f.write(sentence)
    print(sentence, end='')

    while pastMessages != "No MSG":
        f.write(pastMessages)
        print(pastMessages, end='')
        pastMessagesEncoded, addr = clientSocket.recvfrom(2048)
        pastMessages = pastMessagesEncoded.decode()

    f.write(pastMessages + "\n\n")
    print(pastMessages)
    f.close()
    clientSocket.sendto(message.encode(), (serverName, port))
    clientSocket.close()

def create_file():
    f = open("client.txt", "w")
    f.close()


def main():
    if len(sys.argv) != 5:
        print("you silly silly goose, <server_address> <n_port> <req_code> message")
        quit()

    serverAddr = sys.argv[1]
    nPort = int(sys.argv[2])
    reqCode = sys.argv[3]
    message = sys.argv[4]

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverAddr, nPort))
    clientSocket.send(reqCode.encode())
    rPort = clientSocket.recv(1024).decode()
    if rPort != "0":
        open_udp(int(rPort), serverAddr, message)
    else:
        print("Invalid req_code")

    exitKey = input("Click any key to exit") #raw_input needed for older python versions
    clientSocket.close()


if __name__ == "__main__":
    main()
