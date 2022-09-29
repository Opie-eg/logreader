import hashlib

def verify(key,name):
    global score
    score = 0

    # encontra o check digit
    check_digit = key[2]
    check_digit_count = 0

    #aafa-bbfb-cccc-ddfd-1111
    # separa o conteudo
    chunks = key.split('-')
    if len(chunks) == 6:
        hash=chunks.pop()
        name_veri = hashlib.sha1(name.encode())
        if hash == name_veri:
            name_result = True
    else:
        return False
    
    # verifica cada bloco
    for chunk in chunks:
        if len(chunk) != 4:
            return False

        for char in chunk:
            if char == check_digit:
                check_digit_count += 1
            # calcula o score para os characteres
            score += ord(char)

    # verifica se o score está em valores aceitaveis
    if score > 1700 and score < 1800 and check_digit_count == 3 and name_result == True:
        return True
    else:
        return False

