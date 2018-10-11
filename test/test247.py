from SugarCubes import *

test = Test(True,
	Test(True,
		Write('--> ok 2'),
		Write('--> ko 2'),
	),
	Write('--> ko 1')
)

expected = '''
1 :
--> ok 2
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
