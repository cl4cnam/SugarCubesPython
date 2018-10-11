from SugarCubes import *

test = Par(
	RepeatForever(
		Await('e'),
		Write('event &e is generated !')
	),
	RepeatForever(
		Pause(5),
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
event &e is generated !
7 :
8 :
9 :
10 :
'''
