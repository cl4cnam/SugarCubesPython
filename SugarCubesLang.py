from SugarCubes import *

gList_instrSimple = ['print', 'pause', 'await', 'diffuse', 'generate', 'action', 'actionOn', 'filter']
gDict_debBlock_unArg = {
	'repeat': 'Repeat',
	'when': 'When',
	'killL': 'Kill',
	'killS': 'KillS',
	'execWithStopOnL': 'Kill',
	'execWithStopOnS': 'KillS',
	'control': 'ControlS',
	'parex': 'Parex',
	'generateProg': 'Generate',
	'while': 'IfRepeat',
}
gDict_debBlockSimple = {
	'paral': 'Par',
	'seq': 'Seq',
	'branch': 'Seq',
}

def modifySource(ps_source):
	import re
	ls_source = ps_source
	ls_source = re.sub(r'^(\s*)pause$', r'\1pause()', ls_source, 0, re.MULTILINE)
	
	for ls_elt in gDict_debBlock_unArg:
		ls_source = re.sub(ls_elt + r' (.*):', r'for _i_i_i_' + gDict_debBlock_unArg[ls_elt] + r' in range(\1):', ls_source)
	for ls_elt in gDict_debBlockSimple:
		ls_source = re.sub(ls_elt + r':', r'for _PPP_' + gDict_debBlockSimple[ls_elt] + r' in range(0):', ls_source)
	
	for ls_elt in gList_instrSimple:
		ls_source = re.sub(ls_elt + r' (.*)', ls_elt + r'(\1)', ls_source)
	
	lList_nomClasse = re.findall(r'^class (\w+)\(.*\):$', ls_source, re.MULTILINE)
	for ls_nomClasse in lList_nomClasse:
		ls_source = re.sub(r'^(\s*)' + ls_nomClasse + ':', r'\1for _PPP_' + ls_nomClasse + r' in range(0):', ls_source, 0, re.MULTILINE)
	
	# printErr(ls_source)
	return ls_source

def importScPy(ps_name):
	from importlib.machinery import SourceFileLoader
	ls_source = SourceFileLoader(ps_name, ps_name + '.py').get_source(ps_name)
	ls_source = modifySource(ls_source)
	import imp
	tempModule = imp.new_module(ps_name)
	tempModule._source_ = ls_source
	import sys
	sys.modules[ps_name] = tempModule
	exec(ls_source, tempModule.__dict__)
	return tempModule

def sugarifiee(pFunc_prog):
	import ast
	import inspect
	# ls_source = inspect.getsource(pFunc_prog)
	ln_debFunc = pFunc_prog.__code__.co_firstlineno
	# printErr(ln_debFunc)
	import sys
	lModule = sys.modules[pFunc_prog.__module__]
	ls_source = lModule._source_
	lList_lines = ls_source.splitlines(True)
	ls_sourceFunc = ''.join(  inspect.getblock(lList_lines[ln_debFunc:])  )
	# printErr(ls_sourceFunc)
	
	lNode_prog = ast.parse(ls_sourceFunc)
	
	class Visiteur(ast.NodeTransformer):
		def visit_Name(self, node):
			if node.id in gList_instrSimple:
				return ast.Name(node.id[0].upper() + node.id[1:], ast.Load())
			if node.id == 'AND':
				return ast.Name('And', ast.Load())
			if node.id == 'OR':
				return ast.Name('Or', ast.Load())
			return node
		
		def visit_If(self, node):
			self.generic_visit(node)
			# node.test, node.body, node.orelse
			return ast.Call(
				func=ast.Name(id='Test', ctx=ast.Load()),
				args=[
					node.test,
					ast.Call(
						func=ast.Name(id='Seq', ctx=ast.Load()),
						args=node.body,
						keywords=[],
						starargs=None,
						kwargs=None
					),
					ast.Call(
						func=ast.Name(id='Seq', ctx=ast.Load()),
						args=node.orelse,
						keywords=[],
						starargs=None,
						kwargs=None
					),
				],
				keywords=[],
				starargs=None,
				kwargs=None
			)
		
		def visit_Assign(self, node):
			self.generic_visit(node)
			lNode_diffuse = ast.Call(
				func=ast.Name(id='Diffuse', ctx=ast.Load()),
				args=[
					ast.Str(
						s=node.targets[0].id
					),
					node.value
				],
				keywords=[],
				starargs=None,
				kwargs=None
			)
			# printErr(ast.dump(lNode_diffuse))
			return lNode_diffuse
		
		def visit_For(self, node):
			self.generic_visit(node)
			if node.target.id.startswith('_i_i_i_'):
				import re
				ls_instr = re.match(r'_i_i_i_(\S*)', node.target.id).group(1)
				l_firstArg = node.iter.args[0]
				lNode_body = node.body
				lNode_body.insert(0, l_firstArg)
				lNode_repeat = ast.Call(
					func=ast.Name(id=ls_instr, ctx=ast.Load()),
					args=lNode_body,
					keywords=[],
					starargs=None,
					kwargs=None
				)
				return lNode_repeat
			if node.target.id.startswith('_PPP_'):
				import re
				ls_instr = re.match(r'_PPP_(\S*)', node.target.id).group(1)
				return ast.Call(
					func=ast.Name(id=ls_instr, ctx=ast.Load()),
					args=node.body,
					keywords=[],
					starargs=None,
					kwargs=None
				)
			return node
		
		def visit_Expr(self, node):
			self.generic_visit(node)
			return node.value
		
		def visit_Module(self, node):
			# printErr(ast.dump(node))
			self.generic_visit(node)
			# return ast.Expression(node.body[0].body[0].value)
			# lNode_body = node.body[1].body
			lNode_body = node.body[0].body
			lNode_seq = ast.Call(
				func=ast.Name(id='Seq', ctx=ast.Load()),
				args=lNode_body,
				keywords=[],
				starargs=None,
				kwargs=None
			)
			return ast.Expression(lNode_seq)
	
	lNode_prog = Visiteur().visit(lNode_prog)
	ast.fix_missing_locations(lNode_prog)
	
	# printErr(ast.dump(lNode_prog, True, True))
	# printErr(ast.dump(lNode_prog))
	l_ret = eval(compile(lNode_prog, filename="<ast>", mode="eval"), lModule.__dict__)
	# printErr(l_ret)
	return l_ret


def sugarcube(p_nombreInstant_ou_fctProg, *, printInstant=None):
	if callable(p_nombreInstant_ou_fctProg):
		return sugarifiee(p_nombreInstant_ou_fctProg)
	ln_nombreInstant = p_nombreInstant_ou_fctProg
	def tempTranfo(pFunc_prog):
		def tempTranformee(*args, **kwargs):
			gProcesseur = Processeur()
			lProg = sugarifiee(pFunc_prog)
			gProcesseur.addProgram(lProg)

			while not gProcesseur.aLiveProgParallel.isTerminee() and gProcesseur.aInstant.an_num == -1 or gProcesseur.aInstant.an_num < ln_nombreInstant and gProcesseur.aInstant.an_num != -1:
				if printInstant == True:
					print('{0} :'.format(gProcesseur.aInstant.an_num + 1))
				gProcesseur.doMacroEtape()
		tempTranformee.processeurIntegre = True
		return tempTranformee
	return tempTranfo

def extends(pMethod):
	def tempMethod(self, *arg):
		self.__class__.__name__ = self.__class__.__bases__[0].__name__
		getattr(   super(type(self), self),   pMethod.__name__   )   (*arg)
		pMethod(self)
	return tempMethod