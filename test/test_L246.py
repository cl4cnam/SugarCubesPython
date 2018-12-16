from SugarCubesLang import *

@sugarcube
def test():
	if True:
		if False:
			print '--> ok 2'
		else:
			print '--> ko 2'
	else:
		print '--> ko 1'

expected = '''
1 :
--> ko 2
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
