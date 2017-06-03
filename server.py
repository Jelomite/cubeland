import sys
import socket
from select import select
from pickle import dumps, loads
from cubedict import CubeDict
from cube import Cube

HOST = '192.168.14.96'
SOCKET_LIST = []
RECV_BUFFER = 4096
PORT = 9009

def server():
    # the server itself.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
    cubes = CubeDict()

    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)

    print("server started on port " + str(PORT))

    while True:

        # non blocking input system.
        while sys.stdin in select([sys.stdin], [], [], 0)[0]:
            command = input().split(' ')

            # simple commands
            if command[0] == 'load':
                if len(SOCKET_LIST) < 2:
                    if len(command) > 1:
                        with open('saves/' + command[1], 'rb') as f:
                            cubes = loads(f.read())
                        print('load complete')
                    else:
                        print('invalid arguments')

                else:
                    print('cannot load map, please try again later')
            elif command[0] == 'save':
                # save map
                if len(command) > 1:
                    with open('saves/' + command[1], 'wb') as f:
                        f.write(dumps(cubes))
                    print('save complete')
                else:
                    print('invalid arguments')
            elif command[0] == 'clear':
                if len(SOCKET_LIST) < 2:
                    cubes = CubeDict()
                else:
                    print('cannot clear map, please try again later')

            else:
                print('unkown command "' + command[0] + '"')

        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read, ready_to_write, in_error = select(SOCKET_LIST, [], [], 0)

        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print("Client (%s, %s) connected" % addr)

                broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)
                payload = dumps(cubes)
                sockfd.sendall(payload)

            # a message from a client, not a new connection
            else:
                # process data recieved from client,
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER).decode('utf-8')
                    if data:
                        # there is something in the socket
                        broadcast(server_socket, sock, data)
                        modify_map(data, cubes)
                    else:
                        # remove the socket that's broken
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)

                        # exception
                except:
                    broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                    continue


# broadcast messages to all connected clients
def broadcast(server_socket, sock, message):
    """
    :param server_socket: the socket of the server
    :param sock: the client socket
    :param message: a message that the server will send to all sockets except the client
    :return:
    """
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock:
            try:
                socket.send(str.encode(message))
            except:
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)


def modify_map(data_stream, cubes):
    """
    :param data_stream: the message the client has sent 
    :param cubes: the map object that we will modify
    :return: 
    """
    if data_stream:
        info = data_stream.split('$')
        if len(info) == 4:

            if info[3] == '1':
                cubes.append(Cube(tuple([float(x) for x in info][:-1]), 0.05, (0, 0, 1)))
            if info[3] == '2':
                cubes.pop(tuple([float(x) for x in info][:-1]))


if __name__ == "__main__":
    try:
        sys.exit(server())
    except KeyboardInterrupt:
        print('shutting down')
