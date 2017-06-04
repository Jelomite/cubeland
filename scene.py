import pygame
import math
import numpy
from OpenGL.GL import *
from OpenGL.GLU import *


class Scene(object):
    """
    Scene class is in charge of all the GUI and openGL controls.
    it is here to help with rendering and interacting with the user.
    """

    def __init__(self, w=1920, h=1080, fov=55, fps=60, flags=pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE,
                 debug=False):
        """
        this is the initializing function, it runs when the class is being called.
        :param w: width of window 
        :param h: height of window
        :param fov: field of view
        :param fps: frames per second
        :param flags: flags for pygame
        :param debug: enable or disable debug mode
        """
        pygame.init()
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(not debug)
        if debug:
            w = 680
            h = 480
            self.screen = pygame.display.set_mode((w, h), flags)

        else:
            self.screen = pygame.display.set_mode((w, h), flags | pygame.FULLSCREEN)

        glMatrixMode(GL_PROJECTION)
        gluPerspective(fov, w / h, 0.001, 100000.0)
        glMatrixMode(GL_MODELVIEW)
        self.keys = dict()
        self.mouse = dict()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.look_speed = 0.2
        self.move_speed = 0.1
        self.w = w
        self.h = h
        self.light_pos = [0, 0, 0, 0]
        self.pos = (0, 0, 0)
        self.debug = debug
        self.m = None

    def shading(self, pos):
        """
        handles the shading of the scene using some openGL trickery.
        :param pos: position of the light source.
        :return: 
        """
        glEnable(GL_LIGHTING)
        glShadeModel(GL_FLAT)
        glEnable(GL_COLOR_MATERIAL)
        glMatrixMode(GL_MODELVIEW)

        self.light_pos = pos
        # position is in x, y, z, w format
        # if w is 0 then the light is "directional"
        # otherwise it is "positional"

        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.6, 0.6, 0.6])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.4, 0.4, 0.4])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 0, 1])
        glLightfv(GL_LIGHT0, GL_POSITION, self.light_pos)
        glEnable(GL_LIGHT0)

    def loop(self):
        """
        this function is responsible for updating and controlling the GUI every frame.
        :return: True 
        """
        pygame.display.flip()
        pygame.event.pump()

        self.keys = dict((i, int(v)) for i, v in enumerate(pygame.key.get_pressed()) if i < 305)
        self.mouse = dict((int(i), int(v)) for i, v in enumerate(pygame.mouse.get_pressed()) if i < 6)
        glLightfv(GL_LIGHT0, GL_POSITION, self.light_pos)  # make sure the light stays where it should be
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        self.clock.tick(self.fps)
        return True

    def controls(self, w_key=ord('w'), s_key=ord('s'), a_key=ord('a'), d_key=ord('d'), up_key=32, down_key=304):
        """
        control the camera and translate the rendering as needed to create a realistic first person experience.
        :param w_key: forward key
        :param s_key: backward key
        :param a_key: left key
        :param d_key: right key
        :param up_key: ascend key
        :param down_key: descend key
        :return: 
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # The actual camera setting cycle
        mouse_dx, mouse_dy = pygame.mouse.get_rel()

        buffer = glGetDoublev(GL_MODELVIEW_MATRIX)
        c = -1 * numpy.mat(buffer[:3, :3]) * numpy.mat(buffer[3, :3]).T
        # c is camera center in absolute coordinates,
        self.pos = c
        glTranslate(*c)
        m = buffer.flatten()
        self.m = m
        glRotate(mouse_dx * self.look_speed, m[1], m[5], m[9])
        glRotate(mouse_dy * self.look_speed, m[0], m[4], m[8])

        # compensate roll
        glRotated(-math.atan2(-m[4], m[5]) * 180 / math.pi, m[2], m[6], m[10])
        glTranslate(*(-c))

        # move forward-back or right-left
        # fwd =   0.1 if 'w' is pressed;   -0.1 if 's'
        fwd = self.move_speed * (self.keys[w_key] - self.keys[s_key])
        strafe = self.move_speed * (self.keys[a_key] - self.keys[d_key])
        hover = self.move_speed * (self.keys[down_key] - self.keys[up_key])

        if abs(fwd) or abs(strafe) or abs(hover):
            m = glGetDoublev(GL_MODELVIEW_MATRIX).flatten()
            glTranslate(fwd * m[2], 0, fwd * m[10])
            glTranslate(0, hover * m[5], 0)
            glTranslate(strafe * m[0], 0, strafe * m[8])
