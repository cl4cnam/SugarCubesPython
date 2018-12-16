#
# SugarCubes.py
# Auteur du modèle théorique : Jean-Ferdy Susini
# Auteur de l'implémentation python : Claude Lion
# Date création : 04/06/2018
# Copyright : © Claude Lion 2018
#
from SugarCubesUtils import *

# avancements
PAS_FINI = 0
FINI = 1

forever = -1

class Info:
	def __init__(self, ps_type, p_valeur):
		self.as_type = ps_type
		self.a_valeur = p_valeur
	def isSensor(self):
		return self.as_type[0] == '$'
	def getValeur(self):
		if callable(self.a_valeur):
			return self.a_valeur()
		else:
			return self.a_valeur
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
		self.aSetLiveProg_finiPourLInstant = set()
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
		# Mise en place nouvel instant
		#---------------------------------
		self.aInstant = Instant(self.aInstant)
		
		# Exécution normale
		#---------------------------------
		# printErr('---------------------------------------------------------------------')
		# printErr('--> num instant : ' + str(self.aInstant.an_num))
		# printErr('---------------------------------------------------------------------')
		while not self.aLiveProgParallel.isFiniPourMacroEtape():
			self.aLiveProgParallel.doMicroEtape()
			if not self.isThereSomethingToUnblock(): break
		
		# Exécution spéciale "fin d'instant"
		#-----------------------------------
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
initUtils(__name__, Program)

class LiveProgram: # abstract
	def __init__(self, *args):
		self.ai_avancement = PAS_FINI
		self.aList_args = list(args)
		setParent(args, self)
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
	def isFiniPourMacroEtape(self):
		return self.isTerminee() or id(self) in self.getProcesseur().aInstant.aSetLiveProg_finiPourLInstant
	def isTerminee(self):
		return self.ai_avancement == FINI
	def copyAvancement(self, pLiveProg):
		self.ai_avancement = pLiveProg.ai_avancement
		lSetLiveProg_fini = self.getProcesseur().aInstant.aSetLiveProg_finiPourLInstant
		if pLiveProg.isFiniPourMacroEtape():
			self.setFiniPourMacroEtape()
		else:
			lSetLiveProg_fini.discard(id(self))
	def copyMinAvancement(self, pListLiveProg):
		lList_avancement = [ lLiveProg.ai_avancement for lLiveProg in pListLiveProg ]
		self.ai_avancement = min(  lList_avancement  ) if len(lList_avancement) else FINI
		lSetLiveProg_fini = self.getProcesseur().aInstant.aSetLiveProg_finiPourLInstant
		if all( [
			lLiveProg.isFiniPourMacroEtape() or lLiveProg.isTerminee()
			for lLiveProg in pListLiveProg
		] ):
			self.setFiniPourMacroEtape()
	def setFiniPourMacroEtape(self):
		lSetLiveProg_fini = self.getProcesseur().aInstant.aSetLiveProg_finiPourLInstant
		lSetLiveProg_fini.add(id(self))
	def terminer(self):
		self.ai_avancement = FINI
	def doMicroEtape(self):
		if not self.isFiniPourMacroEtape():
			self.doTransition()
	def doMicroEtapeDeFinDInstant(self):
		self.doTransitionFinale()
	def doTransitionFinale(self):
		pass

@deLive('double')
class LiveProgExecWithStop(LiveProgram):
	def __init__(self, p_configEvent, pLiveProg, pLiveProg_lastWill=None):
		super().__init__(p_configEvent, pLiveProg, pLiveProg_lastWill)
		self.a_configEvent = p_configEvent
		self.aLiveProg = pLiveProg
		self.aLiveProg_lastWill = pLiveProg_lastWill
		self.ab_killable = True
	def doTransition(self):
		self.aLiveProg.doMicroEtape()
		self.copyAvancement(self.aLiveProg)
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

@deLive('double')
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
			self.copyAvancement(self.aLiveProg_courant)
	def doTransitionFinale(self):
		if self.aLiveProg_courant != None:
			self.aLiveProg_courant.doMicroEtapeDeFinDInstant()
			self.copyAvancement(self.aLiveProg_courant)
		else:
			self.aLiveProg_courant = self.aLiveProg_else
			if self.aLiveProg_else == None:
				self.terminer()

@deLive('double')
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
			self.copyAvancement(self.aLiveProg_courant)
		else:
			self.terminer()

@deLive('double')
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
			self.copyAvancement(self.aLiveProg_courant)
		else:
			self.terminer()

@deLive('double')
class LiveProgNothing(LiveProgram):
	def __init__(self, *args):
		super().__init__(*args)
		self.terminer()
	def doTransition(self):
		pass
	def doTransitionFinale(self):
		pass

