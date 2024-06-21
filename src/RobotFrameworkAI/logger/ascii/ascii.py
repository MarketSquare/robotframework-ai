import os


def get_ascii_art(char):
    ascii_order = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789?!-"
    file_path = os.path.join(os.path.dirname(__file__), 'ascii.misc')
    with open(file_path, 'r') as f:
        ascii_symbols = f.read().split('\n\n')
    index = ascii_order.find(char)
    return ascii_symbols[0].split('\n')[11 * index: 11 * (index + 1)]

def string_to_ascii(str, empty_cols=0):
    ascii_art_str = [' '*empty_cols for _ in range(11)]  # Initialize with empty lines
    for char in str:
        ascii_art_char = get_ascii_art(char)
        for i in range(11):
            ascii_art_str[i] += ascii_art_char[i]  # Concatenate lines horizontally
    return ascii_art_str[:10]
