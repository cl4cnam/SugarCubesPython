from SugarCubesLang import *

@sugarcube
def test():
	parex 'e':
		branch:
			print '--> start'
			pause
			repeat 10:
				print '--> bip'
		branch:
			generateProg 'e':
				repeat 5:
					print '--> new'

expected = '''
1 :
--> start
2 :
--> bip
--> new
3 :
--> bip
--> new
4 :
--> bip
--> new
5 :
--> bip
--> new
6 :
--> bip
--> new
7 :
--> bip
8 :
--> bip
9 :
--> bip
10 :
--> bip
'''
