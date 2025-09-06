import re
import regex 
import unicodedata
from datetime import datetime
from rapidfuzz import process, fuzz
from .config import provinces

COUNTRY_CODES = {
    'VNM': 'Việt Nam',
    'USA': 'United States',
    'JPN': 'Japan',
    'CHN': 'China',
    'FRA': 'France',
    'GBR': 'United Kingdom',
}

GENDER = {
    'M': 'Nam',
    'F': 'Nữ',
}

def normalize(text):
    return text.lower().replace('.', '').strip()

def correct_place_of_birth(input_text):
    match = process.extractOne(
        normalize(input_text),
        [normalize(p) for p in provinces],
        scorer=fuzz.WRatio
    )
    if match and match[1] > 60:
        return provinces[[normalize(p) for p in provinces].index(match[0])]
    return input_text

def normalize_date(date_str):
    date_str = date_str.replace(' ', '').replace('-', '/')
    date_str = re.sub(r'[^\d/]', '', date_str)
    formats = ["%d/%m/%Y", "%d/%m/%y", "%y%m%d"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except:
            pass
    return date_str

def compute_check_digit(data):
    weights = [7, 3, 1]
    total = 0
    for i, char in enumerate(data):
        if char.isdigit():
            value = int(char)
        elif char.isalpha():
            value = ord(char.upper()) - 55
        elif char == '<':
            value = 0
        else:
            return -1
        total += value * weights[i % 3]
    return str(total % 10)

def count_invalid_characters(text):
    return len(regex.findall(r'[^\p{Latin}\s]', text))

def compare_names(name1, name2):
    def remove_accents(input_str):
        nfkd = unicodedata.normalize('NFKD', input_str)
        return ''.join(c for c in nfkd if not unicodedata.combining(c)).replace('Đ', 'D').replace('đ', 'd')

    def normalize_name(name):
        name = remove_accents(name).upper().strip()
        return re.sub(r'[^A-Z ]+', '', name)
    
    return normalize_name(name1) == normalize_name(name2)
