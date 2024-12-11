from zipfile import ZipFile
import os


from utils.xml import get_publication_date


WORK_DIR = 'Temp/129897758/2024_12_11_19_39_22_451403_0366200009424000037'
arc = '0366200009424000037_0.zip'
with ZipFile(os.path.join(WORK_DIR, arc)) as z:
    filelist = z.filelist

    for file in filelist:
        print(file.filename)
        print(any(file.filename.startswith(doc_type) for doc_type in ['epNotification', 'epNoticeApplicationsAbsence']))
        if any(file.filename.startswith(doc_type) for doc_type in ['epNotification', 'epNoticeApplicationsAbsence']):
            z.extract(file.filename, WORK_DIR)
            eispublicationdate = get_publication_date('notification', WORK_DIR, file.filename)
            print(eispublicationdate)
            os.unlink(os.path.join(WORK_DIR, file.filename))
