def balance(left, right):
    w_left = left.count('!') * 2 + left.count('?') * 3
    w_right = right.count('!') * 2 + right.count('?') * 3
    
    if w_left > w_right:
        return "Left"
    elif w_right > w_left:
        return "Right"
    else:
        return "Balance"
