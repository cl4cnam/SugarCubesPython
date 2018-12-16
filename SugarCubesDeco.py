from SugarCubes import *

monde = None

def initMonde(pMonde):
	global monde
	monde = pMonde

# Objets actifs (décorateurs)
#----------------------------
def active(pClass):
	class classeComposee(Par, pClass):
		def __init__(self, *args, **kwargs):
			lList_nomMethode = [
				ls_func
				for ls_func in dir(pClass)
				if callable(getattr(pClass, ls_func))
			]
			# printErr(lList_nomMethode)
			lList_nomMethode_on_ = [
				ls_func
				for ls_func in lList_nomMethode
				if ls_func[:4] == '_on_'
			]
			for ls_func in lList_nomMethode_on_:
				# printErr(ls_func[4:])
				setattr(   pClass,   ls_func,   on(ls_func[4:])( getattr(pClass, ls_func) )   )
			# lList_nomMethodeActive = [
				# ls_func
				# for ls_func in dir(pClass)
				# if callable(getattr(pClass, ls_func)) and hasattr(getattr(pClass, ls_func), 'toCallNTimes')
			# ]
			lList_nomMethodeActive = [
				ls_func
				for ls_func in lList_nomMethode
				if hasattr(getattr(pClass, ls_func), 'toCallNTimes')
			]
			lList_methodeActive = [
				getattr(pClass, ls_methActive) for ls_methActive in lList_nomMethodeActive
			]
			lList_prog = [
				Repeat( lFunc_methActive.toCallNTimes, *lFunc_methActive(self) )
				for lFunc_methActive in lList_methodeActive
			]
			Par.__init__(self, *lList_prog)
			pClass.__init__(self, *args, **kwargs)
			global monde
			if monde != None:
				monde.addProgram(self)
		def diffuseInNextInstant(self, ps_typeInfo, p_valInfo=None):
			global monde
			if monde != None:
				monde.generateEvent(ps_typeInfo, p_valInfo)
			else:
				raise RuntimeError('il faut un monde global, pour utiliser self.diffuse')
	return classeComposee

def activeSingle(pClass):
	lClass_nouvelle = active(pClass)
	lInstance = lClass_nouvelle()
	return lClass_nouvelle

def repeat(pn_nombreFois):
	def tempAuto(pMethod):
		pMethod.toCallNTimes = pn_nombreFois
		return pMethod
	return tempAuto

def actionForever(pMethod):
	# method.__self__ == objet sur lequel est la method
	# fonction.__get__(obj) == bound method
	def tempo(self):
		return [ Action(pMethod.__get__(self)) ]
	return repeat(forever)(tempo)

def publicVar(pMethod):
	def tempo(self):
		return [  Diffuse( pMethod.__name__, pMethod.__get__(self) )  ]
	return repeat(forever)(tempo)

def listToOr(pList_s_typeInfo):
	if len(pList_s_typeInfo) == 1:
		return pList_s_typeInfo[0]
	else:
		return Or(*pList_s_typeInfo)

def on(*pList_s_typeInfo):
	def transforme(pMethod):
		def tempo(self):
			def pMethode_transformee(pDictList_valRecue):
				return pMethod(
					self,
					*[
						pDictList_valRecue[ls_typeInfo] if ls_typeInfo in pDictList_valRecue else []
						for ls_typeInfo in pList_s_typeInfo
					]
				)
			return [  ActionOn(listToOr(pList_s_typeInfo), pMethode_transformee)  ]
		return repeat(forever)(tempo)
	return transforme
