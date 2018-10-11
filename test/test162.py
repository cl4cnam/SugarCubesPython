from SugarCubes import *

def traiteTexte(v):
	msgs = v['e']
	for msg in msgs:
		print(msg)

test = Actor(
	Par(
		ActionOn('e', traiteTexte),
		RepeatS(5,
			Pause(0),
			Generate('e', "Hello World!"),
		)
	)
)

expected = '''
1 :
Hello World!
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
