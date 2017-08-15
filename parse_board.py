''' Parses the .html file of the game's page to '''

import sys
# import numpy as np

def get_board(infile="C:/Users/andys-pc/Downloads/ShapeShifter.html"):
	try:
		with open(infile, encoding='utf8') as f:
			for line in nonblank_lines(f):		# not needed to remove blank lines, just for readability for me
				# 1a) Get board array
				if("imgLocStr = new") in line:
					# Board is an array. imgLocStr = new Array starts it, gives num rows
					num_rows = int(line[line.index("(") + 1:line.index(")")])
					# recreate board array
					board_array = [0] * num_rows
					# next line gives number of columns
					line = next(f)
					num_cols = int(line[line.index("(") + 1:line.index(")")])
					# skip until line no longer contains = new Array. also create two-dimensional array
					for i in range(num_rows):
						board_array[i] = [0] * num_rows
						line = next(f)

					# 1b) Fill board array
					for col in range(num_cols):
						for row in range(num_rows):
							obj_type = line[line.index('"') + 1: len(line)-2]
							board_array[row][col] = obj_type
							line= next(f)
					print(board_array)

	except StopIteration:	# generator running out of values when next() is used. normal. may not be needed
		pass
	except (OSError, IOError):		# python 3.3 IOError became OSError & FileNotFoundError is in OSError
		print("Could not open file to parse board")
		sys.exit(1)

def nonblank_lines(f):
	for l in f:
		line = l.rstrip()
		if line:
			yield line

get_board()
