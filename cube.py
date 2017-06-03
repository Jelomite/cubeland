from OpenGL.GL import *

'''
the base class for the building blocks that will appear on the screen when the game is run.
it's a generic box, everything is customizable.
this class is the parent of all other objects that will be rendered in the game.
'''


class Box(object):
    def __init__(self, x, y, z, xi, yi, zi, color):
        """
        initializing function, it runs every time the class is being called.
        
        :param x: x position
        :param y: y position
        :param z: z position
        :param xi: x vector scale
        :param yi: y vector scale
        :param zi: z vector scale
        :param color: color in rgb 
        """
        self.x = x
        self.y = y
        self.z = z
        self.xi = xi
        self.yi = yi
        self.zi = zi
        self.color = color

    def draw(self):
        """
        the OpenGL instructions so the box will be rendered properly.
        this function draws the object on screen.
        
        :return: 
        """
        vertices = (
            (self.x + self.xi, self.y - self.yi, self.z - self.zi),
            (self.x + self.xi, self.y + self.yi, self.z - self.zi),
            (self.x - self.xi, self.y + self.yi, self.z - self.zi),
            (self.x - self.xi, self.y - self.yi, self.z - self.zi),
            (self.x + self.xi, self.y - self.yi, self.z + self.zi),
            (self.x + self.xi, self.y + self.yi, self.z + self.zi),
            (self.x - self.xi, self.y - self.yi, self.z + self.zi),
            (self.x - self.xi, self.y + self.yi, self.z + self.zi)

        )

        surfaces = (
            (4, 5, 1, 0),  # right
            (3, 2, 7, 6),  # left
            (6, 7, 5, 4),  # front
            (0, 1, 2, 3),  # back
            (1, 5, 7, 2),  # top
            (4, 0, 3, 6)  # bottom
        )

        colors = [
            0.7,  # right
            0.7,  # left
            1,  # front
            0.6,  # back
            0.9,  # top
            0.3  # bottom

        ]

        vao = []
        new_color = []

        # generate color vertex array.
        for color in colors:
            for i in range(4):
                new_color.append(color * self.color[0])
                new_color.append(color * self.color[1])
                new_color.append(color * self.color[2])

        # generate surface vertex array.
        for surface in surfaces:
            for vertex in surface:
                vao.append(vertices[vertex])

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, vao)
        glColorPointer(3, GL_FLOAT, 0, new_color)
        glDrawArrays(GL_QUADS, 0, len(vao))

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)


'''
a cube, it's the same as a box, but all scales are the same.
'''


class Cube(Box):
    # simple cube with coordinates and a scale.
    def __init__(self, cords, i, color):
        """
        initializing function
        :param cords: tuple of the x, y, z coordinates.
        :param i: scale in all three dimensions
        :param color: color of the cube in rgb
        """
        super().__init__(cords[0], cords[1], cords[2], i, i, i, color)


'''
a floor, it's a huge flat plain that is square
'''


class Floor(Box):
    # a squared 2d plane with a coordinates and a scale
    def __init__(self, x, y, z, i, color):
        """
        
        :param x: x coordinate
        :param y: y coordinate
        :param z: z coordinate
        :param i: scale of the plain
        :param color: color in rgb
        """
        super().__init__(x, y, z, i, 0.001, i, color)


'''
wireframed cube with only outlines
'''


class WireCube(Cube):
    # wireframe of a cube
    def __init__(self, coords, i):
        super().__init__(coords, i, None)

    def draw(self):
        """
        draw function for the wireframe.
        :return: 
        """
        vertices = (
            (self.x + self.xi, self.y - self.yi, self.z - self.zi),
            (self.x + self.xi, self.y + self.yi, self.z - self.zi),
            (self.x - self.xi, self.y + self.yi, self.z - self.zi),
            (self.x - self.xi, self.y - self.yi, self.z - self.zi),
            (self.x + self.xi, self.y - self.yi, self.z + self.zi),
            (self.x + self.xi, self.y + self.yi, self.z + self.zi),
            (self.x - self.xi, self.y - self.yi, self.z + self.zi),
            (self.x - self.xi, self.y + self.yi, self.z + self.zi)

        )

        edges = (
            (0, 1),
            (0, 3),
            (0, 4),
            (2, 1),
            (2, 3),
            (2, 7),
            (6, 3),
            (6, 4),
            (6, 7),
            (5, 1),
            (5, 4),
            (5, 7),

        )

        glBegin(GL_LINES)
        glColor3fv((1, 1, 1))

        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()
