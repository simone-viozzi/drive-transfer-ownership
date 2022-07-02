

import shutil
import os
from drive import primitives
import logging
import logging.config
import json


basepath = os.path.dirname(os.path.abspath(__file__))


logging_conf = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(levelname)s] %(name)s: %(message)s'
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
logging.getLogger('drive.primitives.ls').setLevel(logging.ERROR)
logging.getLogger('drive.primitives._raw_ls').setLevel(logging.ERROR)


logging.config.dictConfig(logging_conf)
log = logging.getLogger()



if __name__ == '__main__':
    shutil.rmtree(f'{basepath}/tmp/', ignore_errors=True)
    os.mkdir(f'{basepath}/tmp/')
    
    univpm1: primitives = primitives('univpm1', f'{basepath}/auth/')

    l = univpm1.ls('/tmp/')
    print(l)


    #f = univpm1.drive.CreateFile({'id': 'root'})
#
    #f.FetchMetadata()
    #print(json.dumps(f.metadata, indent=4))


    