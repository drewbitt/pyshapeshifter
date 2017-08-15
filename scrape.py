""" File to scrape the .html file of the game's page to get layout, rules, and available shapes
Could've been done much easier in Javascript, but I was exploring Python
"""

import sys
from html.parser import HTMLParser

""" Uses HTMLParser for parsing shapes just so I could try it out

Overrides MyHTMLParser class methods handle_starttag and handle_endtag
"""

class MyHTMLParser(HTMLParser):

	def __init__(self):
		HTMLParser.__init__(self)
		self.size = [[0 for _ in range(5)] for _ in range(4)]		# max size = 4*5. array top-bottom, left-right
		self.in_tr, self.in_td, self.in_correct_table = (False,)*3
		self.count_row, self.count_cell = 0, 0
		self.pieces_array = []

	def error(self, message):		# to implement all abstract methods
		pass

	def get_pieces_array(self):
		return self.pieces_array

	def handle_starttag(self, tag, attrs):
		if tag == 'table':
			cellpadding = int(attrs[1][1])		# assumes cell_padding is always second, border first
			# there is extra <td> & <tr> in a table b4 useful tags, so checking for correct table
			if cellpadding == 0:		# incorrect table has cell_padding = 15 from what I've seen
				self.in_correct_table = True
		elif tag == 'tr':
			if self.in_correct_table:
				self.count_row += 1		# keeps track of what row we are in
				self.in_tr = True
		elif tag == 'td':
			if self.in_correct_table:
				self.count_cell += 1
				self.in_td = True
		elif tag == 'img':
			# if an img is found, the img = one square block of the shape
			# keep track of all blocks found in shape by making the found position = 1 in self.size
			self.size[self.count_row-1][self.count_cell-1] += 1

	def handle_endtag(self, tag):
		if self.in_correct_table:
			if tag == 'td':
				self.in_td = False
			elif tag == 'tr':
				self.in_tr = False
				self.count_cell = 0
			elif tag == 'table':
				if self.in_correct_table:
					self.in_correct_table = False
					# store completed shape, reset shape size & all counts
					self.pieces_array.append(self.size)
					self.size = [[0 for _ in range(5)] for _ in range(4)]
					self.count_row, self.count_cell = 0, 0

"""Method for parsing the board, getting the cycle for changing types, and getting all pieces available
All combined so that the file would not be iterated through multiple times

Returns tuple of the board list, cycle list, and shape list"""

def get_all(infile):
	board_array = []
	cycle_array = []
	pieces_array = []
	try:
		with open(infile, encoding='utf8') as f:
			for line in f:
				# 1a) Get board array
				if'imgLocStr = new' in line:
					# Board is an array. imgLocStr = new Array starts it, gives # rows
					num_rows = int(line[line.index("(") + 1:line.index(")")])
					# next line gives number of columns
					line = next(f)
					num_cols = int(line[line.index("(") + 1:line.index(")")])
					# skip until line no longer contains = new Array. also create two-dimensional array
					for _ in range(num_rows):
						board_array.append([0] * num_rows)
						line = next(f)

					# 1b) Fill board array
					for col in range(num_cols):
						for row in range(num_rows):
							obj_type = line[line.index('"') + 1: len(line)-2]
							board_array[row][col] = obj_type
							line = next(f)

				# 2) Get cycle for changing types
				# Goal is always second to last
				if 'border="1" bordercolor="gray"' in line:
					while "gif" in line:
						# ignore all arrow images
						if "arrow" not in line:
							index_r = line.index(".gif")
							index_l = line[:index_r].rfind("/")
							cycle_array.append(line[index_l+1:index_r])
						line = next(f)

				# 3) Get pieces available
				if "<b><big>ACTIVE SHAPE</big></b>" in line:
					parser = MyHTMLParser()
					parser.feed(line)
					pieces_array = parser.get_pieces_array()

		return (board_array, cycle_array, pieces_array)
	except (OSError, IOError):		# python 3.3 IOError became OSError & FileNotFoundError is in OSError
		sys.exit("Could not open file to scrape/parse")

if __name__ == '__main__':
	get_all("C:/Users/andys-pc/Downloads/ShapeShifter.html")		# debugging
