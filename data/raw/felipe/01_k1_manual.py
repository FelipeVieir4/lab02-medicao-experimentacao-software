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