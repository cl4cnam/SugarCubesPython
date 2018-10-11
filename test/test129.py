from SugarCubes import *

def traiteTexte(v):
	msgs = v['e']
	for msg in msgs:
		print(msg)

def fun1(v):
	return v[0]

def async(m):
	m.generateEvent('$sens1', "Hello World !")

test = Actor(
	Par(
		RepeatS(forever,
			Await('e'),
			ActionOn('e', traiteTexte),
			Pause(),
		),
		RepeatS(forever,
			Await('$sens1'),
			Filter('$sens1', 'e', fun1),
			Pause(),
		),
	)
)

expected = '''
1 :
Hello World !
2 :
3 :
Hello World !
4 :
5 :
Hello World !
6 :
7 :
Hello World !
8 :
9 :
Hello World !
10 :
'''