@deLive('double')
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

@deLive('double')
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

@deLive('double')
class LiveProgDiffuse(LiveProgram):
	def __init__(self, ps_typeInfo, p_valeurInfo=None):
		super().__init__(ps_typeInfo, p_valeurInfo)
		self.aInfo = Info(ps_typeInfo, p_valeurInfo)
		if self.aInfo.isSensor(): raise TypeError('Les sensors ne peuvent pas être diffusés')
	def doTransition(self):
		lProcesseur = self.getProcesseur()
		lDictInfo_diffusees = lProcesseur.aInstant.aDictInfo_diffusees
		lInfo_updated = Info(self.aInfo.as_type, self.aInfo.getValeur())
		lInfo_updated.addToDictInfo(lDictInfo_diffusees)
		self.terminer()

@deLive('simple')
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

@deLive('double')
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

@deLive('double')
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
			self.copyAvancement(self.aLiveProg)
		else:
			lProcesseur.aInstant.aDict_configOuString__typesInfoAttendu[id(self)] = self.a_typesInfoAttendue
	def doTransitionFinale(self):
		lProcesseur = self.getProcesseur()
		if lProcesseur.aInstant.evalConfig(self.a_typesInfoAttendue):
			self.aLiveProg.doMicroEtapeDeFinDInstant()
			self.copyAvancement(self.aLiveProg)

@deLive('double')
class LiveProgPause(LiveProgram):
	def __init__(self, pn_nombreFois=1):
		super().__init__(pn_nombreFois)
		self.ai_pausesRestantes = pn_nombreFois
	def doTransition(self):
		if self.ai_pausesRestantes == 0:
			self.terminer()
		else:
			self.ai_pausesRestantes -= 1
			self.setFiniPourMacroEtape()
	def setNouvelleMacroEtape(self):
		self.setPlusFiniPourMacroEtape()

@deLive('simple')
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

@deLive('double')
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
		self.copyMinAvancement(self.aList_args)
	def doTransitionFinale(self):
		for l_instr in self.aList_args:
			l_instr.doMicroEtapeDeFinDInstant()
		self.copyMinAvancement(self.aList_args)
		
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
				self.ai_avancement = PAS_FINI
ProgPar = ProgParallel
Par = ProgParallel

class LiveProgSeq_(LiveProgram):
	def __init__(self, pIter_instr):
		super().__init__()
		self.aIter_instr = pIter_instr
	def doTransition(self):
		while True:
			try:
				if not hasattr(self, 'aProg_courante') or self.aProg_courante.isTerminee():
					self.aProg_courante = next(self.aIter_instr)
					setParent([self.aProg_courante], self)
			except StopIteration:
				break
			self.aProg_courante.doMicroEtape()
			if not self.aProg_courante.isTerminee():
				self.copyAvancement(self.aProg_courante)
				return
		self.terminer()
	def doTransitionFinale(self):
		try:
			self.aProg_courante.doMicroEtapeDeFinDInstant()
			if not self.aProg_courante.isTerminee():
				self.copyAvancement(self.aProg_courante)
		except AttributeError: pass

@deLive('simple')
class LiveProgSequence(LiveProgram):
	def __new__(cls, *args):
		return LiveProgSeq_(iter(args))
	def __str__(self):
		return '; '.join( [ str(arg) for arg in self.aList_args ] )
ProgSeq = ProgSequence
Seq = ProgSequence

@deLive('double')
class LiveProgLoop(LiveProgram):
	def __new__(cls, pLiveProgram_corps, pn_nombreFois=1, pFunc_cond=None):
		def getNewIter(pLiveProgram_corps, pn_nombreFois):
			if pn_nombreFois == 0: raise StopIteration
			ln_nombreProgDejaFaite = 0
			while True:
				yield pLiveProgram_corps
				ln_nombreProgDejaFaite += 1
				lParent = pLiveProgram_corps.a_parent
				pLiveProgram_corps = pLiveProgram_corps.aProg.getLive()
				pLiveProgram_corps.a_parent = lParent
				if pFunc_cond != None:
					if not pFunc_cond(): break
				if ln_nombreProgDejaFaite >= pn_nombreFois*2 - 1 and pn_nombreFois != -1: break
				lLivePause = Pause().getLive()
				lLivePause.a_parent = lParent
				yield lLivePause
				ln_nombreProgDejaFaite += 1
			raise StopIteration
		return LiveProgSeq_(  getNewIter(pLiveProgram_corps, pn_nombreFois)  )

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
RepeatS = Repeat
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
def ControlS(p_configEvent, *args):
	return ProgControl(p_configEvent, Seq(*args))
def KillS(p_configEvent, *args):
	return ExecWithStop(p_configEvent, Seq(*args))
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
