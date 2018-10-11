#
# SugarCubes.py
# Auteur du modèle théorique : Jean-Ferdy Susini
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
		self.aDict_configOuString__typesInfoAttendu = {} # clé : id(await), valeur : config
		self.aDictInfo_pourInstantSuivant = {}
		try:
			self.aDictInfo_diffusees = p_instant.aDictInfo_pourInstantSuivant
		except AttributeError:
			self.aDictInfo_diffusees = {}
		self.aListFun_actionAtomique = []
		self.aListFun_actionAtomiqueOnConfig = []
		self.aDictList_nouvellesBranches = {} # clé : id(par), valeur : listes des nouvelles branches
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
	def generateEvent(self, ps_typeInfo, p_valInfo=None):
		lDictInfo_suiv = self.aInstant.aDictInfo_pourInstantSuivant
		Info(ps_typeInfo, p_valInfo).addToDictInfo(lDictInfo_suiv)
	def addProgram(self, pProg):
		self.aProgParallel.add(pProg)
		self.aLiveProgParallel.add(pProg.getLive())
	def isThereSomethingToUnblock(self):
		lDict_typesInfoAttendu = self.aInstant.aDict_configOuString__typesInfoAttendu
		return any(
			[
				self.aInstant.evalConfig(lDict_typesInfoAttendu[idInstrAwait])
				for idInstrAwait in lDict_typesInfoAttendu
			]
		)
	def doMacroEtape(self):
		# Mise en place nouvelleMacroEtape
		#---------------------------------
		self.aInstant = Instant(self.aInstant)
		# printErr('--> num instant : ' + str(self.aInstant.an_num))
		self.aLiveProgParallel.setNouvelleMacroEtape()
		
		# Exécution normale
		#---------------------------------
		# printErr('--> num (setNouvelleMacroEtape) instant : ' + str(self.aInstant.an_num))
		while not self.aLiveProgParallel.isFiniPourMacroEtape():
			self.aLiveProgParallel.doMicroEtape()
			if not self.isThereSomethingToUnblock(): break
		
		# Exécution spéciale "fin d'instant"
		#-----------------------------------
		# printErr('--> num (fin) instant : ' + str(self.aInstant.an_num))
		self.aLiveProgParallel.doMicroEtapeDeFinDInstant()
		
		# Exécution ActionOnConfig
		#-----------------------------------
		lInstant = self.aInstant
		for lFunOnConfig in self.aInstant.aListFun_actionAtomiqueOnConfig:
			if lInstant.evalConfig(lFunOnConfig['config']):
				lFunOnConfig['action'](lInstant.aDictInfo_diffusees)
			else:
				lFunOnConfig['defaut'](lInstant.aDictInfo_diffusees)
		
		# Exécution Action
		#-----------------------------------
		for lFun in self.aInstant.aListFun_actionAtomique:
			lFun()
		
		# Ajout branches
		#-----------------------------------
		for lLiveParId in lInstant.aDictList_nouvellesBranches:
			for lLiveProg_branche in lInstant.aDictList_nouvellesBranches[lLiveParId]:
				getObjectById(lLiveParId).add(lLiveProg_branche)

class Program: # abstract
	niv_tab = 0
	def __init__(self, *args, **kwargs):
		self.aList_args = list(args)
		self.aDict_kwargs = dict(kwargs)
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
		lLiveProg = lClass_live(*lList_liveArgs, **self.aDict_kwargs)
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
	def getPropriete(self, ps_nomPropriete):
		try:
			return getattr(self.aProg, ps_nomPropriete)
		except AttributeError:
			if not hasattr(self, 'a_parent'):
				printErr('target not found : ' + ps_nomPropriete)
				import sys
				sys.exit()
			return self.a_parent.getPropriete(ps_nomPropriete)
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
	def __init__(self, p_configEvent, pLiveProg, pLiveProg_lastWill=None):
		super().__init__(p_configEvent, pLiveProg, pLiveProg_lastWill)
		self.a_configEvent = p_configEvent
		self.aLiveProg = pLiveProg
		self.aLiveProg_lastWill = pLiveProg_lastWill
		self.ab_killable = True
	def doTransition(self):
		self.aLiveProg.doMicroEtape()
		self.ai_avancement = self.aLiveProg.ai_avancement
	def doTransitionFinale(self):
		self.aLiveProg.doMicroEtapeDeFinDInstant()
		lInstant = self.getProcesseur().aInstant
		if self.ab_killable and lInstant.evalConfig(self.a_configEvent):
			if self.aLiveProg_lastWill != None:
				self.aLiveProg = self.aLiveProg_lastWill
				self.aLiveProg_lastWill = None
				self.ab_killable = False
			else:
				self.terminer()
