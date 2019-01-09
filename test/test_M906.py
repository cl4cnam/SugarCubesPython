from SugarCubesLang import *

def aggregMin(pList_val):
	return [min(pList_val)]

@sugarcube
def test():
	paral:
		branch:
			i = 0
			pause
			ifRepeat i < 5:
				i = i + 1
		branch:
			pause
			ifRepeat i < 5:
				a = 10 * i
		branch:
			pause(2)
			ifRepeat i < 5:
				print('--> ' + str(a))

expected = '''
1 :
2 :
3 :
--> 0
4 :
--> 10
5 :
--> 20
6 :
--> 30
7 :
--> 40
8 :
9 :
10 :
'''
