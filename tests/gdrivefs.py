
from __future__ import annotations

import json
import logging
import logging.config
import os

from pydrive2.auth import GoogleAuth
from pydrive2.fs import GDriveFileSystem

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

    fs = GDriveFileSystem("root/tmp/", auth)

    #try:
    #    fs.rm('root/tmp/folder/', recursive=True)
    #except FileNotFoundError:
    #    pass
    #fs.makedir('root/tmp/folder/')
    
    #print(fs.expand_path('root/tmp/fo1/fo2/', recursive=True))

    fs.copy('root/tmp/a.pdf', 'root/tmp/folder/', recursive=False)
    #fs.copy('root/tmp/f1/', 'root/tmp/folder/new_folder1', recursive=True)

    #a = fs.info('root/tmp/a.pdf')
    #print(a)

    #fs.mv('root/tmp/aa/a.pdf', 'root/tmp')
    #fs.mv('root/tmp/a.pdf', 'root/tmp/aa')

    #fs.mv('root/tmp/b.pdf', 'root/')
    #fs.mv('root/a.pdf', 'root/tmp/b.pdf')


    #f = fs.find('root/tmp/fo1/')
    #print(f)

    #f = fs.find('root/tmp/fo1/fo2')
    #print(f)


    #e = fs.expand_path('root/tmp/fo1/fo2', recursive=True)
    #print(e)
    