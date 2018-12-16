from SugarCubesLang import *

class ParTest(Par):
	@extends
	def __init__(self):
		self.x = 10
	def dump(self):
		print('--> ' + str(self.x))

@sugarcube
def test():
	ParTest:
		seq:
			print '--> hello'
			action 'dump'

expected = '''
1 :
--> hello
--> 10
2 :
3 :
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
