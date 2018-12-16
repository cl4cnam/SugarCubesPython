from SugarCubesLang import *

class SeqTest(Seq):
	@extends
	def __init__(self):
		self.x = 0
	def dump(self):
		print('--> ' + str(self.x))

@sugarcube
def test():
	SeqTest:
		print '--> hello'
		action 'dump'

expected = '''
1 :
--> hello
--> 0
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
