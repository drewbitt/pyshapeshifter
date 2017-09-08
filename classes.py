"""
To Do:
	* Implement getting the image for each object
	* Speed fixes
"""

import abc 			# not really needed but eh
# import scrape		# debug

""" Class for the board that contains the board layout (objects in a list), the cycle of how the objects change,
and the goal. Has method to change the board"""
class Board(list):		# may not need to be of class list

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
					col = SwordObj([index, index2])		# row, col
				elif col == "cro":
					col = CrownObj([index, index2])
				elif col == "gob":
					col = GobletObj([index, index2])
				row[index2] = col
		return b

	"""Convert text values of cycle_array into objects. Uses default value of None for coordinate"""
	def __convert_cycle(self, c):
		for index, i in enumerate(c):
			i = i[:-2]		# remove the trailing info from cycle_array elements
			if i == "swo":
				i = SwordObj()
			elif i == "cro":
				i = CrownObj()
			elif i == "gob":
				i = GobletObj()
			c[index] = i
		return c

	def __create_cycle_type_dict(self):
		cycle_type_dict = {}
		for index, i in enumerate(self.cycle_array[:-1]):
			cycle_type_dict[i.name()] = self.cycle_array[index+1].name()
		return cycle_type_dict

	def __change_type(self, board_obj):
		name = self.type_dict[board_obj.name()]
		name += "Obj(board_obj.get_coord())"
		return eval(name)		# evaluates string to create object

	""" coord is a list of all coordinates to change, chk=True means only check and return board after placing,
	without writing to self.board_array.
	Returns True if sucessful & chk=False
	"""
	def place_shape(self, coord, chk=False):
		board = self.board_array
		for c in coord:
			board[c[0]][c[1]] = self.__change_type(board[c[0]][c[1]])
		if chk:
			return board
		self.board_array = board
		return True

# --------------Objects
# Add others later once I get to their levels and figure out their names
class TypeOfObj(metaclass=abc.ABCMeta):
	# coord is list [row, col]
	def __init__(self, coord=None):
		self.coord = coord
	@abc.abstractmethod
	def get_image(self):
		"""Returns img for the class to be used for displaying"""
	@abc.abstractmethod
	def print(self):
		"""Print name of class and coordinate"""

# Unsure if I want each class to actually print the image with .print or just return the filename
class CrownObj(TypeOfObj):
	def get_image(self):
		return "IMAGE GOES HERE"
	def name(self):
		return "Crown"
	def print(self):
		print("Crown Object, coord {}".format(self.coord))
class GobletObj(TypeOfObj):
	def get_image(self):
		return "IMAGE GOES HERE"
	def name(self):
		return "Goblet"
	def print(self):
		print("Goblet Object, coord {}".format(self.coord))
class SwordObj(TypeOfObj):
	def get_image(self):
		return "IMAGE GOES HERE"
	def name(self):
		return "Sword"
	def print(self):
		print("Sword Object, coord {}".format(self.coord))
TypeOfObj.register(CrownObj)
TypeOfObj.register(GobletObj)
TypeOfObj.register(SwordObj)
# -----------------------------------------------
''' Simple list object of the pieces that slims down the array from extra 0s.'''
class Pieces(list):
	def __init__(self, pieces_array):
		super().__init__()
		self.pieces_array = pieces_array
		self.pieces_array = self.__remove_empty(pieces_array)

	"""Remove all empty (all elements = 0) rows and columns to get true shape size"""
	def __remove_empty(self, p):
		# Transpose goes through rows and columns. remove_blank_rows removes all rows where all elements eval False,
		# which 0 does
		def transpose(a):
			return zip(*a)

		def remove_blank_rows(a):
			return [list(row) for row in a if any(row)]

		for index, i in enumerate(p):
			i = remove_blank_rows(transpose(remove_blank_rows(transpose(i))))
			p[index] = i
		return p

	def get_piece(self, index, remove=False):
		if remove:
			return Piece(self.pieces_array.pop(index))
		else:
			return Piece(self.pieces_array[index])

class Piece:
	def __init__(self, layout):
		self.layout = layout
	def print(self):
		return "IMPLEMENT LATER"

'''
b, c, p= scrape.get_all("C:/Users/andys-pc/Downloads/ShapeShifter.html")
bb = Board(b,c)
pp = Pieces(p)

# first shape is [ [1,0], [1,1], [1,0] ]
bb.place_shape([ [2,0], [2,1], [3,1], [2,2] ])
'''

