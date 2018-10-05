#
# SugarCubes.py
# Auteur du concept : Jean-Ferdy Susini
# Auteur de l'implémentation python : Claude Lion
# Date création : 04/06/2018
# Copyright : © Claude Lion 2018
#
from SugarCubesUtils import *

# avancements
PAS_FINI_POUR_MACRO_ETAPE = 0
FINI_POUR_MACRO_ETAPE = 1
FIN = 2

forever = -1

class Info:
	def __init__(self, ps_type, p_valeur):
		self.as_type = ps_type
		self.a_valeur = p_valeur
	def isSensor(self):
		return self.as_type == '$'
	def addToDictInfo(self, pDictInfo):
		try:
			pDictInfo[self.as_type]
		except KeyError:
			pDictInfo[self.as_type] = []
		if self.a_valeur != None:
			pDictInfo[self.as_type].append(self.a_valeur)

class Instant:
	def __init__(self, p_instant):
		self.an_num = p_instant.an_num + 1 if isinstance(p_instant, Instant) else 0
		self.aDictInfo_pourInstantSuivant = {}
		try:
			self.aDictInfo_diffusees = p_instant.aDictInfo_pourInstantSuivant
		except AttributeError:
			self.aDictInfo_diffusees = {}
		self.aListFun_actionAtomique = []
		self.aListFun_actionAtomiqueOnConfig = []
	def evalConfig(self, ps_typeInfo__pLiveProgram_boolean):
		try:
			return ps_typeInfo__pLiveProgram_boolean.evaluate()
		except AttributeError:
			return ps_typeInfo__pLiveProgram_boolean in self.aDictInfo_diffusees

class Processeur:
	def __init__(self):
		self.aProgParallel = ProgParallel()
		self.aLiveProgParallel = self.aProgParallel.getLive()
		self.aLiveProgParallel.aProcesseur = self
		self.aInstant = Instant(None)
		self.aDict_configOuString__typesInfoAttendu = {} # clé : id(await), valeur : config
	def generateEvent(self, ps_typeInfo, p_valInfo):
		lDictInfo_suiv = self.aInstant.aDictInfo_pourInstantSuivant
		Info(ps_typeInfo, p_valInfo).addToDictInfo(lDictInfo_suiv)
	def addProgram(self, pProg):
		self.aProgParallel.add(pProg)
		self.aLiveProgParallel.add(pProg.getLive())
	def isThereAwaitToUnblock(self):
		# lInstant = self.aInstant
		lDict_typesInfoAttendu = self.aDict_configOuString__typesInfoAttendu
		return any(
			[
				self.aInstant.evalConfig(lDict_typesInfoAttendu[idInstrAwait])
				for idInstrAwait in lDict_typesInfoAttendu
			]
		)
	def doMacroEtape(self):
		self.aInstant = Instant(self.aInstant)
		# printErr('num instant : ' + str(self.ai_instant))
		self.aLiveProgParallel.setNouvelleMacroEtape()
		while not self.aLiveProgParallel.isFiniPourMacroEtape():
			self.aLiveProgParallel.doMicroEtape()
			if not self.isThereAwaitToUnblock(): break
		self.aLiveProgParallel.doMicroEtapeDeFinDInstant()
		for lFun in self.aInstant.aListFun_actionAtomique:
			lFun()
		lInstant = self.aInstant
		for lFunOnConfig in self.aInstant.aListFun_actionAtomiqueOnConfig:
			if lInstant.evalConfig(lFunOnConfig['config']):
				lFunOnConfig['action'](lInstant.aDictInfo_diffusees)
			else:
				lFunOnConfig['defaut'](lInstant.aDictInfo_diffusees)

class Program: # abstract
	niv_tab = 0
	def __init__(self, *args):
		self.aList_args = list(args)
	def getClassNameLive(self, pClass):
		try:
			return getGlobalByName(__name__, 'Live' + pClass.__name__)
		except AttributeError:
			for lClass_base in pClass.__bases__:
				ls_rep = self.getClassNameLive(lClass_base)
				if ls_rep != None: return ls_rep
	def getLive(self):
		lClass_live = self.getClassNameLive(self.__class__)
		lList_liveArgs = [
			arg.getLive() if isinstance(arg, Program) else arg
			for arg in self.aList_args
		]
		lLiveProg = lClass_live(*lList_liveArgs)
		lLiveProg.aProg = self
		return lLiveProg
	def __str__(self):
		ls_nom = self.__class__.__name__
		if 'Prog' in ls_nom:
			ls_nom = ls_nom[4:]
		ls_debut = ls_nom + '(\n'
		ls_fin = ')'
		ls_milieu = ',\n'.join( [ str(arg) for arg in self.aList_args ] ) + '\n'
		self.__class__.niv_tab += 1
		ls_milieu = getAvecTab(ls_milieu, self.__class__.niv_tab)
		self.__class__.niv_tab -= 1
		return ls_debut + ls_milieu + ls_fin

