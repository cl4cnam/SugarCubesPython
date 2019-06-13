from SugarCubes import *

maxI = 20
myCount = 0

def fun1(v):
	return 1

def asyncPre(m):
	global myCount
	myCount += 1
	if myCount == 10:
		m.generateEvent('$sens1', "Hello World !")

test = Actor(
	Seq(
		Write('--> start'),
		Pause(1),
		Kill(Or('e1', 'e2'),
			Kill('e3',
				Par(
					Generate('e4', None, forever),
					ControlS(And('e', 'f'),
						Par(
							Filter('$sens1', 'g', fun1, forever),
							Filter('$sens2', 'g', fun1, forever),
						)
					),
					Seq(
						Await('g'),
						Write('--> g')
					),
					Seq(
						Pause(2),
						Write('--> go'),
						Repeat(forever, Generate('e'), Generate('f'))
					)
				),
				Write('--> fin')
			)
		)
	)
)

expected = '''
1 :
--> start
2 :
3 :
4 :
--> go
5 :
6 :
7 :
8 :
9 :
10 :
--> g
11 :
12 :
13 :
14 :
15 :
16 :
17 :
18 :
19 :
20 :
'''
