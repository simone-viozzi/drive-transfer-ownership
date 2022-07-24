

from __future__ import annotations
import shutil
import os
from drive import primitives, Path
import logging
import logging.config
import json
from deepdiff import DeepDiff
from pprint import pprint


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
    
    file = univpm1.ls_single_file("/tmp/file1")
    
    #file.Rename("file1_renamed")

    #file.FetchMetadata(fields="title")
    #file["title"] = "new_file1"
    #file.Upload()

 


'''
self["title"] = new_title

self._FilesPatch(param=param)
'''


'''
if param is None:
    param = {}

if "body" not in param:
    param["body"] = {}

param['body']['title'] = new_title

file = {'title': new_title}
        
self.auth.service.files().patch(
    fileId=self["id"],
    body=file,
    fields='title').execute()
'''