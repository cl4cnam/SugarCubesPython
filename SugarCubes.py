from SugarCubesUtils import *

# avancements
PAS_FINI_POUR_MACRO_ETAPE = 0
FINI_POUR_MACRO_ETAPE = 1
FIN = 2

forever = -1

class Event:
	listeEvent = {}
	def __new__(cls, ps_nom):
		if ps_nom in cls.listeEvent:
			return cls.listeEvent[ps_nom]
		else:
			l_temp = super().__new__(cls)
			listeEvent[ps_nom] = l_temp
			return l_temp
	def setPresent(self, pi_instant):
		self.ai_dernierInstantDePresence = pi_instant

class Engine:
	def __init__(self):
		self.aInstruction_program = InstrParallel()
		self.aLiveInstruction_program = self.aInstruction_program.getLive()
		# self.aEventEnv = EventEnv() # TO DEFINE
		self.ai_instant = 1
	def add(self, pInstruction):
		self.aInstruction_program.add(pInstruction)
		self.aLiveInstruction_program.add(pInstruction.getLive())
	def doMacroEtape(self):
		# printErr('num instant : ' + str(self.ai_instant))
		self.aLiveInstruction_program.setNouvelleMacroEtape()
		while not self.aLiveInstruction_program.isFiniPourMacroEtape():
			self.aLiveInstruction_program.doMicroEtape()
		self.ai_instant += 1

class Instruction: # abstract
	niv_tab = 0
	def __init__(self, *args):
		self.aList_args = list(args)
	def getLive(self):
		# printErr(self.__class__.__name__)
		lClass_live = getGlobalByName(__name__, 'Live' + self.__class__.__name__)
		lList_liveArgs = [
			arg.getLive() if isinstance(arg, Instruction) else arg
			for arg in self.aList_args
		]
		lLiveInstr = lClass_live(*lList_liveArgs)
		lLiveInstr.aInstr = self
		return lLiveInstr
	def __str__(self):
		ls_debut = self.__class__.__name__ + '(\n'
		ls_fin = ')'
		ls_milieu = ',\n'.join( [ str(arg) for arg in self.aList_args ] ) + '\n'
		self.__class__.niv_tab += 1
		ls_milieu = getAvecTab(ls_milieu, self.__class__.niv_tab)
		self.__class__.niv_tab -= 1
		return ls_debut + ls_milieu + ls_fin

class LiveInstruction: # abstract
	def __init__(self, *args):
		self.ai_avancement = PAS_FINI_POUR_MACRO_ETAPE
		self.aList_args = list(args)
	def setNouvelleMacroEtape(self):
		self.setPlusFiniPourMacroEtape()
		for arg in self.aList_args:
			if isinstance(arg, LiveInstruction):
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

class InstrNothing(Instruction):
	pass

class LiveInstrNothing(LiveInstruction):
	def __init__(self, *args):
		super().__init__(*args)
		self.terminer()
	def doTransition(self):
		pass

class InstrPause(Instruction):
	pass

class LiveInstrPause(LiveInstruction):
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
Pause = InstrPause

class InstructionAtom(Instruction): # abstract
	pass

class LiveInstructionAtom(LiveInstruction): # abstract
	def doTransition(self):
		self.doIt()
		self.terminer()

class InstrAtomPrint(InstructionAtom):
	pass

class LiveInstrAtomPrint(LiveInstructionAtom):
	def doIt(self):
		print(self.aList_args[0])
Print = InstrAtomPrint

class InstrParallel(Instruction):
	def add(self, pInstr):
		self.aList_args.append(pInstr)

class LiveInstrParallel(LiveInstruction):
	def add(self, pInstr):
		self.aList_args.append(pInstr)
	def __str__(self):
		return ' || '.join( [ str(arg) for arg in self.aList_args ] )
	def doTransition(self):
		for l_instr in self.aList_args:
			l_instr.doMicroEtape()
		self.ai_avancement = min(  [ arg.ai_avancement for arg in self.aList_args ]  )
InstrPar = InstrParallel
Par = InstrParallel

class LiveInstrSeq_(LiveInstruction):
	def __init__(self, pTuple_args, *pDefIter_instr, pFunc_getNewIter):
		super().__init__(pTuple_args)
		self.aDefIter_instr = pDefIter_instr
		self.aFunc_getNewIter = pFunc_getNewIter
		self.aIter_instr = self.aFunc_getNewIter(*self.aDefIter_instr)
	def doTransition(self):
		# printErr('trans ' + self.__class__.__name__)
		while True:
			self.aInstr_courante.doMicroEtape()
			if not self.aInstr_courante.isTerminee():
				self.ai_avancement = self.aInstr_courante.ai_avancement
				return
			try:
				self.aInstr_courante = next(self.aIter_instr)
			except StopIteration:
				break
		self.terminer()
	def setNouvelleMacroEtape(self):
		# printErr('setNouvelleMacroEtape ' + self.__class__.__name__)
		if not hasattr(self, 'aInstr_courante') or self.aInstr_courante.isTerminee():
			try:
				self.aInstr_courante = next(self.aIter_instr)
			except StopIteration:
				# printErr('deb supp ' + self.__class__.__name__)
				self.terminer()
		self.setPlusFiniPourMacroEtape()
		if hasattr(self, 'aInstr_courante'): self.aInstr_courante.setNouvelleMacroEtape()

class InstrSequence(Instruction):
	pass

class LiveInstrSequence(LiveInstruction):
	def __new__(cls, *args, **kwargs):
		def getNewIter(args):
			return iter(args)
		# l_tmpSeq = LiveInstrSeq_(args, args, pFunc_getNewIter=getNewIter, pInstr=kwargs['pInstr'])
		l_tmpSeq = LiveInstrSeq_(args, args, pFunc_getNewIter=getNewIter)
		l_tmpSeq.aList_args = list(args)
		return l_tmpSeq
	def __str__(self):
		return '; '.join( [ str(arg) for arg in self.aList_args ] )
InstrSeq = InstrSequence
Seq = InstrSequence

class InstrLoop(Instruction):
	pass

class LiveInstrLoop(LiveInstruction):
	def __new__(cls, pLiveInstruction_corps, pn_nombreFois=1, **kwargs):
		def getNewIter(pLiveInstruction_corps, pn_nombreFois):
			def defGener(pLiveInstruction_corps, pn_nombreFois):
				if pn_nombreFois == 0: raise StopIteration
				ln_nombreInstrDejaFaite = 0
				while True:
					yield pLiveInstruction_corps
					ln_nombreInstrDejaFaite += 1
					pLiveInstruction_corps = pLiveInstruction_corps.aInstr.getLive()
					pLiveInstruction_corps.setNouvelleMacroEtape()
					if ln_nombreInstrDejaFaite >= pn_nombreFois*2 - 1 and pn_nombreFois != -1: break
					yield Pause().getLive()
					ln_nombreInstrDejaFaite += 1
				raise StopIteration
			return defGener(pLiveInstruction_corps, pn_nombreFois)
		l_tmpLoop = LiveInstrSeq_(
			(pLiveInstruction_corps,),
			pLiveInstruction_corps, pn_nombreFois,
			pFunc_getNewIter=getNewIter
		)
		return l_tmpLoop
Loop = InstrLoop
Repeat = InstrLoop
