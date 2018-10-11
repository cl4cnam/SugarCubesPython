from SugarCubes import *

test = Test(False,
	Test(True,
		Write('--> ok 2'),
		Write('--> ko 2'),
	),
	Write('--> ko 1')
)

expected = '''
1 :
--> ko 1
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
