import math
import random
import pygame

class Vector(object):
	""" The basic 2d vector object for directions and things
	"""

	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y

	def getMag(self): #Returns the magnitude of the vector
		return math.sqrt(self.x**2 + self.y**2)

	def norm(self): #Return the unit vector of the vector
		return Vector(self.x/self.getMag(), self.y/self.getMag()) if self.getMag()>0 else Vector(0, 0)

	def add(self, other):
		self.x = self.x + other.x
		self.y = self.y + other.y

	def __add__(self, other):
		return Vector(self.x + other.x, self.y + other.y)

	def sub(self, other):
		self.x = self.x - other.x
		self.y = self.y - other.y

	def __sub__(self, other):
		return Vector(self.x - other.x, self.y - other.y)

	def mul(self, other):
		self.x = self.x * other
		self.y = self.y * other

	def __mul__(self, other): #Multiply Vector by scalar
		return Vector(self.x * other, self.y * other)

	def __str__(self):
		return "vec("+str(self.x)+", "+str(self.y)+")"

class Ball(object):
	""" The basic ball object that the player interacts with
	"""

	def __init__(self, pos = Vector(), vel = Vector(), radius = 2, color = (0, 50, 0), held = False, friction = .8):
		self.pos = pos
		self.vel = vel
		self.radius = radius
		self.color = color
		self.held = held
		self.friction = friction

	def move(self, displayObject):
		self.vel.mul(self.friction)
		width = displayObject.width
		height = displayObject.height
		if self.vel.getMag() < 1:
			self.vel = Vector(0, 0)
			self.friction = .8 #Return to normal friction 
		if self.pos.x < 0:
			self.vel.x = abs(self.vel.x) #Equivalent to inverting the component but a little more robust
			self.pos.x = 0 #Move thing back to border (sometimes it goes so fast that it ends up at like -100)
		if self.pos.x > width:
			self.vel.x = -abs(self.vel.x)
			self.pos.x = width
		if self.pos.y < 0:
			self.vel.y = abs(self.vel.y)
			self.pos.y = 0
		if self.pos.y > height:
			self.vel.y = -abs(self.vel.y)
			self.pos.y = height
		self.pos.add(self.vel)

	def draw(self, screen):
		if not self.held:
			self.color = (255 * self.vel.getMag()/100.0, 50 + 205 * self.vel.getMag()/100.0, 0)
			pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

	def fire(self, dir = Vector()):
		self.friction = .95 #Reduced friction for balls you shoot out
		self.vel = dir * random.randint(60, 100)

	def __str__(self):
		return "Ball at pos: " + str(self.pos) + ", with velocity: " + str(self.vel)

class Player(object):
	""" The player object for keeping track of the player
	"""

	def __init__(self, pos = Vector(), radius = 5, color = (150, 150, 255), suck_radius = 30, pickup_dist = 5, sucking = False, speed = 5):
		self.pos = pos
		self.radius = radius
		self.color = color
		self.suck_radius = suck_radius
		self.pickup_dist = pickup_dist
		self.sucking = sucking
		self.speed = speed

	def draw(self, screen):
		pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

class Enemy(object):
	""" Basic NPC Class
	"""

	def __init__(self, pos = Vector, radius = 5, color = (255, 0, 0), speed = 7):
		self.pos = pos
		self.radius = radius
		self.color = color
		self.speed = speed

	def move(self, direction):
		self.pos.add(direction * self.speed)

	def draw(self, screen):
		pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

	def kill(self):
		newBalls = []
		num_balls = 20
		for i in range(num_balls):
			angle = ((i*360/num_balls) * math.pi) / 180.0
			newBall = Ball(pos = self.pos * 1.0, vel = Vector(math.cos(angle), math.sin(angle)) * 10, friction = .98)
			newBalls.append(newBall)
		return newBalls

	def __str__(self):
		return "Enemy at: " + str(self.pos)

class DisplayObject(object):
	""" For keeping track of stats about the screen
	"""

	def __init__(self, width = 0, height = 0):
		self.width = width
		self.height = height