from SugarCubes import *

def traiteTexte(v):
	msgs = v['e']
	for msg in msgs:
		print(msg)

test = Seq(
	Generate('a', '--> Hello'),
	Pause(),
	Generate('e', Getval('a')),
	ActionOn('e', traiteTexte)
)

expected = '''
1 :
2 :
--> Hello
3 :
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
