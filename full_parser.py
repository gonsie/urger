# Encapsulation of lexer/parser pair
class PLYPair:
	def __init__(self, l=None, p=None):
		self.lexer = l
		self.parser = p
		self.result = None

	def set_lexer(self, l):
		self.lexer = l

	def set_parser(self, p):
		self.parser = p

	def parse_file(self, fname):
		f = open(fname, 'r')
		a = f.read()
		f.close()
		return self.parse(a)

	def parse(self, text):
		self.result = self.parser.parse(text, lexer=self.lexer)
		return self.result

import ply_verilog_netlist
import ply_liberty
import ply_boolean_expressions

if __name__ == "__main__":
	print "\n*** Liberty Parser"
	l = PLYPair()
	l.set_lexer(ply_liberty.create_lexer())
	l.set_parser(ply_liberty.create_parser())
	l.parse_file('Examples/example_library.lib')
	cd = l.result.cell_tokens()
	print l.result.stats

	print "\n*** Verilog Netlist Parser"
	vn = PLYPair()
	vn.set_lexer(ply_verilog_netlist.create_lexer(cd))
	vn.set_parser(ply_verilog_netlist.create_parser())
	vn.parse_file('Examples/example_netlist.v')

	print "\n*** Boolean Expression Parser"
	be = PLYPair()
	be.set_lexer(ply_boolean_expressions.create_lexer())
	be.set_parser(ply_boolean_expressions.create_parser())

	for cell_name in cd:
		cell = l.result.get_cell(cell_name)
		pd = cell.pin_tokens()
		pm = cell.pin_map()

		# this only works because of introspection at runtime
		ply_boolean_expressions.update(pd, pm)

		print cell_name
		for p in cell.boolexps():
			print "\tPin", p.name, "=", p.function, "\t--> ", p.cstr, "=", be.parse(p.function)


