from SugarCubesLang import *

def traiteTexte(v):
	msgs = v['e']
	for msg in msgs:
		print(msg)

@sugarcube
def test():
	paral:
		actionOn 'e', traiteTexte
		repeat 5:
			pause 0
			generate 'e', "Hello World!"

expected = '''
1 :
Hello World!
2 :
3 :
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