ExecWithStop = ProgExecWithStop

class ProgWhen(Program): pass
class LiveProgWhen(LiveProgram):
	def __init__(self, p_configEvent, pLiveProg, pLiveProg_else=None):
		super().__init__(p_configEvent, pLiveProg, pLiveProg_else)
		self.a_configEvent = p_configEvent
		self.aLiveProg = pLiveProg
		self.aLiveProg_else = pLiveProg_else
		self.aLiveProg_courant = None
	def doTransition(self):
		if self.aLiveProg_courant == None:
			lInstant = self.getProcesseur().aInstant
			if lInstant.evalConfig(self.a_configEvent):
				try:
					del lInstant.aDict_configOuString__typesInfoAttendu[id(self)]
				except KeyError: pass
				self.aLiveProg_courant = self.aLiveProg
			else:
				lInstant.aDict_configOuString__typesInfoAttendu[id(self)] = self.a_configEvent
		if self.aLiveProg_courant != None:
			self.aLiveProg_courant.doMicroEtape()
			self.ai_avancement = self.aLiveProg_courant.ai_avancement
	def doTransitionFinale(self):
		if self.aLiveProg_courant != None:
			self.aLiveProg_courant.doMicroEtapeDeFinDInstant()
			self.ai_avancement = self.aLiveProg_courant.ai_avancement
		else:
			self.aLiveProg_courant = self.aLiveProg_else
			if self.aLiveProg_else == None:
				self.terminer()
When = ProgWhen

class ProgTest(Program): pass
class LiveProgTest(LiveProgram):
	def __init__(self, p_condition, pLiveProg, pLiveProg_else=None):
		super().__init__(p_condition, pLiveProg, pLiveProg_else)
		self.a_condition = p_condition
		self.aLiveProg = pLiveProg
		self.aLiveProg_else = pLiveProg_else
		self.aLiveProg_courant = None
	def doTransition(self):
		if self.aLiveProg_courant == None:
			if isinstance(self.a_condition, bool):
				lb_condition = self.a_condition
			else:
				lb_condition = self.a_condition()
			if lb_condition:
				self.aLiveProg_courant = self.aLiveProg
			else:
				self.aLiveProg_courant = self.aLiveProg_else
		if self.aLiveProg_courant != None:
			self.aLiveProg_courant.doMicroEtape()
			self.ai_avancement = self.aLiveProg_courant.ai_avancement
		else:
			self.terminer()
Test = ProgTest

class ProgMatch(Program): pass
class LiveProgMatch(LiveProgram):
	def __init__(self, p_condition, *pList_LiveProg):
		super().__init__(p_condition, *pList_LiveProg)
		self.a_condition = p_condition
		self.aList_LiveProg = pList_LiveProg
		self.aLiveProg_courant = None
	def doTransition(self):
		if self.aLiveProg_courant == None:
			if isinstance(self.a_condition, int):
				ln_num = self.a_condition
			else:
				ln_num = getattr(self.a_condition[0], self.a_condition[1], -1)
			try:
				self.aLiveProg_courant = self.aList_LiveProg[ln_num]
			except IndexError: pass
		if self.aLiveProg_courant != None:
			self.aLiveProg_courant.doMicroEtape()
			self.ai_avancement = self.aLiveProg_courant.ai_avancement
		else:
			self.terminer()
