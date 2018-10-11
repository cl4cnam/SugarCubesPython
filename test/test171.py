from SugarCubes import *

def traiteTexte(v):
	msgs = v['e']
	for msg in msgs:
		print(msg)

test = Actor(
	Par(
		ActionOnM('e', traiteTexte, None, forever),
		RepeatS(20,
			Pause(2),
			Generate('e', "Hello World!"),
		)
	)
)

expected = '''
1 :
2 :
3 :
Hello World!
4 :
5 :
6 :
Hello World!
7 :
8 :
9 :
Hello World!
10 :
'''
