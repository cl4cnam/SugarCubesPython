from SugarCubes import *

def traiteTexte(v):
	msgs = v['e']
	for msg in msgs:
		print('--> ' + str(msg))

test = Seq(
	Generate('a', 100),
	Generate('b', 7),
	Pause(),
	Generate( 'e', SubBin(Getval('a'), Getval('b')) ),
	ActionOn('e', traiteTexte)
)

expected = '''
1 :
2 :
--> 93
3 :
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
