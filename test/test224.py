from SugarCubes import *

class SeqTest(Seq):
	def __init__(self, *pList_Prog):
		super().__init__(*pList_Prog)
		self.x = 0
	def inc(self):
		self.x += 1
	def dump(self):
		print('--> ' + str(self.x))

class SeqTest2(Seq):
	def __init__(self, *pList_Prog):
		super().__init__(*pList_Prog)
		self.x = 0
	def inc(self):
		self.x += 1
	def dump(self):
		print('--> ' + str(self.x))

test = Actor(
	SeqTest(
		Write('--> hello'),
		Repeat(4,
			Action('inc'),
		),
		Action('dump')
	),
	SeqTest(
		Write('--> hello'),
		Repeat(7,
			Action('inc'),
		),
		Action('dump')
	),
)

expected = '''
1 :
--> hello
--> hello
2 :
3 :
4 :
--> 4
5 :
6 :
7 :
--> 7
8 :
9 :
10 :
'''
