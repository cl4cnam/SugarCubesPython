def getGlobalByName(ps_moduleName, ps_name):
	import sys
	lModule = sys.modules[ps_moduleName]
	lGlobal = getattr(lModule, ps_name)
	return lGlobal

def getObjectById(pn_id):
	import ctypes
	return ctypes.cast(pn_id, ctypes.py_object).value

def printErr(ps_texte):
	import sys
	sys.stderr.write(ps_texte + '\n')

def printErrExit(ps_texte):
	import sys
	sys.stderr.write(ps_texte + '\n')
	sys.exit()

def getAvecTab(ps_texte, pn_nombreTab):
	TAB='\t'
	# TAB='    '
	# TAB='..'
	ps_texte = TAB*pn_nombreTab + ps_texte
	ls_newlineALaFin = '\n' if ps_texte[-1] == '\n' else ''
	if ps_texte[-1] == '\n': ps_texte = ps_texte[:-1]
	ps_texte = ps_texte.replace('\n', '\n' + TAB*pn_nombreTab)
	return ps_texte + ls_newlineALaFin

def writeTab(pFunc_write, pn_nombreTab, ps_texte):
	ps_texte = getAvecTab(ps_texte, pn_nombreTab)
	pFunc_write(ps_texte)

def setParent(pList_children, p_parent):
	for child in pList_children:
		try:
			child.a_parent = p_parent
		except AttributeError:
			pass