def to_nato(words):
    alphabet = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
        'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
        'U', 'V', 'W', 'X', 'Y', 'Z'
    ]

    nato = [
        'Alfa', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot',
        'Golf', 'Hotel', 'India', 'Juliett', 'Kilo', 'Lima',
        'Mike', 'November', 'Oscar', 'Papa', 'Quebec', 'Romeo',
        'Sierra', 'Tango', 'Uniform', 'Victor', 'Whiskey',
        'Xray', 'Yankee', 'Zulu'
    ]

    result = []

    for char in words:
        if char == ' ':
            continue

        char = char.upper()

        if char in alphabet:
            position = alphabet.index(char)
            result.append(nato[position])
        else:
            result.append(char)

    return " ".join(result)