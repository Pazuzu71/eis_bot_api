import os
import re


def create_dir(DIR):
    if not os.path.exists(DIR):
        os.mkdir(DIR)


def find_subsystemType(eisdocno: str):
    eisdocno = eisdocno.strip()
    if re.fullmatch(r'\d{19}', eisdocno) and eisdocno.startswith('0'):
        return 'PRIZ'
    elif re.fullmatch(r'\d{19}', eisdocno) and not eisdocno.startswith('0'):
        return 'RGK'
    elif re.fullmatch(r'\d{18}', eisdocno):
        return 'RPGZ'
    elif re.fullmatch(r'\d{23}', eisdocno):
        return 'RPEC'
