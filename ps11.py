# Problem Set 11: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random
import matplotlib.pyplot as plt
import pylab
from types import *
# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).

        x: a real number indicating the x-coordinate
        y: a real number indicating the y-coordinate
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: integer representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)


# === Problems 1 and 2

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """

    # global variables for flag of clean and dirty tile
    CLEAN = 1
    DIRTY = 0

    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.
        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        assert width > 0 and type(width) is IntType
        assert height > 0 and type(height) is IntType

        self.width = width
        self.height = height
        self.tiles = [([RectangularRoom.DIRTY] * self.width) for i in range(self.height)] 

    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.
        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        tileI = int(self.height - 1 - math.floor(pos.getY())) 
        tileJ = int(math.floor(pos.getX()))
        self.tiles[tileI][tileJ] = RectangularRoom.CLEAN
        

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.tiles[self.height - 1 - n][m] == RectangularRoom.CLEAN

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        count = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.tiles[i][j] == RectangularRoom.CLEAN:
                    count = count + 1
        return count

    def isPercentOfRoomCleaned(self, percentage):
        """
        Return True if percentage specified of room tiles is cleand

        percentage: a float 
        """
        res = False
        if self.getPercentOfRoomCleaned() >= percentage:
            res = True
        return res
    
    def getPercentOfRoomCleaned(self):
        """
        Return percent value of room cleaned

        returns: a float value of percentage
        """
        return float(self.getNumCleanedTiles()) / self.getNumTiles()
    
    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        # random.uniform(a, b), returns a float N(a <= N <= b)
        posX = random.uniform(0, self.width)
        posY = random.uniform(0, self.height)
        return Position(posX, posY)

    def isPositionInRoom(self, pos):
        """
        Return True if POS is inside the room.

        pos: a Position object.
        returns: True if POS is in the room, False otherwise.
        """
        inRoom = False
        x = pos.getX()
        y = pos.getY()
        if x >= 0 and x <= self.width and y >= 0 and y <= self.height:
            inRoom = True
        return inRoom

class BaseRobot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in
    the room.  The robot also has a fixed speed.

    Subclasses of BaseRobot should provide movement strategies by
    implementing updatePositionAndClean(), which simulates a single
    time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified
        room. The robot initially has a random direction d and a
        random position p in the room.

        The direction d is an integer satisfying 0 <= d < 360; it
        specifies an angle in degrees.

        p is a Position object giving the robot's position.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        # random.randint(a, b), returns a integer N(a <= N <= b)
        self.d = random.randint(0, 359)
        self.p = self.room.getRandomPosition()

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.p

    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.d

    def getRobotSpeed(self):
        """
        Return the speed of robot

        returns: a float value of speed of robot
        """
        return self.speed

    def getRoom(self):
        return self.room

    def getRandomDirection(self):
        """
        Return random dirction of robot

        returns: a integer in [0, 360) as an angle degrees
        """
        return random.randint(0, 359)

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.p = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.d = direction


class Robot(BaseRobot):
    """
    A Robot is a BaseRobot with the standard movement strategy.

    At each time-step, a Robot attempts to move in its current
    direction; when it hits a wall, it chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        currentPos = self.getRobotPosition()
        room = self.getRoom()
        room.cleanTileAtPosition(currentPos)
        angle = self.getRobotDirection()
        speed = self.getRobotSpeed()
        newPos = currentPos.getNewPosition(angle, speed)
        while not room.isPositionInRoom(newPos):
            angle = self.getRandomDirection()
            newPos = currentPos.getNewPosition(angle, speed)
        # set new position and direction info
        self.setRobotDirection(angle)
        self.setRobotPosition(newPos)
        

# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type, visualize):
    """
    Runs NUM_TRIALS trials of the simulation and returns a list of
    lists, one per trial. The list for a trial has an element for each
    timestep of that trial, the value of which is the percentage of
    the room that is clean after that timestep. Each trial stops when
    MIN_COVERAGE of the room is clean.
    
    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE,
    each with speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    Visualization is turned on when boolean VISUALIZE is set to True.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    visualize: a boolean (True to turn on visualization)
    """
    import time
    import ps11_visualized

    res = []

    for i in range(num_trials):
        anim = None
        robots = []
        timeStep = 0
        room = RectangularRoom(width, height)
        for j in range(num_robots):
            robots.append(robot_type(room, speed))
        if visualize:
            anim = ps11_visualized.RobotVisualization(num_robots, width, height)
        while not room.isPercentOfRoomCleaned(min_coverage):
            for robot in robots:
                robot.updatePositionAndClean()
            timeStep = timeStep + 1
            if visualize:
                anim.update(room, robots)
        perTrial = []
        perTrial.append(timeStep)
        perTrial.append(room.getPercentOfRoomCleaned())
        res.append(perTrial)
        if visualize:
            anim.done()
    return res    