class LiveProgram: # abstract
	def __init__(self, *args):
		self.ai_avancement = PAS_FINI_POUR_MACRO_ETAPE
		self.aList_args = list(args)
		setParent(args, self)
		self.aFrozenset_eventGenerable = self.getEventGenerable().union(*[
			arg.aFrozenset_eventGenerable
			for arg in self.aList_args
			if isinstance(arg, LiveProgram)
		])
	def getEventGenerable(self):
		return frozenset([])
	def getProcesseur(self):
		try:
			return self.aProcesseur
		except AttributeError:
			return self.a_parent.getProcesseur()
	def setNouvelleMacroEtape(self):
		self.setPlusFiniPourMacroEtape()
		for arg in self.aList_args:
			if isinstance(arg, LiveProgram):
				arg.setNouvelleMacroEtape()
	def isFiniPourMacroEtape(self):
		return self.ai_avancement >= FINI_POUR_MACRO_ETAPE
	def isTerminee(self):
		return self.ai_avancement == FIN
	def setFiniPourMacroEtape(self):
		self.ai_avancement = max(self.ai_avancement, FINI_POUR_MACRO_ETAPE)
	def setPlusFiniPourMacroEtape(self):
		if not self.isTerminee(): self.ai_avancement = PAS_FINI_POUR_MACRO_ETAPE
	def terminer(self):
		self.ai_avancement = FIN
	def doMicroEtape(self):
		if not self.isFiniPourMacroEtape():
			self.doTransition()
	def doMicroEtapeDeFinDInstant(self):
		self.doTransitionFinale()
	def doTransitionFinale(self):
		pass

class ProgExecWithStop(Program): pass
class LiveProgExecWithStop(LiveProgram):
	def __init__(self, p_configEvent, pLiveProg):
		super().__init__(p_configEvent, pLiveProg)
		self.a_configEvent = p_configEvent
		self.aLiveProg = pLiveProg
	def doTransition(self):
		self.aLiveProg.doMicroEtape()
		self.ai_avancement = self.aLiveProg.ai_avancement
	def doTransitionFinale(self):
		lInstant = self.getProcesseur().aInstant
		if lInstant.evalConfig(self.a_configEvent):
			self.terminer()
ExecWithStop = ProgExecWithStop

class ProgNothing(Program): pass
class LiveProgNothing(LiveProgram):
	def __init__(self, *args):
		super().__init__(*args)
		self.terminer()
	def doTransition(self):
		pass
	def doTransitionFinale(self):
		pass
Nothing = ProgNothing

class ProgAnd(Program): pass
class LiveProgAnd(LiveProgram):
	def __init__(self, *args):
		super().__init__(*args)
	def doTransition(self):
		self.terminer()
	def evaluate(self):
		lProcesseur = self.getProcesseur()
		return all([
			lProcesseur.aInstant.evalConfig(arg)
			for arg in self.aList_args
		])
And = ProgAnd

class ProgOr(Program): pass
class LiveProgOr(LiveProgram):
	def __init__(self, *args):
		super().__init__(*args)
	def doTransition(self):
		self.terminer()
	def evaluate(self):
		lProcesseur = self.getProcesseur()
		return any([
			lProcesseur.aInstant.evalConfig(arg)
			for arg in self.aList_args
		])
Or = ProgOr

class ProgDiffuse(Program): pass
class LiveProgDiffuse(LiveProgram):
	def __init__(self, ps_typeInfo, p_valeurInfo=None):
		super().__init__(ps_typeInfo, p_valeurInfo)
		self.as_typeInfo = ps_typeInfo
		self.a_valeurInfo = p_valeurInfo
		if ps_typeInfo[0] == '$': raise TypeError('Les sensors ne peuvent pas être diffusés')
	def doTransition(self):
		lProcesseur = self.getProcesseur()
		lDictInfo_diffusees = lProcesseur.aInstant.aDictInfo_diffusees
		Info(self.as_typeInfo, self.a_valeurInfo).addToDictInfo(lDictInfo_diffusees)
		self.terminer()
Diffuse = ProgDiffuse

