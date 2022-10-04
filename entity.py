import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from random import randint


class Entity(object):
    """Any object that inherits from this class will have the basic ability to move around the maze on its own"""
    def __init__(self, node):
        """Initialize class variables"""
        self.name = None
        self.directions = {UP: Vector2(0, -1), DOWN: Vector2(0, 1),
                           LEFT: Vector2(-1, 0), RIGHT: Vector2(1, 0), STOP: Vector2()}
        self.direction = STOP
        self.setSpeed(100)
        self.radius = 10
        self.collideRadius = 5
        self.color = WHITE
        self.node = node
        self.setPosition()
        self.target = node
        self.visible = True
        self.disablePortal = False

    def update(self, dt):
        """Game loop called once per frame of the game"""
        self.position += self.directions[self.direction] * self.speed * dt

        if self.overshotTarget():
            self.node = self.target
            directions = self.validDirections()
            direction = self.randomDirection(directions)
            if not self.disablePortal:
                if self.node.neighbors[PORTAL] is not None:
                    self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            self.setPosition()

    def setPosition(self):
        """Sets the position of the Entity"""
        self.position = self.node.position.copy()

    def validDirection(self, direction):
        """Checks if the pressed key is a valid direction"""
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False

    def getNewTarget(self, direction):
        """Checks if there is a Node in a direction,
        If True move Pacman to that node automatically"""
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node

    def overshotTarget(self):
        """Checks to see if the Entity has overshot the target node he is moving towards"""
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False

    def reverseDirection(self):
        """Allows the Entity to reverse directions at any time"""
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    def oppositeDirection(self, direction):
        """Checks to see if the input direction is the opposite of the Entity's current direction"""
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    def setSpeed(self, speed):
        """Sets the speed of the Entity"""
        self.speed = speed * TILEWIDTH / 16

    def render(self, screen):
        """Draws the Entity onto the screen"""
        if self.visible:
            p = self.position.asInt()
            pygame.draw.circle(screen, self.color, p, self.radius)

    def validDirections(self):
        """Gets a list of valid directions the Entity can move in"""
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.validDirection(key):
                if key != self.direction * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions

    def randomDirection(self, directions):
        """Chooses one of the directions randomly"""
        return directions[randint(0, len(directions)-1)]