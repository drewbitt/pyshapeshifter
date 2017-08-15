''' Scrapes the .html file of the game's page
Would be great to look into using native HTML scraping/parsing for this, or Javascript'''

import sys
from html.parser import HTMLParser

# using HTMLParser for parsing shapes

class MyHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		# the max size of a shape is 4x5 so a [4][5] array
		self.size = [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]]
		self.in_tr = False
		self.in_td = False
		# there is an extra <td> and <tr> before the ones with the <img> tags, so adding to see if we are in the
		# correct table so that the count does not mess up. also allows to save shapes
		self.in_correct_table = False
		self.count_row = 0
		self.count_cell = 0

	def handle_starttag(self, tag, attrs):
		if tag == 'table':
			cellpadding = int(attrs[1][1])
			if cellpadding == 0:
				self.in_correct_table = True
		elif tag == 'tr':
			if self.in_correct_table:
				self.count_row += 1
				self.in_tr = True
		elif tag == 'td':
			if self.in_correct_table:
				self.count_cell += 1
				self.in_td = True
		elif tag == 'img':
			if self.in_correct_table:		# uneeded I think
				print("Row {}".format(self.count_row))
				print("Cell {}".format(self.count_cell))
				print(self.size)
				self.size[self.count_row-1][self.count_cell-1] += 1

	def handle_endtag(self, tag):
		if self.in_correct_table:
			if tag == 'td':
				self.in_td = False
			elif tag == 'tr':
				self.in_tr = False
				self.count_cell = 0
			elif tag == 'table':
				# save shape
				self.count_row = 0
				self.count_cell = 0

# Method for parsing the board, getting the cycle for changing types, and getting all pieces available
def get_all(infile="C:/Users/andys-pc/Downloads/ShapeShifter.html"):
	board_array = []
	cycle_array = []
	pieces_array = []
	try:
		with open(infile, encoding='utf8') as f:
			for line in nonblank_lines(f):
				# 1a) Get board array
				if('imgLocStr = new') in line:
					# Board is an array. imgLocStr = new Array starts it, gives num rows
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
							line= next(f)

				# 2) Get cycle for changing types
				# Goal is always second to last
				if ('border="1" bordercolor="gray"' in line):
					while ("gif" in line):
						if ("arrow" not in line):
							index_r = line.index(".gif")
							index_l = line[:index_r].rfind("/")
							cycle_array.append(line[index_l+1:index_r])
						line= next(f)

				# 3) Get pieces available
				if ("<b><big>ACTIVE SHAPE</big></b>" in line):
					parser = MyHTMLParser()
					parser.feed(line)

				'''<center><b><big>ACTIVE SHAPE</big></b><p></p>

				<table border="0" cellpadding="15" cellspacing="0" width="50" height="50">
				<tbody>

				<tr>	row
				<td>	cell

				<table border="0" cellpadding="0" cellspacing="0">		start piece

				<tbody>

				<tr><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td>
				<td height="10" width="10"></td>

				</tr>		end row - means just one thing is here

				<tr><td>

				<img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td>
				<td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0">
				</td>

				</tr>     means two things were here

				<tr><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td height="10" width="10"></td></tr>
				</tbody>

				</table>

				</td>
				</tr>
				</tbody>
				</table>

				<br><center><b><big>NEXT SHAPES</big></b><table border="0" cellpadding="15" cellspacing="0" width="50" height="50"><tbody><tr><td align="center" valign="center"><table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td height="10" width="10"></td><td height="10" width="10"></td></tr><tr><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td height="10" width="10"></td></tr><tr><td height="10" width="10"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td></tr></tbody></table></td><td align="center" valign="center"><table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td height="10" width="10"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td></tr><tr><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td></tr><tr><td height="10" width="10"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td height="10" width="10"></td></tr></tbody></table></td><td align="center" valign="center"><table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td height="10" width="10"></td></tr><tr><td height="10" width="10"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td height="10" width="10"></td></tr><tr><td height="10" width="10"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td></tr></tbody></table></td><td align="center" valign="center"><table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td></tr><tr><td height="10" width="10"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td height="10" width="10"></td></tr></tbody></table></td><td align="center" valign="center"><table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td height="10" width="10"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td></tr><tr><td height="10" width="10"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td height="10" width="10"></td></tr><tr><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td></tr></tbody></table></td><td align="center" valign="center"><table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td></tr><tr><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td height="10" width="10"></td></tr></tbody></table></td><td align="center" valign="center"><table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td></tr></tbody></table></td><td align="center" valign="center"><table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td height="10" width="10"></td><td height="10" width="10"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td></tr><tr><td height="10" width="10"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td></tr><tr><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td height="10" width="10"></td></tr></tbody></table></td></tr><tr><td align="center" valign="center"><table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td></tr><tr><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td height="10" width="10"></td></tr></tbody></table></td><td align="center" valign="center"><table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td height="10" width="10"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td></tr><tr><td height="10" width="10"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td></tr><tr><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td><img src="./ShapeShifter_files/square.gif" width="10" height="10" border="0"></td><td height="10" width="10"></td></tr></tbody></table></td></tr></tbody></table>  <p align="center">
				'''


	except StopIteration:	# generator running out of values when next() is used. normal. may not be needed
		pass
	except (OSError, IOError):		# python 3.3 IOError became OSError & FileNotFoundError is in OSError
		print("Could not open file to parse board")
		sys.exit(1)

# don't need to remove blank lines, just for debugging/readability
def nonblank_lines(f):
	for l in f:
		line = l.rstrip()
		if line:
			yield line

get_all()