# === Provided function
def computeMeans(list_of_lists):
    """
    Returns a list as long as the longest list in LIST_OF_LISTS, where
    the value at index i is the average of the values at index i in
    all of LIST_OF_LISTS' lists.

    Lists shorter than the longest list are padded with their final
    value to be the same length.
    """
    # Find length of longest list
    longest = 0
    for lst in list_of_lists:
        if len(lst) > longest:
           longest = len(lst)
    # Get totals
    tots = [0]*(longest)
    for lst in list_of_lists:
        for i in range(longest):
            if i < len(lst):
                tots[i] += lst[i]
            else:
                tots[i] += lst[-1]
    # Convert tots to an array to make averaging across each index easier
    tots = pylab.array(tots)
    # Compute means
    means = tots/float(len(list_of_lists))
    return means


# === Problem 4
def computeMeanTimeStep(list_of_lists):
    """
    Return a average value of time steps took by robot
    
    returns: a Integer of average value of many trials
    """
    length = len(list_of_lists)
    avg = 0
    sum = 0
    for list in list_of_lists:
        sum = sum + list[0]
    avg = int(sum / length)
    return avg

def buildPlot1Data(x_axis_data, y_axis_data, robot_num, speed, width, height, minCoverage, num_trials, Robot, visualize):
    roomArea = width * height
    x_axis_data.append(roomArea)
    sim_res_info_lists = runSimulation(robot_num, speed, width, height, minCoverage, num_trials, Robot, visualize)
    y_axis_data.append(computeMeanTimeStep(sim_res_info_lists))
    
