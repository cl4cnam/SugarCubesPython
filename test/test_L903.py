from SugarCubesLang import *

def traiteTexte(v):
	msgs = v['e']
	for msg in msgs:
		print('--> ' + str(msg))

@sugarcube
def test():
	a = 100
	b = 7
	pause
	e = a - b
	actionOn 'e', traiteTexte

expected = '''
1 :
2 :
--> 93
3 :
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
