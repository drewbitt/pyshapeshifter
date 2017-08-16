import abc 		# for subclasses
import scrape	# debug

class Board():		# maybe subclass this as list or object (depending on approach)

	def __init__(self, board_array):
		self.board_array = board_array
		self.__convert(board_array)

	"""Convert text values of board (e.g. "swo") into objects of their type"""
	def __convert(self, b):
		for index, row in enumerate(b):
			for index2, col in enumerate(row):
				if col == "swo":
					col = SwordObj((index, index2))
				elif col ==  "cro":
					col = CrownObj((index, index2))
				elif col == "gob":
					col = GobletObj((index, index2))
				col.print()

	""" shape is Shape object, coord is tuple, chk=True means only check and return board after placing,
	without actually writing to self.board_array.

	Issue - how to get the coordinates right in relation to the shape - coord = bottom left most?

	If chk = True, returns a new board object after the placement of the shape without altering the original.
	Returns -1 if error is reached, else returns None"""
	def place_shape(self, shape, coord, chk=False):
		print("Implement later")

# --------------Objects
# Add others later once I get to their levels and figure out their names

# Individual objects (crown, goblet, etc.) would be children to this
class TypeOfObj(metaclass=abc.ABCMeta):

	# Going to store coordinate to easily look at positions. May not be needed, but shouldn't be harmful.
	# Store in tuple form i.e (row, col)
	def __init__(self, coord):
		self.coord = coord

	def get_coord(self):
		return self.coord

	@abc.abstractmethod
	def get_image(self):
		"""Returns img for the class to be used for displaying"""
	def print(self):
		"""Print name of class and coordinate"""

class CrownObj(TypeOfObj):
	def get_image(self):
		return("IMAGE GOES HERE")
	def print(self):
		print("Crown Object - Coord = {}".format(self.coord))
class GobletObj(TypeOfObj):
	def get_image(self):
		return("IMAGE GOES HERE")
	def print(self):
		print("Goblet Object - Coord = {}".format(self.coord))
class SwordObj(TypeOfObj):
	def get_image(self):
		return("IMAGE GOES HERE")
	def print(self):
		print("Sword Object - Coord= {}".format(self.coord))
TypeOfObj.register(CrownObj)
TypeOfObj.register(GobletObj)
TypeOfObj.register(SwordObj)
# -----------------------------------------------

class Pieces(list):
	def __init__(self, pieces_array):
		super(Pieces, self).__init__()
		self.pieces_array = pieces_array
		self.pieces_array = self.__remove_empty(pieces_array)

	"""Remove all empty rows and columns to get true shape size"""
	def __remove_empty(self, p):
		for v in p:
			# 1) Remove all original rows with no shape cells in them
			v.remove([0,0,0,0,0])
			# 2a) Remove all columns with no shape cells in them. Checks to see if a 1 is found in any column,
			# if not, then removes column. Recursive function, probably one of the worst things I've ever wrote.
			def remove_columns_main(numElements):

				for e in range(numElements):
					found = False
					def remove_cols():
						for i in range(len(v)):
							if v[i][e] == 1:
								return True
					found = remove_cols()
					if found is False or found is None:
						for z in range(len(v)):
							del(v[z][e])
						return remove_columns_main(numElements-1)
				return v
			# 2b) Actually call recursive function and return new array
			v = remove_columns_main(5)

			# 3a) There will be new empty rows, but don't know size of array so can't just v.remove (will error
			# if not found). So recursively checks with loop, removes any completely empty rows
			def remove_new_duplicates(v):
				for q in v:
					if all(n == 0 for n in q):
						v.remove(q)
						return remove_new_duplicates(v)
				return v
			# 3b) Actually call recursive function and return new array
			v = remove_new_duplicates(v)
		# Finally, return new pieces array
		return p


_,_, p= scrape.get_all("C:/Users/andys-pc/Downloads/ShapeShifter.html")
Pieces(p)


