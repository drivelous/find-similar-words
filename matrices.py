

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
	"""
	Creates scoring matrix - a dictionary
	of dictionaries
	"""
	scoring = {}
	for letter_key in alphabet:
		# Creates dict as value of letter
		scoring[letter_key] = {}
		for letter_value in alphabet:
			if letter_key == '-':
				scoring[letter_key][letter_value] = dash_score
			elif letter_key == letter_value:
				scoring[letter_key][letter_value] = diag_score
			elif letter_value == '-':
				scoring[letter_key][letter_value] = dash_score
			else:
				scoring[letter_key][letter_value] = off_diag_score

	return scoring


def create_alignment_matrix(seq_x, seq_y, scoring, global_flag):
	"""
	Creates global alignment matrix
	"""
	len_x = len(seq_x)
	len_y = len(seq_y)

	alignment = [[0 for idx1 in range(len_y + 1)] for idx2 in range(len_x + 1)]

	# alters base alignment matrix to work as global alignment matrix
	if global_flag:
		for idx1 in range(1, len_x + 1):
			letter_x = seq_x[idx1 - 1]
			alignment[idx1][0] = alignment[idx1 - 1][0] + scoring[letter_x]['-']
		for idx2 in range(1, len_y + 1):
			letter_y = seq_y[idx2 - 1]
			alignment[0][idx2] = alignment[0][idx2 - 1] + scoring[letter_y]['-']
		
	return alignment


def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
	"""
	Creates either global or local alignment matrix
	depending on global_flag boolean
	"""
	len_x = len(seq_x)
	len_y = len(seq_y)
	alignment = create_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag)

	for idx1 in range(1, len_x + 1):
		for idx2 in range(1, len_y + 1):

			# Computes target square by evaluating 3 adjacent squares
			left = alignment[idx1][idx2 - 1] + scoring_matrix['-'][seq_y[idx2 - 1]]
			diagonal = alignment[idx1 - 1][idx2 - 1] + scoring_matrix[seq_x[idx1 - 1]][seq_y[idx2 - 1]]
			upper = alignment[idx1 - 1][idx2] + scoring_matrix[seq_x[idx1 - 1]]['-']
			
			# if global alignment, take max value of 3 adjacent squares
			# if local, take max value of 3 adjacent squares - must be at least 0
			if global_flag:
				alignment[idx1][idx2] = max(left, diagonal, upper)
			else:
				alignment[idx1][idx2] = max(0, left, diagonal, upper)
	
	return alignment

def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
	"""
	Compute best score of global alignment for seq_x and seq_y
	Return in form (best_score, x_alignment, y_alignment)
	"""
	idx_x = len(seq_x)
	idx_y = len(seq_y)
	score = alignment_matrix[idx_x][idx_y]
	x_pri = ''
	y_pri = ''

	while idx_x != 0 and idx_y != 0:
		current_square = alignment_matrix[idx_x][idx_y]
		if current_square == alignment_matrix[idx_x - 1][idx_y - 1] + scoring_matrix[seq_x[idx_x - 1]][seq_y[idx_y - 1]]:
			x_pri = seq_x[idx_x - 1] + x_pri
			y_pri = seq_y[idx_y - 1] + y_pri
			idx_x -= 1
			idx_y -= 1
		else:
			if current_square == alignment_matrix[idx_x - 1][idx_y] + scoring_matrix[seq_x[idx_x - 1]]['-']:
				x_pri = seq_x[idx_x - 1] + x_pri
				y_pri = '-' + y_pri
				idx_x -= 1
			else:
				x_pri = '-' + x_pri
				y_pri = seq_y[idx_y - 1] + y_pri
				idx_y -= 1

	while idx_x != 0:
		x_pri = seq_x[idx_x - 1] + x_pri
		y_pri = '-' + y_pri
		idx_x -= 1
	while idx_y != 0:
		x_pri = '-' + x_pri
		y_pri = seq_y[idx_y - 1] + y_pri
		idx_y -= 1

	return (score, x_pri, y_pri)

	

def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
	"""
	Compute best score of global alignment for seq_x and seq_y
	Return in form (best_score, x_alignment, y_alignment)
	"""
	x_pri = ''
	y_pri = ''

	score = float('-inf')
	for idx1, row in enumerate(alignment_matrix):
		for idx2, val in enumerate(row):
			if val > score:
				score = val
				idx_x = idx1
				idx_y = idx2

	while alignment_matrix[idx_x][idx_y] != 0:
		current_square = alignment_matrix[idx_x][idx_y]
		if current_square == alignment_matrix[idx_x - 1][idx_y - 1] + scoring_matrix[seq_x[idx_x - 1]][seq_y[idx_y - 1]]:
			x_pri = seq_x[idx_x - 1] + x_pri
			y_pri = seq_y[idx_y - 1] + y_pri
			idx_x -= 1
			idx_y -= 1
		else:
			if current_square == alignment_matrix[idx_x - 1][idx_y] + scoring_matrix[seq_x[idx_x - 1]]['-']:
				x_pri = seq_x[idx_x - 1] + x_pri
				y_pri = '-' + y_pri
				idx_x -= 1
			else:
				x_pri = '-' + x_pri
				y_pri = seq_y[idx_y - 1] + y_pri
				idx_y -= 1

	return (score, x_pri, y_pri)