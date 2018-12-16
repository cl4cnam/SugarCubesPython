from SugarCubesLang import *

@sugarcube
def test():
	if False:
		print '--> ok'
	else:
		print '--> ko'

expected = '''
1 :
--> ko
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
