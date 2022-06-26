

import shutil
import os
from drive import Drive
import logging


basepath = os.path.dirname(os.path.abspath(__file__))




if __name__ == '__main__':
    shutil.rmtree(f'{basepath}/tmp/', ignore_errors=True)
    os.mkdir(f'{basepath}/tmp/')
    
    univpm1: Drive = Drive('univpm1', f'{basepath}/auth/')

    print("\n" + "*" * 80)
    print(f"listing files in /secondo_anno/Anno 2 Sem.2/Algebra e Logica/appunti")

    l = univpm1.list_files("/secondo_anno/Anno 2 Sem.2/Algebra e Logica/appunti",  debug=True)

    l = map(lambda f: f['title'], l)

    print(list(l))

    print("\n" + "*" * 80)
    print(f"listing files in /secondo_anno/Anno 2 Sem.2/Analisi Numerica/Moodle/soluzioni su spazi piani")

    l = univpm1.list_files("/secondo_anno/Anno 2 Sem.2/Analisi Numerica/moodle/soluzioni su spazi piani",  debug=True)

    l = map(lambda f: f['title'], l)

    print(list(l))


    #print("\n" + "*" * 80)
    #print(f"listing files in /tmp_folder/bla")
    #l = univpm1.list_files("/tmp_folder/bla", debug=True)
#
    #l = map(lambda f: f['title'], l)
#
    #print(list(l))
#
    #print("\n" + "*" * 80)
    #print(f"listing files in /tmp_folder/")
#
    #l = univpm1.list_files("/tmp_folder/", debug=True)
#
    #l = map(lambda f: f['title'], l)
#
    #print(list(l))
#
    #print("\n" + "*" * 80)
    #print(f"listing files in /")
#
    #l = univpm1.list_files("/",  debug=True)
#
    #l = map(lambda f: f['title'], l)
#
    #print(list(l))

    #print(json.dumps(univpm1.about, indent=4))


    #print("#"*50)
    #for f in l:
    #    print(f"{f['title']}, {f['ownerNames'][0]}")
    #    if f["ownerNames"][0] != univpm1.name:
    #        print("not mine")
    #        univpm1.download(f, f'{basepath}/tmp')

    