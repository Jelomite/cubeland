from scene import *
from cube import *
import socket
from _thread import *
import sys
import select
from queue import Queue
from pickle import loads


def approx(n):
    """

    :param n: the coordinates of an object .
    :return: the closest coordinates that apply to the world grid. 
    """
    goal = 0.1
    n1 = round(n, 1)
    if n1 + goal - n < goal / 2:
        return round(n1 + goal, 4)
    elif n1 + goal - n > goal * 1.5:
        return round(n1 - goal, 4)
    else:
        return round(n1, 4)


def update(q):
    """
    :param q: the queue that the client uses to communicate with the server
    :return: None
    """
    global payload
    socket_list = [sys.stdin, s]  # Get the list sockets which are readable
    ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])

    while True:
        for sock in ready_to_read:

            if sock == s:
                # incoming message from remote server, s

                data = sock.recv(4096).decode('utf-8')

                if not data:
                    print('\nDisconnected from chat server')
                    sys.exit()
                else:
                    # print data
                    q.put(data)
                    sys.stdout.flush()

            else:
                # user entered a message
                # msg = sys.stdin.readline()
                s.send(str.encode(payload))
                sys.stdout.flush()


def payload_gen(coordinations):
    """
    :param coordinations: the coordinates of an object
    :return: the string that should be sent to server as a payload
    """
    x = round(float(coordinations[0]), 2)
    y = round(float(coordinations[1]), 2)
    z = round(float(coordinations[2]), 2)
    return str(x) + '$' + str(y) + '$' + str(z)


def cords_gen(l):
    """
    :param l: list of strings that the server sent as coordinates
    :return: a universal form of coordinates, a tuple of floats
    """
    return tuple([float(x) for x in l][:-1])

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print('Wrong arguments')
        sys.exit(1)
    else:

        host = sys.argv[1]
        port = sys.argv[2]

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect to remote host
        try:
            s.connect((host, port))
        except:
            print('Unable to connect')
            sys.exit()

        print('Connected to remote host. You can start sending messages')
        sys.stdout.flush()

        scene = Scene(fov=55, flags=pygame.OPENGL | pygame.DOUBLEBUF)
        scene.move_speed = 0.01
        scene.shading([10, 3, 2, 1])

        cubes = loads(s.recv(102400))
        print('received map info', str(type(cubes)))

        objects = [
            Floor(0, -0.05, 0, 2.5, (0.2, 0.2, 0.2)),
            cubes
        ]

        q = Queue()
        cooldown = 0

        start_new_thread(update, (q,))
        while scene.loop():
            # graphics
            for item in objects:
                item.draw()

            scene.controls()
            # wireframe position calculations
            cooldown += 1
            coords = tuple(map(lambda x: approx(float(x)), [pos for pos in scene.pos]))
            coords = [
                coords[0] - approx(scene.m[2] / 3),
                coords[1] - approx(scene.m[6] / 3),
                coords[2] - approx(scene.m[10] / 3)
            ]

            for index, cord in enumerate(coords):
                if cord == 0:
                    coords[index] = 0

            WireCube(coords, 0.05).draw()

            if scene.debug:
                pass

            # get packet from server

            payload = payload_gen(coords)

            # handle events
            if scene.mouse[2] and cooldown > 10:
                cubes.append(Cube(coords, 0.05, (0, 0, 1)))
                cooldown = 0
                payload = payload_gen(coords) + '$1'
                s.sendall(str.encode(payload))

            if scene.mouse[0] and cooldown > 10:
                cubes.pop(tuple([round(x, 2) for x in coords]))
                cooldown = 0
                payload = payload_gen(coords) + '$2'
                s.sendall(str.encode(payload))

            data = None
            try:
                data = q.get(False, 0)
            except:
                pass

            if data:
                info = data.split('$')
                print(data)
                if len(info) == 4:

                    if info[3] == '1':
                        cubes.append(Cube(cords_gen(info), 0.05, (0, 0, 1)))
                    if info[3] == '2':
                        print('attempting to remove' + str(cords_gen(info)), str(cubes.pop(cords_gen(info))))

                    payload = payload_gen(coords)

            if scene.keys[ord('q')]:
                s.sendall(str.encode('quit'))
                break
