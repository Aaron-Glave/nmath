def to_num_string(characters: str) -> str:
    num_string = []
    for character in characters:
        test_character = character.upper()
        if 'Z' >= test_character >= 'A':
            num_string.append(str(ord(test_character)-ord('A')+1))
        else:
            num_string.append(character)
    return ''.join(num_string)

if __name__ == '__main__':
    print((to_num_string(input())))
