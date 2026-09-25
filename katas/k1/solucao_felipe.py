# ENUNCIADO
# ---------
# Simulate placing tokens on a Connect Four board.
#
# The input is a list of integers representing the columns, from 0 to 6, where
# tokens are dropped, in order. The first player is yellow (Y), followed by red
# (R), alternating turns.
#
# Return the final state of the board after all tokens have been placed. Empty
# cells are marked with '-'. The board has 7 columns and 6 rows. Tokens fall to
# the lowest available position in the chosen column. The input list must not be
# modified. Return rows from top to bottom.


def connect_four_place(columns):
	tab = []

	for i in range(6):
		row = []
		for j in range(7):
			row.append('-')
		tab.append(row)

	is_yellow = True

	for col in columns:
		if is_yellow:
			token = 'Y'
		else:
			token = 'R'

		for row in range(5, -1, -1):
			if tab[row][col] == '-':
				tab[row][col] = token
				break

		if is_yellow:
			is_yellow = False
		else:
			is_yellow = True

	return tab
