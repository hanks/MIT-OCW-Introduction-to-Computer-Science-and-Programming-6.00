# 6.00 Problem Set 9
#
# Name:
# Collaborators:
# Time:

from string import *

class Shape(object):
    def area(self):
        raise Exception("Subclasses should override this method.")

class Square(Shape):
    def __init__(self, h):
        """
        h: length of side of the square
        """
        self.side = float(h)
    def area(self):
        """
        Returns area of the square
        """
        return self.side**2
    def __str__(self):
        return 'Square with side ' + str(self.side)
    def __eq__(self, other):
        """
        Two squares are equal if they have the same dimension.
        other: object to check for equality
        """
        return type(other) == Square and self.side == other.side

class Circle(Shape):
    def __init__(self, radius):
        """
        radius: radius of the circle
        """
        self.radius = float(radius)
    def area(self):
        """
        Returns approximate area of the circle
        """
        return 3.14159*(self.radius**2)
    def __str__(self):
        return 'Circle with radius ' + str(self.radius)
    def __eq__(self, other):
        """
        Two circles are equal if they have the same radius.
        other: object to check for equality
        """
        return type(other) == Circle and self.radius == other.radius

#
# Problem 1: Create the Triangle class
#
## TO DO: Implement the `Triangle` class, which also extends `Shape`.
class Triangle(Shape):
    def __init__(self, base, height):
        """
        base: base of the triangle
        height: height of the triangle
        """
        self.base = base
        self.height = height

    def area(self):
        """
        Returns area of the triangle
        """
        return 0.5 * self.base * self.height

    def __str__(self):
        return "Triangle with base %.1f and height %.1f" % (self.base, self.height)

    def __eq__(self, other):
        """
        Two triangles are equal if they have same base and height
        other: object needed to be checked for equality
        """
        return type(other) == Triangle and self.base == other.base and self.height == other.height
#
# Problem 2: Create the ShapeSet class
#
## TO DO: Fill in the following code skeleton according to the
##    specifications.

class ShapeSet:
    def __init__(self):
        """
        Initialize any needed variables
        """
        self.shapeSet = []

    def addShape(self, sh):
        """
        Add shape sh to the set; no two shapes in the set may be
        identical
        sh: shape to be added
        """
        if (sh not in self.shapeSet):
            self.shapeSet.append(sh)

    def __iter__(self):
        """
        Return an iterator that allows you to iterate over the set of
        shapes, one shape at a time
        """
        return self.shapeSet.__iter__()

    def __str__(self):
        """
        Return the string representation for a set, which consists of
        the string representation of each shape, categorized by type
        (circles, then squares, then triangles)
        """
        shapeIter = self.__iter__()
        res = ""
        for shape in shapeIter:
            res = res + shape.__str__() + "\n"
        return res
        
#
# Problem 3: Find the largest shapes in a ShapeSet
#
def findLargest(shapes):
    """
    Returns A Tuple Containing the elements of ShapeSet with the
       largest area.
    shapes: ShapeSet
    """
    maxArea = 0
    res = []
    for shape in shapes:
        if shape.area() > maxArea:
            maxArea = shape.area()  
    for shape in shapes:
        if shape.area() == maxArea:
            res.append(shape)
    # a usage of creating a tuple
    return tuple(res)

#
# Problem 4: Read shapes from a file into a ShapeSet
#
def readShapesFromFile(filename):
    """
    Retrieves shape information from the given file.
    Creates and returns a ShapeSet with the shapes found.
    filename: string
    """
    ss = ShapeSet()
    shapeInfo = []
    inputFile = open(filename)
    for line in inputFile:
        line = line.strip()
        oneInfoList = line.split(",")
        shapeInfo.append(oneInfoList)
    for info in shapeInfo:
        if info[0] == "circle":
            ss.addShape(Circle(float(info[1])))
        elif info[0] == "square":
            ss.addShape(Square(float(info[1])))
        elif info[0] == "triangle":
            ss.addShape(Triangle(float(info[1]), float(info[2])))
            
    return ss
        
if __name__ == "__main__":
    ss = ShapeSet()
    ss.addShape(Triangle(1.2, 2.5))
    ss.addShape(Triangle(3, 8))
    ss.addShape(Triangle(4, 6))
    ss.addShape(Triangle(1.6, 6.4))
    largest = findLargest(ss)
    for e in largest:
        print e
        
    ssFromFile = readShapesFromFile("shapes.txt")
    print ssFromFile.__str__()

    