Match = ProgMatch

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
		self.aInfo = Info(ps_typeInfo, p_valeurInfo)
		if self.aInfo.isSensor(): raise TypeError('Les sensors ne peuvent pas être diffusés')
	def doTransition(self):
		lProcesseur = self.getProcesseur()
		lDictInfo_diffusees = lProcesseur.aInstant.aDictInfo_diffusees
		self.aInfo.addToDictInfo(lDictInfo_diffusees)
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
		self.terminer()

class ProgAwait(Program): pass
class LiveProgAwait(LiveProgram):
	def __init__(self, p_typesInfoAttendue):
		super().__init__(p_typesInfoAttendue)
		self.a_typesInfoAttendue = p_typesInfoAttendue
	def doTransition(self):
		lProcesseur = self.getProcesseur()
		if lProcesseur.aInstant.evalConfig(self.a_typesInfoAttendue):
			try:
				del lProcesseur.aInstant.aDict_configOuString__typesInfoAttendu[id(self)]
			except KeyError: pass
			self.terminer()
		else:
			lProcesseur.aInstant.aDict_configOuString__typesInfoAttendu[id(self)] = self.a_typesInfoAttendue
	def doTransitionFinale(self):
		pass
Await = ProgAwait

class ProgControl(Program): pass
class LiveProgControl(LiveProgram):
	def __init__(self, p_typesInfoAttendue, pLiveProg):
		super().__init__(p_typesInfoAttendue, pLiveProg)
		self.a_typesInfoAttendue = p_typesInfoAttendue
		self.aLiveProg = pLiveProg
	def doTransition(self):
		lProcesseur = self.getProcesseur()
		if lProcesseur.aInstant.evalConfig(self.a_typesInfoAttendue):
			try:
				del lProcesseur.aInstant.aDict_configOuString__typesInfoAttendu[id(self)]
			except KeyError: pass
			self.aLiveProg.doMicroEtape()
			self.ai_avancement = self.aLiveProg.ai_avancement
		else:
			lProcesseur.aInstant.aDict_configOuString__typesInfoAttendu[id(self)] = self.a_typesInfoAttendue
	def doTransitionFinale(self):
		lProcesseur = self.getProcesseur()
		if lProcesseur.aInstant.evalConfig(self.a_typesInfoAttendue):
			self.aLiveProg.doMicroEtapeDeFinDInstant()
			self.ai_avancement = self.aLiveProg.ai_avancement
Control = ProgControl

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
		if isinstance(self.aList_args[0], str):
			lFun = self.getPropriete(self.aList_args[0])
		else:
			lFun = self.aList_args[0]
		lFun()

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

class ProgParallel(Program):
	def add(self, pProg):
		self.aList_args.append(pProg)
class LiveProgParallel(LiveProgram):
	def __init__(self, *args, channel=None):
		super().__init__(*args)
		self.as_typeInfo_channel = channel
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
		
		if self.as_typeInfo_channel != None:
			lInstant = self.getProcesseur().aInstant
			if self.as_typeInfo_channel in lInstant.aDictInfo_diffusees:
				lDict_nouvBranch = lInstant.aDictList_nouvellesBranches
				try:
					lDict_nouvBranch[id(self)]
				except KeyError:
					lDict_nouvBranch[id(self)] = []
				for lLiveProg in lInstant.aDictInfo_diffusees[self.as_typeInfo_channel]:
					lDict_nouvBranch[id(self)].append(lLiveProg)
				self.ai_avancement = 0
ProgPar = ProgParallel
Par = ProgParallel

