from SugarCubesLang import *

def traiteTexte(v):
	msgs = v['e']
	for msg in msgs:
		print('--> ' + str(msg))

def aggregMin(pList_val):
	return [min(pList_val)]

@sugarcube
def test():
	a = 100
	a = 7
	pause
	e = a $ aggregMin
	actionOn 'e', traiteTexte

expected = '''
1 :
2 :
--> 7
3 :
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
