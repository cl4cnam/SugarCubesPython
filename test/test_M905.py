from SugarCubesLang import *

def aggregMin(pList_val):
	return [min(pList_val)]

@sugarcube
def test():
	ifRepeat False :
		print '--> ok'

expected = '''
1 :
--> ok
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
