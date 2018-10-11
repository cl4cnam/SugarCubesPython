from SugarCubes import *

class SeqTest(Seq):
	def __init__(self, *pList_Prog):
		super().__init__(*pList_Prog)
		self.x = 0
	def dump(self):
		print('--> ' + str(self.x))

test = Actor(
	SeqTest(
		Write('--> hello'),
		Action('dump')
	)
)

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
