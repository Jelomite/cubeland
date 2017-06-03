"""
a new data structure to hold the map
it's basically a python dictionary with a bit more to it. 
"""


class CubeDict:
    def __init__(self):
        self.dict = dict()

    @staticmethod
    def index_gen(cords):
        """
        generates a string for the indexing of the dictionary
        :param cords: coordinates to translate
        :return: 
        """
        x = round(float(cords[0]), 2)
        y = round(float(cords[1]), 2)
        z = round(float(cords[2]), 2)
        return str(x) + '$' + str(y) + '$' + str(z)

    def append(self, cube):
        """
        a function to append the cube to the data structure.
        :type cube: cube.Cube
        :return: 
        """
        index_str = self.index_gen((cube.x, cube.y, cube.z))
        self.dict[index_str] = cube

    def pop(self, cords):
        """
        pop cube from data
        :param cords: the coordinates which we want to remove
        :return: the cube that is popped. if no object in coordinates, return __str__ function
        """

        index_str = self.index_gen(cords)
        try:
            return self.dict.pop(index_str)
        except KeyError:
            return self.__str__()

    def draw(self):
        """
        iterates over the data and draws each cube.
        :return: 
        """
        for key in list(self.dict):
            self.dict[key].draw()

    def __str__(self):
        """
        the data structure string method
        :return: the string of the dict
        """
        return str(self.dict)
