
from __future__ import annotations

from pydrive2.fs import GDriveFileSystem
from pydrive2.auth import GoogleAuth
import os
import logging
import logging.config
import json


basepath = os.path.dirname(os.path.abspath(__file__))


logging_conf = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(levelname)s] %(name)s -> %(funcName)5s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}

logging.getLogger('googleapiclient.discovery').setLevel(logging.ERROR)
#logging.getLogger('drive.primitives.ls').setLevel(logging.ERROR)
logging.getLogger('drive.primitives._get_files_by_query').setLevel(logging.ERROR)


logging.config.dictConfig(logging_conf)
log = logging.getLogger()


def autenticate(name, authpath) -> GoogleAuth:
    print(f'Authenticating "{name}"...')

    gauth = GoogleAuth()

    cred_file = f"{authpath}/client_secrets.json"

    assert os.path.exists(cred_file), f"File {cred_file} not found"

    gauth.settings['client_config_file'] = cred_file
    
    cred_path = f'{authpath}/{name}/credentials.json'

    if os.path.exists(cred_path):
        log.debug('Credentials file exists')
        gauth.LoadCredentialsFile(cred_path)
        if gauth.access_token_expired:
            # Refresh them if expired
            os.remove(cred_path)
            gauth.LocalWebserverAuth()
    else:
        log.debug('Credentials file does not exist')
        os.makedirs(f"{authpath}/{name}", exist_ok=True)
        gauth.LocalWebserverAuth()
    
    gauth.SaveCredentialsFile(cred_path)

    print(f'Authenticated "{name}"')

    return gauth


if __name__ == '__main__':
    
    auth = autenticate('univpm1', f'{basepath}/auth/')

    fs = GDriveFileSystem("root", auth)

    #fs.copy('root/tmp/a.pdf', 'root/tmp/folder/', recursive=False)
    #fs.copy('root/tmp/folder1/', 'root/tmp/folder/', recursive=True)

    #a = fs.info('root/tmp/a.pdf')
    #print(a)

    #fs.mv('root/tmp/aa/b.pdf', 'root/tmp/a.pdf')
    #fs.mv('root/tmp/a.pdf', 'root/tmp/aa/b.pdf')

    fs.mv('root/tmp/a.pdf', 'root/b.pdf')

    