

from __future__ import annotations
import shutil
import os
from drive import primitives, Path
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


def get_titles(l: list) -> list[str]:
    r = []
    for f in l:
        r.append(f['title'])
    return r


if __name__ == '__main__':
    shutil.rmtree(f'{basepath}/tmp/', ignore_errors=True)
    os.mkdir(f'{basepath}/tmp/')
    
    univpm1: primitives = primitives('univpm1', f'{basepath}/auth/')

    print("entripoint")
    
    file = univpm1.ls_single_file("/tmp/asdf")

    b = file.GetContentIOBuffer()
    
    for l in b:
        print(l)
    
 


    