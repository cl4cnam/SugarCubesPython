from SugarCubesLang import *

def traiteTexte(v):
	msgs = v['e']
	for msg in msgs:
		print(msg)

@sugarcube
def test():
	a = '--> Hello'
	a = ' : Bonjour !'
	pause
	e = a
	actionOn 'e', traiteTexte

expected = '''
1 :
2 :
--> Hello
 : Bonjour !
3 :
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
