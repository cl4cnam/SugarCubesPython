from SugarCubesLang import *

def traiteTexte(v):
	msgs = v['e']
	for msg in msgs:
		print(msg)

@sugarcube(10, printInstant=True)
def test():
	paral:
		repeat forever:
			actionOn 'e', traiteTexte
		repeat 5:
			generate 'e', "Hello World !"
		repeat 5:
			pause 0
			generate 'f', "Bonjour tout le monde !"

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
