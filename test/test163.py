from SugarCubes import *

def traiteTexte(v):
	msgs = v['e']
	for msg in msgs:
		print(msg)

test = Actor(
	Par(
		ActionOnM('e', traiteTexte, None, 2),
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
Hello World!
3 :
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
