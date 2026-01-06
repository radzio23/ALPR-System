import re

# Funkcja koryguje typowe błędy OCR specyficzne dla polskich tablic.
def fix_polish_plate(text):
    text = text.strip().upper()
    text = re.sub(r'[^A-Z0-9]', '', text) 
    if len(text) < 4: return text
    text_list = list(text)

    # Mapy zamian znaków, które OCR często myli
    int_to_char = {'0': 'O', '1': 'I', '2': 'Z', '8': 'B', '5': 'S', '4': 'A', '6': 'G'}
    char_to_int = {'O': '0', 'I': '1', 'Z': '7', 'B': '8', 'S': '5', 'A': '4', 'G': '6', 'D': '0'}

    # Pierwsze dwa znaki - wyróżnik miejsca
    for i in range(min(len(text), 2)):
        if text_list[i] in int_to_char:
            text_list[i] = int_to_char[text_list[i]]

    
    # Logika dla długich tablic
    if(len(text_list) > 7):
        if text_list[0] not in ['B', 'C', 'D', 'E', 'F', 'G', 'K', 'L', 'N', 'O', 'P', 'R', 'S', 'T', 'W', 'Z']:
            text_list = text_list[1:]
        if text_list[-1] in ['L', 'I', 'E', 'R', 'J', 'Z', 'B', 'O', 'D']:
            text_list = text_list[:-1]
    
    # Ograniczenie długości
    if(len(text_list) > 8):
        text_list = text_list[:-1]

    # Zamiana liter na cyfry w części numerycznej
    for i in range(3, len(text_list)):
        if text_list[i] in ['B', 'I', 'O', 'Z', 'D']:
            text_list[i] = char_to_int[text_list[i]]

    return "".join(text_list)
