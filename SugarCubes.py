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

class Instant:
	def __init__(self, p_instant):
		self.an_num = p_instant.an_num + 1 if isinstance(p_instant, Instant) else 1
		self.aDictInfo_diffusees = {}
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
	def addProgram(self, pProg):
		self.aProgParallel.add(pProg)
		self.aLiveProgParallel.add(pProg.getLive())
	def isThereAwaitToUnblock(self):
		lInstant = self.aInstant
		lDict_typesInfoAttendu = self.aDict_configOuString__typesInfoAttendu
		return any(
			[
				lInstant.evalConfig(lDict_typesInfoAttendu[idInstrAwait])
				for idInstrAwait in lDict_typesInfoAttendu
			]
		)
	def doMacroEtape(self):
		# printErr('num instant : ' + str(self.ai_instant))
		self.aLiveProgParallel.setNouvelleMacroEtape()
		while not self.aLiveProgParallel.isFiniPourMacroEtape():
			self.aLiveProgParallel.doMicroEtape()
			if not self.isThereAwaitToUnblock(): break
		self.aInstant = Instant(self.aInstant)

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
		ls_debut = self.__class__.__name__ + '(\n'
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

class ProgNothing(Program): pass
class LiveProgNothing(LiveProgram):
	def __init__(self, *args):
		super().__init__(*args)
		self.terminer()
	def doTransition(self):
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
		lInstant = lProcesseur.aInstant
		return all([
			lInstant.evalConfig(arg)
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
		lInstant = lProcesseur.aInstant
		return any([
			lInstant.evalConfig(arg)
			for arg in self.aList_args
		])
Or = ProgOr

class ProgDiffuse(Program): pass
class LiveProgDiffuse(LiveProgram):
	def __init__(self, ps_typeInfo, p_valeurInfo=None):
		super().__init__(ps_typeInfo, p_valeurInfo)
		self.as_typeInfo = ps_typeInfo
		self.a_valeurInfo = p_valeurInfo
	def doTransition(self):
		lProcesseur = self.getProcesseur()
		lInstant = lProcesseur.aInstant
		lDictInfo_diffusees = lInstant.aDictInfo_diffusees
		try:
			lDictInfo_diffusees[self.as_typeInfo]
		except KeyError:
			lDictInfo_diffusees[self.as_typeInfo] = []
		if self.a_valeurInfo != None:
			lDictInfo_diffusees[self.as_typeInfo].append(self.a_valeurInfo)
		
		self.terminer()
Diffuse = ProgDiffuse

class ProgAwait(Program): pass
class LiveProgAwait(LiveProgram):
	def __init__(self, p_typesInfoAttendue):
		super().__init__(p_typesInfoAttendue)
		self.a_typesInfoAttendue = p_typesInfoAttendue
	def doTransition(self):
		lProcesseur = self.getProcesseur()
		lInstant = lProcesseur.aInstant
		if lInstant.evalConfig(self.a_typesInfoAttendue):
			try:
				del lProcesseur.aDict_configOuString__typesInfoAttendu[id(self)]
			except KeyError: pass
			self.terminer()
		else:
			lProcesseur.aDict_configOuString__typesInfoAttendu[id(self)] = self.a_typesInfoAttendue
Await = ProgAwait

class ProgPause(Program): pass
class LiveProgPause(LiveProgram):
	def __init__(self, pn_nombreFois=1):
		super().__init__(pn_nombreFois)
		self.ai_pausesRestantes = pn_nombreFois
		self.ai_save_pausesRestantes = pn_nombreFois
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
		self.doIt()
		self.terminer()

class ProgAtomPrint(ProgramAtom): pass
class LiveProgAtomPrint(LiveProgramAtom):
	def doIt(self):
		print(self.aList_args[0])
Print = ProgAtomPrint

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
		# l_tmpSeq.aList_args = list(args)
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

# classe multi
#--------------
class DiffuseMulti:
	def __new__(cls, ps_typeInfo, p_valInfo, pn_nombreFois, **kwargs):
		return Repeat(Seq(Diffuse(ps_typeInfo, p_valInfo)), pn_nombreFois)

# Alias
#--------
Generate = Diffuse
GenerateM = DiffuseMulti
Write = Print

# Modélisation Monde, Acteur
#---------------------------
Monde = Processeur
Actor = Par
Processeur.addActor = Processeur.addProgram
