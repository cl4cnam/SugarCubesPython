from SugarCubes import *

test = Par(
	RepeatForever(
		Kill('e',
			Await('e'),
			Write('--> e !')
		)
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
7 :
8 :
9 :
10 :
'''
