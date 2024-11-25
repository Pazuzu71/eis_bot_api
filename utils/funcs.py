import os
import re
import xml.etree.ElementTree as ET


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


def get_docs_dates(WORK_DIR):
    notifications, protocols, contracts, contract_procedures = [], [], [], []
    for path, dirs, files in os.walk(WORK_DIR):
        if files:
            for file in files:
                if file.startswith('epNotification'):
                    notifications.append(file)
                if file.startswith('epProtocol'):
                    protocols.append(file)
                if file.startswith('epNoticeApplicationsAbsence_'):
                    protocols.append(file)
                if file.startswith('contract_'):
                    contracts.append(file)
                if file.startswith('contractProcedure_'):
                    contract_procedures.append(file)
    return notifications, protocols, contracts, contract_procedures
