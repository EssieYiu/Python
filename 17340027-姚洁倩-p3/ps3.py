# -*- coding: utf-8 -*-
# Problem Set 3: Simulating robots
# Name:
# Collaborators (discussion):
# Time:

import math
import random

import ps3_visualize
import pylab

# For python 2.7:
from ps3_verify_movement27 import test_robot_movement


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_new_position(self, angle, speed):
        old_x, old_y = self.get_x(), self.get_y()
        
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        
        return Position(new_x, new_y)

    def __str__(self):  
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))


# === Problem 1
class RectangularRoom(object):
    def __init__(self, width, height, dirt_amount):
        self.width = int(width)
        self.height = int(height)
        self.dirt_amount = dirt_amount
        self.tiles = []
        for i in range(int(width)):
            li = []
            for j in range(int(height)):
                li.append(dirt_amount)
            self.tiles.append(li)

    def clean_tile_at_position(self, pos, capacity):
        x = math.floor(pos.get_x())
        y = math.floor(pos.get_y())
        #print("x:",x,"y:",y,"room width:",self.width,"height:",self.height)
        if self.tiles[x][y] >= capacity:
            self.tiles[x][y] = self.tiles[x][y] - capacity
        else:
            self.tiles[x][y] = 0

    def is_tile_cleaned(self, m, n):
        if self.tiles[m][n] == 0:
            return True
        return False

    def get_num_cleaned_tiles(self):
        cleaned = 0
        for i in range(self.width):
            for j in range(self.height):
                if self.tiles[i][j] == 0:
                    cleaned = cleaned + 1
        return cleaned

    def is_position_in_room(self, pos):
        if pos.get_x() >= self.width or pos.get_x() < 0:
            return False
        if pos.get_y() >= self.height or pos.get_y() < 0:
            return False
        return True
        
    def get_dirt_amount(self, m, n):
        return self.tiles[m][n]
        
    def get_num_tiles(self):
        # do not change -- implement in subclasses.
        raise NotImplementedError 
        
    def is_position_valid(self, pos):
        # do not change -- implement in subclasses
        raise NotImplementedError         

    def get_random_position(self):
        # do not change -- implement in subclasses
        raise NotImplementedError        


class Robot(object):
    def __init__(self, room, speed, capacity):
        self.room = room
        self.speed = speed
        self.capacity = capacity
        self.direction = random.randint(0,360)
        self.pos = room.get_random_position()


    def get_robot_position(self):
        return self.pos

    def get_robot_direction(self):
        return self.direction

    def set_robot_position(self, position):
        self.pos = position

    def set_robot_direction(self, direction):
        self.direction = direction

    def update_position_and_clean(self):
        # do not change -- implement in subclasses
        raise NotImplementedError

# === Problem 2
class EmptyRoom(RectangularRoom):
    def get_num_tiles(self):
        return self.width*self.height
        
    def is_position_valid(self, pos):
        return self.is_position_in_room(pos)
        
    def get_random_position(self):
        randx = random.randint(0,self.width-1)
        randy = random.randint(0,self.height-1)
        return Position(randx,randy)

class FurnishedRoom(RectangularRoom):
    def __init__(self, width, height, dirt_amount):
        # This __init__ method is implemented for you -- do not change.
        
        # Call the __init__ method for the parent class
        RectangularRoom.__init__(self, width, height, dirt_amount)
        # Adds the data structure to contain the list of furnished tiles
        self.furniture_tiles = []
        
    def add_furniture_to_room(self):
        # This addFurnitureToRoom method is implemented for you. Do not change it.
        furniture_width = random.randint(1, self.width - 1)
        furniture_height = random.randint(1, self.height - 1)

        # Randomly choose bottom left corner of the furniture item.    
        f_bottom_left_x = random.randint(0, self.width - furniture_width)
        f_bottom_left_y = random.randint(0, self.height - furniture_height)

        # Fill list with tuples of furniture tiles.
        for i in range(f_bottom_left_x, f_bottom_left_x + furniture_width):
            for j in range(f_bottom_left_y, f_bottom_left_y + furniture_height):
                self.furniture_tiles.append((i,j))             

    def is_tile_furnished(self, m, n):
        return (m,n) in self.furniture_tiles
        
    def is_position_furnished(self, pos):
        x = math.floor(pos.get_x())
        y = math.floor(pos.get_y())
        return self.is_tile_furnished(x,y)
        
    def is_position_valid(self, pos):
        if not self.is_position_in_room(pos):
            return False
        if self.is_position_furnished(pos):
            return False
        return True
        
    def get_num_tiles(self):
        return self.width*self.height - len(self.furniture_tiles)
        
    def get_random_position(self):
        random.seed(0)
        x = random.randint(0,self.height-1)
        y = random.randint(0,self.width-1)
        while not self.is_position_valid(Position(x,y)):
            x = random.randint(0,self.height-1)
            y = random.randint(0,self.width-1)
        return Position(x,y)

