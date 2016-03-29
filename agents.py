# -*- coding: utf-8 -*-

class Environment():

	def __init__(self):
		self.State = False

	def Activate(self):
		self.State = True

	def Deactivate(self):
		self.State = False

class Agent():
	
	def __init__(self, env):
		self.Environment = env
		self.name = __dict__
	def add_cond(self, value):
		self.Cond = value
		
	def check(self):
		if self.Environment.State == True:
			return True
	
	def Activate(self):
		if self.check():
			print("Active!")
		else: print(self, "No environment!")


param1 = Environment()
param2 = Environment()

cat = Agent(param1)
param1.Activate()
cat.Activate()
cat.add_cond('b')
