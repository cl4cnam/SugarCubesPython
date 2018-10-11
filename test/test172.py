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
			GenerateM('e', "Hello World!", 2),
		)
	)
)

expected = '''
1 :
2 :
Hello World!
3 :
Hello World!
4 :
5 :
Hello World!
6 :
Hello World!
7 :
8 :
Hello World!
9 :
Hello World!
10 :
'''
