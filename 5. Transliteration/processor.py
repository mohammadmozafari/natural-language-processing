import re
__all__ = ['tg_preprocess', 'fa_preprocess', 'tg_samet', 'fa_samet', 'get_samet_pairs']

__fa = {
    'تط': 't',
    'سثص': 's',
    'ق': 'v',
    'غ': 'q',
    'ضذزظ': 'z',
    'حه': 'h',
    'ب': 'b',
    'پ': 'p',
    'ج': 'j',
    'چ': 'c',
    'خ': 'x',
    'د': 'd',
    'ر': 'r',
    'ژ': 'i',
    'ش': 'u',
    'ع': 'a',
    'ف': 'f',
    'ک': 'k',
    'گ': 'g',
    'ل': 'l',
    'م': 'm',
    'ن': 'n',
    'آاوی': None

}

__tg = {
    'т': 't',
    'с': 's',
    'қ': 'v',    
    'ғ': 'q',
    'з': 'z',
    'ҳ': 'h',
    'б': 'b',
    'п': 'p',
    'ҷ': 'j',
    'ч': 'c',
    'х': 'x',
    'д': 'd',
    'р': 'r',
    'ж': 'i',
    'ш': 'u',
    'ъ': 'a',
    'ф': 'f',
    'к': 'k',
    'г': 'g',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'овяюёйеаиуўӯ': None
}


def make_trans(trans_dic):
    converted_dic = {}
    for key, val in trans_dic.items():
        for char in key:
            converted_dic[char] = val
    return str.maketrans(converted_dic)

tg_trans = make_trans(__tg)
fa_trans = make_trans(__fa)



ALL_YA = 'ئیيى'
K = 'كک'
V = 'ؤو'
A = 'إاأ'
H = 'ۀة'
HAMZE = 'ء'
ALLAH = 'ﷲ'
SEPRATOR = ',|،'
__fa_preprocess = {
    ('ً', 'ٌ', 'ٍ', 'َ', 'ُ', 'ِ', 'ّ', 'ْ'): None,
    ALL_YA: 'ی',
    K: 'ک',
    V: 'و',
    A: 'ا',
    ALLAH: 'لله',
    H: 'ه',
    SEPRATOR: ' ',
    '\xa0': None,
    '…': None,
    HAMZE: None
}
__tg_preprocess = {
    SEPRATOR: ' ',
    '…': None
}

fa_preprocess_trans = make_trans(__fa_preprocess)
tg_preprocess_trans = make_trans(__tg_preprocess)

def tg_preprocess(text: str):
    output = text.lower().translate(tg_preprocess_trans).strip('-\n\t ')
    return output

def fa_preprocess(text: str):
    return text.translate(fa_preprocess_trans).strip('-\n\t \u200c')

def tg_samet(text: str):
    return text.lower().translate(tg_trans)

def fa_samet(text:str):
    NIM_SPACE = '\u200c'
    H = 'ه'
    text = re.sub(f'{H}(\s|{NIM_SPACE})', r'\1', text)
    return text.replace('ه ', ' ').translate(fa_trans)

def get_samet_pairs(times=1):
    return_values = []
    for tg_key, fa_key, val in zip(__tg.keys(), __fa.keys(), __tg.values()):
        if val is None:
            continue
        for fa_key_char in fa_key:
            new_element = tg_key, fa_key_char
            return_values.append(new_element)
    return return_values * times
        