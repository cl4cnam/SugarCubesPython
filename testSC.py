from SugarCubesUtils import *
from SugarCubes import *

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

def runTest(pTest):
	import sys
	import io

	stdout_save = sys.stdout
	sys.stdout = io.StringIO('')

	gEngine = Engine()
	gEngine.add(pTest['program'])
	for i in range(1, 11):
		print(str(gEngine.ai_instant) + ' :')
		gEngine.doMacroEtape()

	sys.stdout.seek(0)
	resultat = sys.stdout.read()
	sys.stdout = stdout_save

	if resultat == pTest['expected'].lstrip():
		print('OK')
		return True
	else:
		print('ERREUR')
		print('-----------------PROGRAMME--------------------')
		print(gEngine.aInstruction_program)
		print('-----------------OBTENU-----------------------')
		print(resultat)
		print('-----------------ATTENDU----------------------')
		print(pTest['expected'].lstrip())
		print('=============================================================')
		return False

pourStderr = True
# pourStderr = False

for n in range(1000):
# for n in range(1, 19):
	import importlib
	try:
		leModuleDeTest = importlib.import_module('test.test' + str(n))
	except ImportError:
		continue
	print('Test num ' + str(n), end=' : ')
	# if n==18:
	# # if n==17:
		# tracerDebutEtFin(LiveInstruction, 'doMicroEtape')
		# tracerDebutEtFin(LiveInstruction, 'setFiniPourMacroEtape')
		# tracerDebutEtFin(LiveInstrPause, 'doTransition')
		# # tracerDebutEtFin(LiveInstrPause, 'setNouvelleMacroEtape')
		# tracerDebutEtFin(LiveInstrSeq_, 'doTransition')
		# # tracerDebutEtFin(LiveLoop, 'doTransition')
		# # # tracer(LivePar, 'doTransition', '<<', '>>')
	if not runTest(leModuleDeTest.test): break
	# if n==17:
		# cancelTracer(LiveInstruction, 'doMicroEtape')
		# cancelTracer(LiveInstruction, 'setFiniPourMacroEtape')
		# cancelTracer(LiveInstrPause, 'doTransition')
		# # tracerDebutEtFin(LiveInstrPause, 'setNouvelleMacroEtape')
		# cancelTracer(LiveInstrSeq_, 'doTransition')
