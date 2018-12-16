from SugarCubesLang import *

class SeqTest(Seq):
	@extends
	def __init__(self):
		self.x = 0
	def inc(self):
		self.x += 1
	def dump(self):
		print('--> ' + str(self.x))

@sugarcube
def test():
	paral:
		SeqTest:
			print '--> hello'
			repeat 5:
				action 'inc'
			action 'dump'
		SeqTest:
			print '--> hello'
			repeat 6:
				action 'inc'
			action 'dump'

expected = '''
1 :
--> hello
--> hello
2 :
3 :
4 :
5 :
--> 5
6 :
--> 6
7 :
8 :
9 :
10 :
'''