# === Problem 3
class StandardRobot(Robot):
    def update_position_and_clean(self):
        #random.seed(0)
        new_pos = self.pos.get_new_position(self.direction,self.speed)
        if not self.room.is_position_valid(new_pos):
            self.set_robot_direction(random.randint(0,360))
        else:
            self.pos = new_pos
            self.room.clean_tile_at_position(self.pos,self.capacity)
        


# Uncomment this line to see your implementation of StandardRobot in action!
#test_robot_movement(StandardRobot, EmptyRoom)
#test_robot_movement(StandardRobot, FurnishedRoom)

# === Problem 4
class FaultyRobot(Robot):
    p = 0.15

    @staticmethod
    def set_faulty_probability(prob):
        FaultyRobot.p = prob
    
    def gets_faulty(self):
        return random.random() < FaultyRobot.p
    
    def update_position_and_clean(self):
        if self.gets_faulty():
            self.direction = random.randint(0,360)
        else:
            new_pos = self.pos.get_new_position(self.direction,self.speed)
            if not self.room.is_position_valid(new_pos):
                self.direction = random.randint(0,360)
            else:
                self.pos = new_pos
                self.room.clean_tile_at_position(self.pos,self.capacity)

        
    
#test_robot_movement(FaultyRobot, EmptyRoom)

# === Problem 5
def run_simulation(num_robots, speed, capacity, width, height, dirt_amount, min_coverage, num_trials,
                  robot_type):
    total_time = 0
    for k in range(num_trials):
        anim = ps3_visualize.RobotVisualization(num_robots,width,height,0)
        room = EmptyRoom(width,height,dirt_amount)
        robots = []
        for i in range(num_robots):
            robots.append(robot_type(room,speed,capacity))
        coverage = 0
        time_steps = 0
        while coverage < min_coverage:
            time_steps += 1
            for robot in robots:
                robot.update_position_and_clean()
                anim.update(room,robots)
                coverage = float(room.get_num_cleaned_tiles()/room.get_num_tiles())
        total_time += time_steps
        anim.done()
    return total_time/num_trials


#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 5, 5, 3, 1.0, 50, StandardRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.8, 50, StandardRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.9, 50, StandardRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))
print ('avg time steps: ' + str(run_simulation(3, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))

# === Problem 6
#
# ANSWER THE FOLLOWING QUESTIONS:
#
# 1)How does the performance of the two robot types compare when cleaning 80%
#       of a 20x20 room?
#   从图中曲线可见，蓝色曲线总在黄色曲线的下方，
#   可见，对于同样大小、同样清理比率的房间，
#   有着同样清理容量和运行速度的机器人，
#   Standard Robot所需要的时间比Faulty Robot要小，
#   因此Standard Robot的性能比Faulty Robot要好。
#   对于两种机器人来说，机器人总数的增加，能够显著地减少清理房间的时间。
#
# 2) How does the performance of the two robot types compare when two of each
#       robot cleans 80% of rooms with dimensions 
#       10x30, 20x15, 25x12, and 50x6?
#   在第二张图中，不论是什么形状的房间，
#   Standard Robot清理的时间都比Faulty Robot使用的要少得多。
#   对于两种机器人来说，相同面积下，纵横比越高的房间，清理所需要的时间也越长。
#   而对于Faulty Robot来说，这个清理所需时间的增长要比Standard Robot要稍快一些。
#

def show_plot_compare_strategies(title, x_label, y_label):
    """
    Produces a plot comparing the two robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print ("Plotting", num_robots, "robots...")
        times1.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, StandardRobot))
        times2.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, FaultyRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    
def show_plot_room_shape(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300/width
        print ("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, StandardRobot))
        times2.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, FaultyRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

show_plot_compare_strategies('Time to clean 80% of a 20x20 room, for various numbers of robots','Number of robots','Time / steps')
show_plot_room_shape('Time to clean 80% of a 300-tile room for various room shapes','Aspect Ratio', 'Time / steps')
