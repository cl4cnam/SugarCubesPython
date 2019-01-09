from SugarCubes import *

def traiteTexte(v):
	msgs = v['e']
	for msg in msgs:
		print(msg)

test = Seq(
	Generate('a', '--> Hello'),
	Generate('a', ' : Bonjour !'),
	Pause(),
	Generate( 'e', Getval('a') ),
	ActionOn('e', traiteTexte)
)

expected = '''
1 :
2 :
--> Hello
 : Bonjour !
3 :
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
