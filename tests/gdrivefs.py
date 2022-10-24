
from __future__ import annotations
from asyncore import read

import json
import logging
import logging.config
import os
import random

from pydrive2.auth import GoogleAuth
from pydrive2.fs import GDriveFileSystem
from pydrive2.files import GoogleDriveFile
import posixpath

import contextlib

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

def print_file_metadata(auth: GoogleAuth, path=None, file_id=None):
    assert path or file_id and not (path and file_id), "Either path or file_id must be provided"
    if path:
        fs = GDriveFileSystem(posixpath.dirname(path), auth)
        file_id = fs._get_item_id(path)
    file = GoogleDriveFile(auth, {"id": file_id})
    file.FetchMetadata(fetch_all=True)

    print(json.dumps(file.metadata, indent=4))

def create_temp_miltiaccount_tree(*accounts_names):

    auths = [
        autenticate(name, f'{basepath}/auth/') for name in accounts_names
    ]


    fss = [
        GDriveFileSystem("root/tmp/", auth) for auth in auths
    ]

    files = ["root/tmp/a", "root/tmp/b.pdf"]
    folders = ['root/tmp/temp_tree']
    for i in range(5):
        account = random.choice(fss)

        n = random.randint(0, 1)
        if n == 0:
            # Create folder
            folder_name = f"folder_{i}"
            folder_path = posixpath.join(random.choice(folders), folder_name)
            account.mkdir(folder_path)
            folders.append(folder_path)
        elif n == 1:
            # copy file
            file_path = random.choice(files)
            file_name = f"{i}_{posixpath.basename(file_path)}"
            folder_path = random.choice(folders)
            new_path = posixpath.join(folder_path, file_name)
            account.copy(file_path, new_path)


def create_temp_tree(account_name):
    auth = autenticate(account_name, f'{basepath}/auth/')

    fs = GDriveFileSystem("root/tmp/", auth)

    root = "root/tmp/temp_tree"
    try:
        fs.mkdir(root)
    except FileExistsError:
        return

    files = ["root/tmp/a", "root/tmp/b.pdf"]
    folders = [root]
    for i in range(3):

        n = random.randint(0, 1)
        if n == 0:
            # Create folder
            folder_name = f"folder_{i}"
            folder_path = posixpath.join(random.choice(folders), folder_name)
            fs.mkdir(folder_path)
            folders.append(folder_path)
        elif n == 1:
            # copy file
            file_path = random.choice(files)
            file_name = f"{i}_{posixpath.basename(file_path)}"
            folder_path = random.choice(folders)
            new_path = posixpath.join(folder_path, file_name)
            fs.copy(file_path, new_path)


if __name__ == '__main__':
    create_temp_tree('univpm1')

    auth = autenticate('univpm1', f'{basepath}/auth/')
    fs = GDriveFileSystem("root/tmp/temp_tree", auth)

    root = "root/tmp/temp_tree"
    all_dirs = [root]
    all_files = []
    for path, dirs, files in fs.walk(root):
        all_dirs.extend(posixpath.join(path, d) for d in dirs)
        all_files.extend(posixpath.join(path, f) for f in files)
    
    print("All dirs:")
    print(all_dirs)
    print("All files:")
    print(all_files)
    print()
    print("cache:")
    print(json.dumps(fs._ids_cache, indent=4))

    assert all_files and all_dirs, "No files or dirs found"
    input("waiting...")

    file = random.choice(all_files)
    file_name = posixpath.basename(file)
    parent = posixpath.dirname(file)

    all_dirs.remove(parent)
    folder = random.choice(all_dirs)


    print(f"moving file {file} to folder {folder}")
    fs.move(file, folder)

    new_folder_content: list[str] = fs.ls(folder)
    assert posixpath.join(folder, file_name) in new_folder_content, "File not moved"

    print(json.dumps(fs._ids_cache, indent=4))







    #print_file_metadata(auth, "root/tmp/a")

    #fs.cp('root/tmp/a', 'root/tmp/temp_tree/aaa')
    #print(fs.ls('root/tmp/temp_tree'))

    #print(json.dumps(
    #    fs.ls("root/tmp/", detail=True), indent=4
    #))
#
    #for path, dirs, files in fs.walk("root/tmp/", detail=True):
    #    print(f'Path: {path}')
    #    print(f'Dirs: {dirs}')
    #    print(f'Files: {files}')
    #    print()

    #print(json.dumps(fs.find("root/tmp/fo1/", detail=True), indent=4))

    #fs.change_owner("root/tmp/fo1/",)

    #with contextlib.suppress(FileNotFoundError):
    #    fs.mv("root/tmp/folder/fo2/file", "root/tmp/folder/fo1/")


    #fs.ls("root/tmp/folder/fo1/file")
#
    #id_before = fs._get_item_id("root/tmp/folder/fo1/file")
    #fs.mv("root/tmp/folder/fo1/file", "root/tmp/folder/fo2/")
#
    #try:
    #    path_after = fs._ids_cache["ids"][id_before]
    #    print(path_after)
    #    print("no error")
    #except Exception as e:
    #    print("error: ", e)
#
    #id_before = fs._get_item_id("root/tmp/folder/fo2/file")
#
    #fs.mv("root/tmp/folder/fo2/file", "root/tmp/folder/fo1/")
#
    #try:
    #    path_after = fs._ids_cache["ids"][id_before]
    #    print(path_after)
    #    print("no error")
    #except Exception as e:
    #    print("error: ", e)


