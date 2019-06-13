# from SugarCubesUtils import *
from SugarCubesLang import *

def indent(pb_pourStderr, pn_nombreTabSupplementaire):
	import sys, functools
	if pb_pourStderr:
		l_flux = sys.stderr
	else:
		l_flux = sys.stdout
	
	if not hasattr(sys.stdout, 'compteurIndent'):
		sys.stdout.compteurIndent = 0
	sys.stdout.compteurIndent += pn_nombreTabSupplementaire
	
	if not hasattr(sys.stdout, 'save_write'):
		sys.stdout.save_write = l_flux.write
	l_flux.write = functools.partial(writeTab, sys.stdout.save_write, sys.stdout.compteurIndent)

def getTracifiee(pb_pourStderr, pFunc_methode, ps_avant, ps_apres):
	def tempFunc(*args, ps_avant=ps_avant, ps_apres=ps_apres, pb_pourStderr=pb_pourStderr, **kwargs):
		if pb_pourStderr:
			lFunc_print = printErr
		else:
			lFunc_print = print
		ls_selfName = args[0].__class__.__name__
		ps_avant = ps_avant.replace('selfClass', ls_selfName)
		ps_apres = ps_apres.replace('selfClass', ls_selfName)
		
		if ps_avant != '': lFunc_print(ps_avant)
		indent(pb_pourStderr, 1)
		pFunc_methode(*args, **kwargs)
		indent(pb_pourStderr, -1)
		if ps_apres != '': lFunc_print(ps_apres)
	return tempFunc

def tracer(pb_pourStderr, pClass, ps_nomAttribFunc, ps_avant, ps_apres):
	if pb_pourStderr:
		ls_save = 'saveErr_'
	else:
		ls_save = 'save_'
	lFunc_temp = getattr(pClass, ps_nomAttribFunc)
	setattr(   pClass,  ls_save + ps_nomAttribFunc,  lFunc_temp   )
	setattr(   pClass,  ps_nomAttribFunc,  getTracifiee(pb_pourStderr, lFunc_temp, ps_avant, ps_apres)   )

def tracerDebut(pClass, ps_nomAttribFunc):
	tracer(pourStderr, pClass, ps_nomAttribFunc, '[-- (' + pClass.__name__ + ')selfClass.' + ps_nomAttribFunc, '')

def tracerDebutEtFin(pClass, ps_nomAttribFunc):
	tracer(pourStderr, pClass, ps_nomAttribFunc, '[-- (' + pClass.__name__ + ')selfClass.' + ps_nomAttribFunc, '--] (' + pClass.__name__ + ')selfClass.' + ps_nomAttribFunc)

def cancelTracer(pClass, ps_nomAttribFunc):
	if pourStderr:
		ls_save = 'saveErr_'
	else:
		ls_save = 'save_'
	setattr(   pClass,  ps_nomAttribFunc,  getattr(pClass, ls_save + ps_nomAttribFunc)   )

def runTest(ps_fichTest):
	import sys
	import io

	import os.path
	if not os.path.isfile(ps_fichTest):
		# print(ps_fichTest)
		return True
	print(ps_fichTest, end=' : ')
	stdout_save = sys.stdout
	sys.stdout = io.StringIO('')

	# try:
		# pModule_test.init()
	# except AttributeError: pass
	lModule_test = importScPy(ps_fichTest[:-3])
	if hasattr(lModule_test.test, 'processeurIntegre'):
		lModule_test.test()
	else:
		gProcesseur = Processeur()
		gProcesseur.addProgram(lModule_test.test)
		if hasattr(lModule_test, 'maxI'):
			gNombreInstant = lModule_test.maxI
		else:
			gNombreInstant = 10
		for i in range(1, gNombreInstant + 1):
		# for i in range(1, 4):
			if hasattr(lModule_test, 'asyncPre'):
				lModule_test.asyncPre(gProcesseur)
			print(str(gProcesseur.aInstant.an_num + 1) + ' :')
			gProcesseur.doMacroEtape()

	sys.stdout.seek(0)
	resultat = sys.stdout.read()
	sys.stdout = stdout_save

	if resultat == lModule_test.expected.lstrip():
		print('OK')
		return True
	else:
		print('ERREUR')
		# print('-----------------PROGRAMME--------------------')
		# print(gMonde.aProgParallel)
		print('-----------------OBTENU-----------------------')
		print(resultat)
		print('-----------------ATTENDU----------------------')
		print(lModule_test.expected.lstrip())
		print('=============================================================')
		return False

pourStderr = True
# pourStderr = False

for n in range(1000):
# for n in range(3):
	# if n != 244: continue
	# if not n in [223, 244]: continue
	# if not n in [242, 244]: continue
	if not runTest('test/test_L' + str(n) + '.py'): break
	if not runTest('test/test_M' + str(n) + '.py'): break
	if not runTest('test/test_N' + str(n) + '.py'): break
