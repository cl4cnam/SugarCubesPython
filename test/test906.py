from SugarCubes import *

def traiteTexte(v):
	msgs = v['e']
	for msg in msgs:
		print('--> ' + str(msg))

def aggregMin(pList_val):
	return [min(pList_val)]

az = 34

test = Seq(
	Generate('a', 100),
	Generate('a', 7),
	Pause(),
	Generate( 'e', Getval('az', aggregMin) ),
	ActionOn('e', traiteTexte)
)

expected = '''
1 :
2 :
--> 34
3 :
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