def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on room size.
    """
    minCoverage = 0.75
    speed = 1.0
    visualize = False
    robot_num = 1
    num_trials = 30
    x_axis_data = []
    y_axis_data = []
    # 5 x 5
    width = 5
    height = 5
    for i in range(5):
        width = 5 + i * 5
        height = 5 + i * 5
        buildPlot1Data(x_axis_data, y_axis_data, robot_num, speed, width, height, minCoverage, num_trials, Robot, visualize)
    
    plt.plot(x_axis_data, y_axis_data)
    plt.axis([0, 625, 0, 1000])
    plt.xlabel("Room Area")
    plt.ylabel("Timesteps")
    plt.title(("Time to clean %d%% of a square room with %d robots, for various room sizes") % (int(minCoverage * 100), robot_num))
    plt.show()
    
def buildPlot2Data(x_axis_data, y_axis_data, robot_num, speed, width, height, minCoverage, num_trials, Robot, visualize):
    x_axis_data.append(robot_num)
    sim_res_info_lists = runSimulation(robot_num, speed, width, height, minCoverage, num_trials, Robot, visualize)
    y_axis_data.append(computeMeanTimeStep(sim_res_info_lists))
    
def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    minCoverage = 0.75
    speed = 1.0
    visualize = False
    num_trials = 30
    x_axis_data = []
    y_axis_data = []
    # 25 x 25
    width = 25
    height = 25
    for robot_num in range(1, 11):
        buildPlot2Data(x_axis_data, y_axis_data, robot_num, speed, width, height, minCoverage, num_trials, Robot, visualize)
    
    plt.plot(x_axis_data, y_axis_data)
    plt.axis([0, 10, 0, 1000])
    plt.xlabel("Robot Number")
    plt.ylabel("Timesteps")
    plt.title(("Time to clean %d%% of a square room with various robots, for 25 x 25 room sizes") % (int(minCoverage * 100)))
    plt.show()

def buildPlot3Data(x_axis_data, y_axis_data, robot_num, speed, width, height, minCoverage, num_trials, Robot, visualize):
    x_axis_data.append(float(width) / height)
    sim_res_info_lists = runSimulation(robot_num, speed, width, height, minCoverage, num_trials, Robot, visualize)
    y_axis_data.append(computeMeanTimeStep(sim_res_info_lists))
    
def showPlot3():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    minCoverage = 0.75
    speed = 1.0
    visualize = False
    num_trials = 30
    x_axis_data = []
    y_axis_data = []
    robot_num = 2
    # 20 x 20
    width = 20
    height = 20
    buildPlot3Data(x_axis_data, y_axis_data, robot_num, speed, width, height, minCoverage, num_trials, Robot, visualize)
    
    # 25 x 16
    width = 25
    height = 16
    buildPlot3Data(x_axis_data, y_axis_data, robot_num, speed, width, height, minCoverage, num_trials, Robot, visualize)
    
    # 40 x 10
    width = 40
    height = 10
    buildPlot3Data(x_axis_data, y_axis_data, robot_num, speed, width, height, minCoverage, num_trials, Robot, visualize)
    
    # 50 x 8
    width = 50
    height = 8
    buildPlot3Data(x_axis_data, y_axis_data, robot_num, speed, width, height, minCoverage, num_trials, Robot, visualize)
    
    # 80 x 5
    width = 80
    height = 5
    buildPlot3Data(x_axis_data, y_axis_data, robot_num, speed, width, height, minCoverage, num_trials, Robot, visualize)
    
    # 100 x 4
    width = 100
    height = 4
    buildPlot3Data(x_axis_data, y_axis_data, robot_num, speed, width, height, minCoverage, num_trials, Robot, visualize)
    
    plt.plot(x_axis_data, y_axis_data)
    plt.axis([0, 30, 0, 500])
    plt.xlabel("Ratio of width to height")
    plt.ylabel("Timesteps")
    plt.title(("Time to clean %d%% of a square room with %d robots, for 400 room sizes with various width and height") % (int(minCoverage * 100), robot_num))
    plt.show()


def buildPlot4Data(x_axis_data, y_axis_data, robot_num, speed, width, height, minCoverage, num_trials, Robot, visualize):
    x_axis_data.append(minCoverage)
    sim_res_info_lists = runSimulation(robot_num, speed, width, height, minCoverage, num_trials, Robot, visualize)
    y_axis_data.append(computeMeanTimeStep(sim_res_info_lists))
    
def showPlot4():
    """
    Produces a plot showing cleaning time vs. percentage cleaned, for
    each of 1-5 robots.
    """
    speed = 1.0
    visualize = False
    num_trials = 30
    
    x_axis_datas = []
    y_axis_datas = []
    # 25 x 25
    width = 25
    height = 25
    for robot_num in range(1, 6):
        per_x_axis_data = []
        per_y_axis_data = []
        for minCoverage in [x * 0.1 for x in range(1, 11, 2)]:
            buildPlot4Data(per_x_axis_data, per_y_axis_data, robot_num, speed, width, height, minCoverage, num_trials, Robot, visualize)
        x_axis_datas.append(per_x_axis_data)
        y_axis_datas.append(per_y_axis_data)
        
    plt.plot(x_axis_datas[0], y_axis_datas[0], "r-", x_axis_datas[1], y_axis_datas[1], "bs",x_axis_datas[2], y_axis_datas[2], "b--", x_axis_datas[3], y_axis_datas[3], "g^", x_axis_datas[4], y_axis_datas[4], "ro")
    plt.axis([0, 1, 0, 1000])
    plt.xlabel("Min Coverage")
    plt.ylabel("Timesteps")
    plt.title("Time to clean various percentage of a 25 x 25 room with various robots")
    plt.show()

# === Problem 5

class RandomWalkRobot(BaseRobot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement
    strategy: it chooses a new direction at random after each
    time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        currentPos = self.getRobotPosition()
        room = self.getRoom()
        room.cleanTileAtPosition(currentPos)
        # random strategy
        angle = self.getRandomDirection()
        speed = self.getRobotSpeed()
        newPos = currentPos.getNewPosition(angle, speed)
        while not room.isPositionInRoom(newPos):
            angle = self.getRandomDirection()
            newPos = currentPos.getNewPosition(angle, speed)
        # set new position and direction info
        self.setRobotDirection(angle)
        self.setRobotPosition(newPos)


# === Problem 6

def showPlot5():
    """
    Produces a plot comparing the two robot strategies.
    """
    minCoverage = 0.75
    speed = 1.0
    visualize = False
    robot_num = 1
    num_trials = 30
    gen_robot_x_axis_data = []
    gen_robot_y_axis_data = []
    
    ran_robot_x_axis_data = []
    ran_robot_y_axis_data = []
    # 5 x 5
    width = 5
    height = 5
    for i in range(5):
        width = 5 + i * 5
        height = 5 + i * 5
        buildPlot1Data(gen_robot_x_axis_data, gen_robot_y_axis_data, robot_num, speed, width, height, minCoverage, num_trials, Robot, visualize)
    
    width = 5
    height = 5
    for i in range(5):
        width = 5 + i * 5
        height = 5 + i * 5
        buildPlot1Data(ran_robot_x_axis_data, ran_robot_y_axis_data, robot_num, speed, width, height, minCoverage, num_trials, RandomWalkRobot, visualize)
    
    plt.plot(gen_robot_x_axis_data, gen_robot_y_axis_data, "r-", ran_robot_x_axis_data, ran_robot_y_axis_data, "b--",)
    plt.axis([0, 625, 0, 3000])
    plt.xlabel("Room Area")
    plt.ylabel("Timesteps")
    plt.title(("Time to clean %d%% of a square room with %d robots, for various room sizes between different robot types") % (int(minCoverage * 100), robot_num))
    plt.show()

# === Main
if __name__ == "__main__":
    #showPlot1()
    #showPlot2()
    #showPlot3()
    #showPlot4()
    showPlot5()
    #runSimulation(1, 1.0, 20, 20, 0.75, 5, RandomWalkRobot, True)
