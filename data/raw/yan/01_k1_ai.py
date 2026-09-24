def connect_four_place(columns):
    board = [['-' for _ in range(7)] for _ in range(6)]
    is_yellow = True
    
    for col in columns:
        token = 'Y' if is_yellow else 'R'
        
        for row in range(5, -1, -1):
            if board[row][col] == '-':
                board[row][col] = token
                break
                
        is_yellow = not is_yellow
        
    return board