class LiveProgSeq_(LiveProgram):
	def __init__(self, pTuple_args, *pDefIter_instr, pFunc_getNewIter):
		super().__init__(pTuple_args)
		self.aIter_instr = pFunc_getNewIter(*pDefIter_instr)
	def doTransition(self):
		while True:
			self.aProg_courante.doMicroEtape()
			if not self.aProg_courante.isTerminee():
				self.ai_avancement = self.aProg_courante.ai_avancement
				return
			try:
				self.aProg_courante = next(self.aIter_instr)
				self.setNouvelleMacroEtape()
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
		if not hasattr(self, 'aProg_courante') or self.aProg_courante.isTerminee():
			try:
				self.aProg_courante = next(self.aIter_instr)
			except StopIteration:
				self.terminer()
		self.setPlusFiniPourMacroEtape()
		if hasattr(self, 'aProg_courante'):
			self.aProg_courante.setNouvelleMacroEtape()

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
	def __new__(cls, pLiveProgram_corps, pn_nombreFois=1, pFunc_cond=None, **kwargs):
		def getNewIter(pLiveProgram_corps, pn_nombreFois):
			if pn_nombreFois == 0: raise StopIteration
			ln_nombreProgDejaFaite = 0
			while True:
				yield pLiveProgram_corps
				ln_nombreProgDejaFaite += 1
				lParent = pLiveProgram_corps.a_parent
				pLiveProgram_corps = pLiveProgram_corps.aProg.getLive()
				pLiveProgram_corps.a_parent = lParent
				pLiveProgram_corps.setNouvelleMacroEtape()
				if pFunc_cond != None:
					if not pFunc_cond(): break
				if ln_nombreProgDejaFaite >= pn_nombreFois*2 - 1 and pn_nombreFois != -1: break
				yield Pause().getLive()
				ln_nombreProgDejaFaite += 1
			raise StopIteration
		l_tmpLoop = LiveProgSeq_(
			(pLiveProgram_corps,),
			pLiveProgram_corps, pn_nombreFois,
			pFunc_getNewIter=getNewIter
		)
		setParent([pLiveProgram_corps], l_tmpLoop)
		return l_tmpLoop
Loop = ProgLoop

# Instruction composée
#---------------------
def DiffuseMulti(ps_typeInfo, p_valInfo=None, pn_nombreFois=1):
	return Loop(Diffuse(ps_typeInfo, p_valInfo), pn_nombreFois)
def ActionOnMulti(p_configEvent, pFun_reaction, pFun_default=None, pn_nombreFois=1):
	return Loop(ActionOnConfig(p_configEvent, pFun_reaction, pFun_default), pn_nombreFois)
def ActionMulti(pFun, pn_nombreFois=1):
	return Loop(  ProgAtomAction(pFun), pn_nombreFois  )
def Repeat(pn_nombreFois, *args):
	return Loop(   Seq(*args),  pn_nombreFois   )
def RepeatForever(*args):
	return Repeat(-1, *args)
def IfRepeat(pFunc_condition, *args):
	return Loop(   Seq(*args),  -1,  pFunc_condition  )
def IfRepeatLabel(ps_label, pFunc_condition, *args):
	lProg = IfRepeat(pFunc_condition, *args)
	lProg.as_label = ps_label
	return lProg
def Filter(ps_typeSensor, ps_typeInfo, pFunc_filtre, pn_nombreFois=1):
	return Loop(   ProgFilter(ps_typeSensor, ps_typeInfo, pFunc_filtre),  pn_nombreFois   )
RepeatS = Repeat
def ControlS(p_configEvent, *args):
	return ProgControl(p_configEvent, Seq(*args))
def PauseForever():
	return Pause(forever)
def Parex(ps_typeInfo_channel, *args):
	return Par(*args, channel=ps_typeInfo_channel)

# Alias
#--------
Generate = DiffuseMulti
GenerateM = DiffuseMulti
ActionOn = ActionOnMulti
ActionOnM = ActionOnMulti
Action = ActionMulti
Write = Print
Kill = ExecWithStop
Processeur.react = Processeur.doMacroEtape

# Modélisation Monde, Acteur
#---------------------------
Monde = Processeur
Actor = Par
Processeur.addActor = Processeur.addProgram

# Objets actifs (décorateurs)
#----------------------------
def active(pClass):
	class classeComposee(Par, pClass):
		def __init__(self, *args, **kwargs):
			lList_nomMethodeActive = [
				ls_func
				for ls_func in dir(pClass)
				if callable(getattr(pClass, ls_func)) and hasattr(getattr(pClass, ls_func), 'toCallNTimes')
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
	return classeComposee

def automatic(pn_nombreFois):
	def tempAuto(pMethod):
		pMethod.toCallNTimes = pn_nombreFois
		return pMethod
	return tempAuto