class ProgFilter(Program): pass
class LiveProgFilter(LiveProgram):
	def __init__(self, ps_typeSensor, ps_typeInfo, pFunc_filtre):
		super().__init__(ps_typeSensor, ps_typeInfo, pFunc_filtre)
		self.as_typeSensor = ps_typeSensor
		self.as_typeInfo = ps_typeInfo
		self.aFunc_filtre = pFunc_filtre
		if ps_typeSensor[0] != '$': raise TypeError('Seuls les sensors peuvent être filtrés')
		if ps_typeInfo[0] == '$': raise TypeError('Les sensors ne peuvent pas être diffusés')
	def doTransition(self):
		lProcesseur = self.getProcesseur()
		lDictInfo_diffusees = lProcesseur.aInstant.aDictInfo_diffusees
		if self.as_typeSensor in lDictInfo_diffusees:
			l_valRet = self.aFunc_filtre(lDictInfo_diffusees[self.as_typeSensor])
			if l_valRet != None:
				Info(self.as_typeInfo, l_valRet).addToDictInfo(lDictInfo_diffusees)
		# Info(self.as_typeInfo, self.a_valeurInfo).addToDictInfo(lDictInfo_diffusees)
		self.terminer()
Filter = ProgFilter

class ProgAwait(Program): pass
class LiveProgAwait(LiveProgram):
	def __init__(self, p_typesInfoAttendue):
		super().__init__(p_typesInfoAttendue)
		self.a_typesInfoAttendue = p_typesInfoAttendue
	def doTransition(self):
		lProcesseur = self.getProcesseur()
		if lProcesseur.aInstant.evalConfig(self.a_typesInfoAttendue):
			try:
				del lProcesseur.aDict_configOuString__typesInfoAttendu[id(self)]
			except KeyError: pass
			self.terminer()
		else:
			lProcesseur.aDict_configOuString__typesInfoAttendu[id(self)] = self.a_typesInfoAttendue
	def doTransitionFinale(self):
		pass
Await = ProgAwait

class ProgPause(Program): pass
class LiveProgPause(LiveProgram):
	def __init__(self, pn_nombreFois=1):
		super().__init__(pn_nombreFois)
		self.ai_pausesRestantes = pn_nombreFois
		if self.ai_pausesRestantes == 0:
			self.terminer()
	def doTransition(self):
		self.setFiniPourMacroEtape()
		if self.ai_pausesRestantes > 0: self.ai_pausesRestantes -= 1
	def setNouvelleMacroEtape(self):
		if self.ai_pausesRestantes == 0:
			self.terminer()
		else:
			self.setPlusFiniPourMacroEtape()
Pause = ProgPause

class ProgramAtom(Program): pass
class LiveProgramAtom(LiveProgram): # abstract
	def doTransition(self):
		# self.doIt()
		self.getProcesseur().aInstant.aListFun_actionAtomique.append(self.doIt)
		self.terminer()

class ProgAtomPrint(ProgramAtom): pass
class LiveProgAtomPrint(LiveProgramAtom):
	def doIt(self):
		print(self.aList_args[0])
Print = ProgAtomPrint

class ProgAtomAction(ProgramAtom): pass
class LiveProgAtomAction(LiveProgramAtom):
	def doIt(self):
		self.aList_args[0]()
Action = ProgAtomAction

def fonctionVide(pDict_info): pass
class ProgActionOnConfig(Program): pass
class LiveProgActionOnConfig(LiveProgramAtom):
	def doTransition(self):
		try:
			if self.aList_args[2] == None:
				self.aList_args[2] = fonctionVide
		except IndexError:
			self.aList_args.append(fonctionVide)
		self.getProcesseur().aInstant.aListFun_actionAtomiqueOnConfig.append({
			'config': self.aList_args[0],
			'action': self.aList_args[1],
			'defaut': self.aList_args[2]
		})
		self.terminer()
ActionOnConfig = ProgActionOnConfig
ActionOn = ProgActionOnConfig

class ProgParallel(Program):
	def add(self, pProg):
		self.aList_args.append(pProg)
class LiveProgParallel(LiveProgram):
	def add(self, pLiveProg):
		self.aList_args.append(pLiveProg)
		pLiveProg.a_parent = self
	def __str__(self):
		return ' || '.join( [ str(arg) for arg in self.aList_args ] )
	def doTransition(self):
		for l_instr in self.aList_args:
			l_instr.doMicroEtape()
		self.ai_avancement = min(  [ arg.ai_avancement for arg in self.aList_args ]  )
	def doTransitionFinale(self):
		for l_instr in self.aList_args:
			l_instr.doMicroEtapeDeFinDInstant()
		self.ai_avancement = min(  [ arg.ai_avancement for arg in self.aList_args ]  )
