from SugarCubesLang import *

@sugarcube
def test():
	paral:
		when 'e':
			print '--> f'
			print '--> e'
		seq:
			pause 4
			generate 'e'

test = Actor(
	Par(
		When('e', Write('--> f'), Write('--> e')),
		Seq(Pause(4), Generate('e'))
	)
)

expected = '''
1 :
2 :
--> e
3 :
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
