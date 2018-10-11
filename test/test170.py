from SugarCubes import *

def traiteTexte(v):
	msgs = v['e']
	for msg in msgs:
		print(msg)

test = Actor(
	Par(
		ActionOnM('e', traiteTexte, None, forever),
		RepeatS(20,
			Pause(1),
			Generate('e', "Hello World!"),
		)
	)
)

expected = '''
1 :
2 :
Hello World!
3 :
4 :
Hello World!
5 :
6 :
Hello World!
7 :
8 :
Hello World!
9 :
10 :
Hello World!
'''
