from SugarCubesLang import *

def traiteTexte(v):
	msgs = v['e']
	for msg in msgs:
		print(msg)

def fun1(v):
	return "Hello World !"

def asyncPre(m):
	m.generateEvent('$sens1', "Hello World !")

@sugarcube
def test():
	paral:
		actionOn 'e', traiteTexte, None, forever
		repeat 5:
			filter '$sens1', 'e', fun1

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
