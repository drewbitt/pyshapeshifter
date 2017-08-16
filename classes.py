import abc 		# for abstract methods. not really needed but eh
import scrape	# debug

""" Class for the board that contains the board layout (objects in a list), the cycle of how the objects change,
and the goal. Has method to change board when piece is passed to it at a certain position"""
class Board(list):		# maybe subclass this as list or object (depending on approach)

	def __init__(self, board_array, cycle_array):
		super().__init__()
		self.board_array = board_array
		self.cycle_array = cycle_array
		self.board_array = self.__convert_board(self.board_array)

		# Convert cycle array to become a list of their corresponding object
		self.cycle_array = self.__convert_cycle(self.cycle_array)
		# Create dictionary of order of conversion
		self.type_dict = self.__create_cycle_type_dict()

	"""Convert text values of board (e.g. "swo") into objects of their type"""
	def __convert_board(self, b):
		for index, row in enumerate(b):
			for index2, col in enumerate(row):
				if col == "swo":
					col = SwordObj((index, index2))
				elif col ==  "cro":
					col = CrownObj((index, index2))
				elif col == "gob":
					col = GobletObj((index, index2))
				row[index2] = col		# why am I having to do this to get it to save to row? scope issue? enum issue?
		return b

	"""Convert text values of cycle into objects of their own type
	Note: uses default value of None for coordinates since that doesn't matter here
	"""
	def __convert_cycle(self, c):
		for index, i in enumerate(c):
			i = i[:-2]		# remove the trailing info from cycle_array items so you just get "cro", "swo" etc
			# convert cycle_array items to objects as well
			if i == "swo":
				i = SwordObj()
			elif i == "cro":
				i = CrownObj()
			elif i == "gob":
				i = GobletObj()
			c[index] = i
		return c

	def get_cycle(self):
		return self.cycle_array

	"""Returns the goal, which is always the second to last item in cycle array
	Returns the actual object
	"""
	def get_goal(self):
		return self.cycle_array[-2]

	"""Create dictionary of how the types should change"""
	def __create_cycle_type_dict(self):
		cycle_type_dict = {}
		for index, i in enumerate(self.cycle_array[:-1]):
			cycle_type_dict[ i.name() ] = self.cycle_array[index+1].name()
		return cycle_type_dict

	"""Change the type of a single obj. Updates position of new node to old obj's position as well
	Is used when placing a shape onto the board"""
	def __change_type(self, piece):
		name = self.type_dict[piece.name()]
		name = name + "Obj(piece.get_coord())"
		return eval(name)		# evaluates string to create object

	""" piece is Pieces object, coord is tuple, chk=True means only check and return board after placing,
	without actually writing to self.board_array.

	If chk = True, returns a new board object after the placement of the shape without altering the original
	"""

	def place_shape(self, piece, coord, chk=False):
		print("Implement later")

# --------------Objects
# Add others later once I get to their levels and figure out their names

# Individual objects (crown, goblet, etc.) would be children to this
class TypeOfObj(metaclass=abc.ABCMeta):

	# Going to store coordinate to easily look at positions. May not be needed, but shouldn't be harmful.
	# Store in tuple form i.e (row, col)
	def __init__(self, coord=None):
		self.coord = coord

	def get_coord(self):
		return self.coord
	def update_coord(self, coord):
		coord = self.coord

	@abc.abstractmethod
	def get_image(self):
		"""Returns img for the class to be used for displaying"""
	@abc.abstractmethod
	def print(self):
		"""Print name of class and coordinate"""

class CrownObj(TypeOfObj):
	def get_image(self):
		return("IMAGE GOES HERE")
	def name(self):
		return("Crown")
	def print(self):
		print("Crown Object - Coord = {}".format(self.coord))
class GobletObj(TypeOfObj):
	def get_image(self):
		return("IMAGE GOES HERE")
	def name(self):
		return("Goblet")
	def print(self):
		print("Goblet Object - Coord = {}".format(self.coord))
class SwordObj(TypeOfObj):
	def get_image(self):
		return("IMAGE GOES HERE")
	def name(self):
		return("Sword")
	def print(self):
		print("Sword Object - Coord= {}".format(self.coord))
TypeOfObj.register(CrownObj)
TypeOfObj.register(GobletObj)
TypeOfObj.register(SwordObj)
# -----------------------------------------------

class Pieces(list):
	def __init__(self, pieces_array):
		super().__init__()
		self.pieces_array = pieces_array
		self.pieces_array = self.__remove_empty(pieces_array)

	"""Remove all empty (all elements = 0) rows and columns to get true shape size"""
	def __remove_empty(self, p):
		"""Transpose goes through rows and columns. remove_blank_rows removes all rows where all elements eval to False,
		which 0 does"""
		def transpose(a):
			return zip(*a)
		def remove_blank_rows(a):
			return [list(row) for row in a if any(row)]
		for index, i in enumerate(p):
			i = remove_blank_rows( transpose(remove_blank_rows(transpose(i))))
			p[index] = i
		return p

b, c, p= scrape.get_all("C:/Users/andys-pc/Downloads/ShapeShifter.html")
Board(b,c)
Pieces(p)