ProgPar = ProgParallel
Par = ProgParallel

class LiveProgSeq_(LiveProgram):
	def __init__(self, pTuple_args, *pDefIter_instr, pFunc_getNewIter):
		super().__init__(pTuple_args)
		self.aDefIter_instr = pDefIter_instr
		self.aFunc_getNewIter = pFunc_getNewIter
		self.aIter_instr = self.aFunc_getNewIter(*self.aDefIter_instr)
	def doTransition(self):
		# printErr('trans ' + self.__class__.__name__)
		while True:
			self.aProg_courante.doMicroEtape()
			if not self.aProg_courante.isTerminee():
				self.ai_avancement = self.aProg_courante.ai_avancement
				return
			try:
				self.aProg_courante = next(self.aIter_instr)
			except StopIteration:
				break
		self.terminer()
	def doTransitionFinale(self):
		try:
			self.aProg_courante.doMicroEtapeDeFinDInstant()
			if not self.aProg_courante.isTerminee():
				self.ai_avancement = self.aProg_courante.ai_avancement
		except AttributeError: pass
	def setNouvelleMacroEtape(self):
		# printErr('setNouvelleMacroEtape ' + self.__class__.__name__)
		if not hasattr(self, 'aProg_courante') or self.aProg_courante.isTerminee():
			try:
				self.aProg_courante = next(self.aIter_instr)
			except StopIteration:
				# printErr('deb supp ' + self.__class__.__name__)
				self.terminer()
		self.setPlusFiniPourMacroEtape()
		if hasattr(self, 'aProg_courante'): self.aProg_courante.setNouvelleMacroEtape()

class ProgSequence(Program): pass
class LiveProgSequence(LiveProgram):
	def __new__(cls, *args, **kwargs):
		l_tmpSeq = LiveProgSeq_(args, args, pFunc_getNewIter=iter)
		setParent(args, l_tmpSeq)
		return l_tmpSeq
	def __str__(self):
		return '; '.join( [ str(arg) for arg in self.aList_args ] )
ProgSeq = ProgSequence
Seq = ProgSequence

class ProgLoop(Program): pass
class LiveProgLoop(LiveProgram):
	def __new__(cls, pLiveProgram_corps, pn_nombreFois=1, **kwargs):
		def getNewIter(pLiveProgram_corps, pn_nombreFois):
			def defGener(pLiveProgram_corps, pn_nombreFois):
				if pn_nombreFois == 0: raise StopIteration
				ln_nombreProgDejaFaite = 0
				while True:
					yield pLiveProgram_corps
					ln_nombreProgDejaFaite += 1
					lParent = pLiveProgram_corps.a_parent
					pLiveProgram_corps = pLiveProgram_corps.aProg.getLive()
					pLiveProgram_corps.a_parent = lParent
					pLiveProgram_corps.setNouvelleMacroEtape()
					if ln_nombreProgDejaFaite >= pn_nombreFois*2 - 1 and pn_nombreFois != -1: break
					yield Pause().getLive()
					ln_nombreProgDejaFaite += 1
				raise StopIteration
			return defGener(pLiveProgram_corps, pn_nombreFois)
		l_tmpLoop = LiveProgSeq_(
			(pLiveProgram_corps,),
			pLiveProgram_corps, pn_nombreFois,
			pFunc_getNewIter=getNewIter
		)
		setParent([pLiveProgram_corps], l_tmpLoop)
		return l_tmpLoop
Loop = ProgLoop
Repeat = ProgLoop


# Instruction composée
#---------------------
def DiffuseMulti(ps_typeInfo, p_valInfo, pn_nombreFois):
	return Repeat(Diffuse(ps_typeInfo, p_valInfo), pn_nombreFois)
def ActionOnMulti(p_configEvent, pFun_reaction, pFun_default, pn_nombreFois):
	return Repeat(ActionOn(p_configEvent, pFun_reaction, pFun_default), pn_nombreFois)
def RepeatS(pn_nombreFois, *args):
	return Repeat(   Seq(*args),  pn_nombreFois   )
def KillS(p_configEvent, pProg_killable, pProg_suite):
	return Seq(Kill(p_configEvent, pProg_killable), pProg_suite)

# Alias
#--------
Generate = Diffuse
GenerateM = DiffuseMulti
ActionOnM = ActionOnMulti
Write = Print
Kill = ExecWithStop

# Modélisation Monde, Acteur
#---------------------------
Monde = Processeur
Actor = Par
Processeur.addActor = Processeur.addProgram
