

import shutil
import os
from drive import Drive
import logging
import logging.config


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

logging.config.dictConfig(logging_conf)
log = logging.getLogger()



if __name__ == '__main__':
    shutil.rmtree(f'{basepath}/tmp/', ignore_errors=True)
    os.mkdir(f'{basepath}/tmp/')
    
    univpm1: Drive = Drive('univpm1', f'{basepath}/auth/')

    log.debug("\n" + "*" * 80)
    log.debug(f"listing files in /secondo_anno/Anno 2 Sem.2/Algebra e Logica/appunti")

    l = univpm1.list_files("/secondo_anno/Anno 2 Sem.2/Algebra e Logica/appunti")

    l = map(lambda f: f['title'], l)

    log.debug(list(l))

    log.debug("\n" + "*" * 80)
    log.debug(f"listing files in /secondo_anno/Anno 2 Sem.2/Analisi Numerica/Moodle/soluzioni su spazi piani")

    l = univpm1.list_files("/secondo_anno/Anno 2 Sem.2/Analisi Numerica/moodle/soluzioni su spazi piani")

    l = map(lambda f: f['title'], l)

    log.debug(list(l))


    #log.debug("\n" + "*" * 80)
    #log.debug(f"listing files in /tmp_folder/bla")
    #l = univpm1.list_files("/tmp_folder/bla", debug=True)
#
    #l = map(lambda f: f['title'], l)
#
    #log.debug(list(l))
#
    #log.debug("\n" + "*" * 80)
    #log.debug(f"listing files in /tmp_folder/")
#
    #l = univpm1.list_files("/tmp_folder/", debug=True)
#
    #l = map(lambda f: f['title'], l)
#
    #log.debug(list(l))
#
    #log.debug("\n" + "*" * 80)
    #log.debug(f"listing files in /")
#
    #l = univpm1.list_files("/",  debug=True)
#
    #l = map(lambda f: f['title'], l)
#
    #log.debug(list(l))

    #log.debug(json.dumps(univpm1.about, indent=4))


    #log.debug("#"*50)
    #for f in l:
    #    log.debug(f"{f['title']}, {f['ownerNames'][0]}")
    #    if f["ownerNames"][0] != univpm1.name:
    #        log.debug("not mine")
    #        univpm1.download(f, f'{basepath}/tmp')

    