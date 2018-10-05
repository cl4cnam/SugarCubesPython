from SugarCubes import *

def traiteTexte(v):
	msgs = v['e']
	for msg in msgs:
		print(msg)

test = Actor(
	Par(
		ActionOnM('e', traiteTexte, None, forever),
		RepeatS(5,
			Generate('e', "Hello World !")
		),
		RepeatS(5,
			Pause(0),
			Generate('f', "Bonjour tout le monde !")
		)
	)
)

expected = '''
1 :
Hello World !
2 :
Hello World !
3 :
Hello World !
4 :
Hello World !
5 :
Hello World !
6 :
7 :
8 :
9 :
10 :
'''
