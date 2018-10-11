from SugarCubes import *

test = Par(
	RepeatForever(
		Await('e'),
		Write('event &e is generated !')
	),
	RepeatForever(
		Pause(10),
		Generate('e')
	),
)

expected = '''
1 :
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
