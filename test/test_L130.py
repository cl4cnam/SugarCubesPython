from SugarCubesLang import *

myCount = 1
myCount2 = 1

def traiteTexte(v):
	msgs = v['e']
	for msg in msgs:
		print(msg)

def fun1(v):
	global myCount2
	ls_ret = v[0] + '_' + str(myCount2)
	myCount2 += 1
	return ls_ret

def asyncPre(m):
	global myCount
	m.generateEvent('$sens1', "Hello World !" + str(myCount))
	myCount += 1

@sugarcube
def test():
	paral:
		repeat forever:
			await 'e'
			actionOn 'e', traiteTexte
			pause
		repeat forever:
			await '$sens1'
			filter '$sens1', 'e', fun1
			pause

expected = '''
1 :
Hello World !1_1
2 :
3 :
Hello World !3_2
4 :
5 :
Hello World !5_3
6 :
7 :
Hello World !7_4
8 :
9 :
Hello World !9_5
10 :
'''
