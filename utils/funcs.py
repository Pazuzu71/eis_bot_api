import os
import re
from utils.xml import get_publication_date


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
                elif file.startswith('epProtocol'):
                    protocols.append(file)
                elif file.startswith('epNoticeApplicationsAbsence_'):
                    protocols.append(file)
                elif file.startswith('contract_'):
                    eispublicationdate = get_publication_date('contract', WORK_DIR, file)
                    contracts.append((file, eispublicationdate))
                elif file.startswith('contractProcedure_'):
                    eispublicationdate = get_publication_date('contractProcedure', WORK_DIR, file)
                    contract_procedures.append((file, eispublicationdate))
    return notifications, protocols, contracts, contract_procedures
