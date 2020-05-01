# python

# base class for QC-SH interface.

# How to add new method beside the class
#	class Foo():
# 		pass
# 		...
#	def bar(self):
#	print "ok"
# 	Foo.bar = bar
#
class QClib():
	"""
	Q. C. caller base interface.
	"""
	def ___init__(self):
		"""
		common data block, cannot be inherted by subclass automatically
		"""
		
		return
	def __del__(self):
		
		return
		
	def checkin(self):
		"""
		check interface & determine the implimented module to be called.
		i.e. turbomole/gaussian/... et al.
		if zero time or non-zero.
		
		"""
		
		return
		
	def initialize(self):
		"""
		init. data structure et al.
		"""
		
		return
		
	def prepare(self):
		"""
		prepare qc input data
		based on template (user) or parameter (auto)
		"""
		# coord
		
		# template
		
		# generate
		
		return
		
	def run(self):
		"""
		call the QC code & confirm the running is ok. if not throw error messages.
		"""
		# dscf grad escf egrad
		
		return
		
	def analyze(self):
		"""
		for surface hopping like calc., the required QC information was extraced.
		"""
		
		return
		
	def finalize(self):
		"""
		simply clean up the tmp dat. and so on.
		"""
		
		return
		
		
		
	