from __future__ import annotations


import cachetools.func
import cachetools
from cachetools import cached
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import GoogleDriveFile
import os
import json
import logging

from .exceptions import FolderNotFound, FolderAlreadyExist, FolderNotEmpty



log = logging.getLogger(__name__)

      
"""
{
    "kind": "drive#file",
    "id": "1_lK6PhWHFjIfKevhKQCgve-DtJHKSf3a",
    "etag": "\"MTY1NjE2MjY0NzAzNg\"",
    "selfLink": "https://www.googleapis.com/drive/v2/files/1_lK6PhWHFjIfKevhKQCgve-DtJHKSf3a",
    "alternateLink": "https://drive.google.com/drive/folders/1_lK6PhWHFjIfKevhKQCgve-DtJHKSf3a",
    "embedLink": "https://drive.google.com/embeddedfolderview?id=1_lK6PhWHFjIfKevhKQCgve-DtJHKSf3a",
    "iconLink": "https://drive-thirdparty.googleusercontent.com/16/type/application/vnd.google-apps.folder+shared",
    "title": "bla",
    "mimeType": "application/vnd.google-apps.folder",
    "labels": {
        "starred": false,
        "hidden": false,
        "trashed": false,
        "restricted": false,
        "viewed": true
    },
    "copyRequiresWriterPermission": false,
    "createdDate": "2022-06-25T12:24:15.266Z",
    "modifiedDate": "2022-06-25T13:10:47.036Z",
    "modifiedByMeDate": "2022-06-25T13:10:34.258Z",
    "lastViewedByMeDate": "2022-06-25T13:01:58.034Z",
    "markedViewedByMeDate": "1970-01-01T00:00:00.000Z",
    "sharedWithMeDate": "2022-06-25T13:10:47.171Z",
    "version": "6",
    "sharingUser": {
        "kind": "drive#user",
        "displayName": "simone viozzi",
        "picture": {
            "url": "https://lh3.googleusercontent.com/a-/AOh14GhUIG-84Lq_qYOlWSphia5-1oJ4qHjg3E2O1KKUAA=s64"
        },
        "isAuthenticatedUser": false,
        "permissionId": "00173786927897941269",
        "emailAddress": "viozzis333@gmail.com"
    },
    "parents": [
        {
            "kind": "drive#parentReference",
            "id": "1d8MdVX6EPovRw-Diw2K8rxBPqs1O8SSJ",
            "selfLink": "https://www.googleapis.com/drive/v2/files/1_lK6PhWHFjIfKevhKQCgve-DtJHKSf3a/parents/1d8MdVX6EPovRw-Diw2K8rxBPqs1O8SSJ",
            "parentLink": "https://www.googleapis.com/drive/v2/files/1d8MdVX6EPovRw-Diw2K8rxBPqs1O8SSJ",
            "isRoot": false
        }
    ],
    "userPermission": {
        "kind": "drive#permission",
        "etag": "\"Y-tQxHMNePgYDkYPDQHF0zIgD18\"",
        "id": "me",
        "selfLink": "https://www.googleapis.com/drive/v2/files/1_lK6PhWHFjIfKevhKQCgve-DtJHKSf3a/permissions/me",
        "role": "writer",
        "type": "user",
        "pendingOwner": false
    },
    "quotaBytesUsed": "0",
    "ownerNames": [
        "simone viozzi"
    ],
    "owners": [
        {
            "kind": "drive#user",
            "displayName": "simone viozzi",
            "picture": {
                "url": "https://lh3.googleusercontent.com/a-/AOh14GhUIG-84Lq_qYOlWSphia5-1oJ4qHjg3E2O1KKUAA=s64"
            },
            "isAuthenticatedUser": false,
            "permissionId": "00173786927897941269",
            "emailAddress": "viozzis333@gmail.com"
        }
    ],
    "lastModifyingUserName": "simone viozzi",
    "lastModifyingUser": {
        "kind": "drive#user",
        "displayName": "simone viozzi",
        "picture": {
            "url": "https://lh3.googleusercontent.com/a-/AOh14GhUIG-84Lq_qYOlWSphia5-1oJ4qHjg3E2O1KKUAA=s64"
        },
        "isAuthenticatedUser": false,
        "permissionId": "00173786927897941269",
        "emailAddress": "viozzis333@gmail.com"
    },
    "capabilities": {
        "canCopy": false,
        "canEdit": true
    },
    "editable": true,
    "copyable": false,
    "writersCanShare": true,
    "shared": true,
    "explicitlyTrashed": false,
    "appDataContents": false,
    "spaces": [
        "drive"
    ]
}
"""

"""
"exportFormats": [
        {
            "source": "application/vnd.google-apps.document",
            "targets": [
                "application/rtf",
                "application/vnd.oasis.opendocument.text",
                "text/html",
                "application/pdf",
                "application/epub+zip",
                "application/zip",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "text/plain"
            ]
        },
        {
            "source": "application/vnd.google-apps.spreadsheet",
            "targets": [
                "application/x-vnd.oasis.opendocument.spreadsheet",
                "text/tab-separated-values",
                "application/pdf",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "text/csv",
                "application/zip",
                "application/vnd.oasis.opendocument.spreadsheet"
            ]
        },
        {
            "source": "application/vnd.google-apps.jam",
            "targets": [
                "application/pdf"
            ]
        },
        {
            "source": "application/vnd.google-apps.script",
            "targets": [
                "application/vnd.google-apps.script+json"
            ]
        },
        {
            "source": "application/vnd.google-apps.presentation",
            "targets": [
                "application/vnd.oasis.opendocument.presentation",
                "application/pdf",
                "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                "text/plain"
            ]
        },
        {
            "source": "application/vnd.google-apps.form",
            "targets": [
                "application/zip"
            ]
        },
        {
            "source": "application/vnd.google-apps.drawing",
            "targets": [
                "image/svg+xml",
                "image/png",
                "application/pdf",
                "image/jpeg"
            ]
        },
        {
            "source": "application/vnd.google-apps.site",
            "targets": [
                "text/plain"
            ]
        }
    ],
"""
cache = cachetools.LRUCache(maxsize=1024, getsizeof=len)

export_guide = {
    "application/vnd.google-apps.document": "application/vnd.oasis.opendocument.text",
    "application/pdf": None
}

class Path(str):

    def __new__(cls, path):
        return str.__new__(cls, path)

    def __init__(self, path):
        self.path = Path.split_path(path)
        self.path_str = path

    def __getitem__(self, s: int | slice) -> str | list:
        if isinstance(s, slice):
            s.indices
            start, stop, step = s.indices(len(self))
            if step is not None and step != 1:
                raise ValueError("step not supported")
            return self.path[start:stop]
        elif isinstance(s, int):
            return self.path[s]
        elif isinstance(s, tuple):
            raise NotImplementedError('Tuple as index')
        else:
            raise TypeError('Invalid argument type: {}'.format(type(s)))

    def __len__(self):
        return len(self.path)

    def __repr__(self):
        return self.path_str

    def __str__(self):
        return self.path_str

    def __iter__(self):
        return iter(self.path)

    def __eq__(self, other):
        return super().__eq__(other)
    
    def __hash__(self):
        return super().__hash__()
    
    def get_partial(self, i: int) -> str:
        if i > 0: i+=1

        if i > len(self) or i < -len(self)+1:
            raise IndexError('Index out of range')

        return Path.join_path(self.path[:i])

    @staticmethod
    def check_path(path: str) -> str:
        path = path.rstrip('/')
        if not path.startswith('/'):
            path = f'/{path}'
        return path

    @staticmethod
    def split_path(path: str) -> list[str]:
        """split path in a list like:
        /aa/bb/ -> ['/', 'aa', 'bb']
        / -> ['/']

        Args:
            path (str): the path to split

        Returns:
            list[str]: the path split in a list
        """
        path = Path.check_path(path)

        if path == '/':
            return ['/']
        else:
            l = path.split('/')
            l[0] = '/'
            return l


    @staticmethod
    def join_path(splitted_path: list[str]) -> Path:
        """join a splitted path in a path
        ['/', 'aa', 'bb'] -> /aa/bb
        ['/'] -> /
        """

        return Path('/' + '/'.join(splitted_path[1:]))


class primitives:
    def __init__(self, name, authpath, tmp_folder_name='tmp') -> None:
        self.autenticate(name, authpath)

        self.about = self.drive.GetAbout()
        self.name = self.about['name']

        # the temp folder will be used to load thing before moving 
        # them to their final destination
        #self.create_tmp_folder(tmp_folder_name)

        
    def autenticate(self, name, authpath) -> None:
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

        self.drive: GoogleDrive = GoogleDrive(gauth)

    
    def _get_files_by_query(self, query: str) -> "list[GoogleDriveFile]":
        log = logging.getLogger(f"{__name__}._get_files_by_query")
        log.debug(f"doing query: {query}")
        return self.drive.ListFile({'q': query}).GetList()

     
    def _get_file_by_id(self, id: str) -> "GoogleDriveFile":
        f = self.drive.CreateFile({'id': id})
        f.FetchMetadata()
        return f

    def create_tmp_folder(self, tmp_folder_name):
        self.tmp = self.mkdir(f"/{tmp_folder_name}", exist_ok=True)


    @cached(cache, key=lambda self, path: path)
    def ls(self, path) -> list[GoogleDriveFile]:
        log = logging.getLogger(f"{__name__}.ls")

        path = Path(path)

        log.debug("#"* 50)
        log.debug(f"ls in {path}")
        
        folder_id = 'root'
        file_list: list[GoogleDriveFile] = []
        for i in range(len(path)):
            partial_path = path.get_partial(i)

            log.debug(f"listing {partial_path}, i: {i}")

            try:
                file_list = cache[partial_path]
                log.debug(f"{partial_path} is in cache")
            except KeyError:
                log.debug(f"{partial_path} is not in cache")
                file_list = self._get_files_by_query(
                    f"'{folder_id}' in parents and trashed=false"
                )

                try:
                    cache[partial_path] = file_list
                except ValueError:
                    pass  # value too large
            
            if i < len(path) - 1:
                log.debug(f"looking for {path[i+1]}")
                folder_id = None
                for file in file_list:
                    if file['title'] == path[i+1] and file['mimeType'] == 'application/vnd.google-apps.folder':
                        folder_id = file['id']
                        break
                if folder_id is None:
                    raise FileNotFoundError(f"{path.get_partial(i+1)} not found")
            else:
                break

        return file_list


    def ls_single_file(self, path) -> "GoogleDriveFile":
        log = logging.getLogger(f"{__name__}.ls_single_file")

        path = Path(path)
        log.debug(f"path: {path}")

        if len(path) == 1:
            return self._get_file_by_id('root')

        parent = path.get_partial(-1)

        file_list = self.ls(parent)

        for f in file_list:
            if f['title'] == path[-1]:
                return f

        raise FileNotFoundError(f"file {path} not found")


    def mkdir(
        self,
        path: str, exist_ok=False,
        make_parents=False,
    ) -> "GoogleDriveFile":
        """create a folder in path

        Args:
            path (str): the path to the folder, es: /folder/subfolder/newfolder
            exist_ok (bool, optional): if false and the folder exist will give error. Defaults to False.

        Raises:
            FolderAlreadyExist: if the folder exist and exist_ok = False

        Returns:
            GoogleDriveFile: the new folder
        """
        log.debug(f"#" * 50)
        path = Path(path)

        log.debug(f"mkdir {path}")

        folders = path.split('/')
        folders[0] = '/'
        folders = [f for f in folders if f]

        folder_name = folders[-1]
        parent_name = folders[-2] if len(folders) > 1 else '/'

        log.debug(f"folder_name {folder_name}, parent_name {parent_name}")

        partent_path = '/' + '/'.join(folders[1:-1])

        log.debug(f"partent_path {partent_path}")

        last_parent = None
        try:
            for f in self.old_ls(partent_path):
                if f['title'] == folder_name and f['mimeType'] == 'application/vnd.google-apps.folder':
                    log.debug(f"folder {folder_name} already exists")
                    if exist_ok:
                        return f
                    else:
                        raise FolderAlreadyExist(path)
        except FolderNotFound:
            log.debug(f"folder {partent_path} does not exist")
            if make_parents:
                for i in range(len(folders) - 1):
                    partial_path = '/' + '/'.join(folders[1:i+1])
                    log.debug(f"recurse path {partial_path}")
                    last_parent = self.mkdir(partial_path, exist_ok=True, make_parents=True)
            else:
                # TODO change exception
                raise FolderNotFound(partent_path)

        parent_id = None
        if last_parent:
            parent_id = last_parent['id']
        else:
            # TODO avoid this as much as possible!
            log.debug(f"trowing away the cache")
            cache.clear()
            parent_id = self.old_ls(partent_path, get_folder=True)[0]['id']
        
        log.debug(f"creating folder {path}")
     
        log.debug(f"parent_id {parent_id}")

        f = self.drive.CreateFile({
            'title': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [{'id': parent_id}]
        })

        f.Upload()

        return f


    def rm(self, file: "GoogleDriveFile", recursive=False):
        """delete a file or folder

        Args:
            file (GoogleDriveFile): the file / folder to delete
            recursive (bool, optional): if true the whole subtree under file will be deleted. Defaults to False.

        Raises:
            FolderNotEmpty: if you delete a non empty folder and recursive = False
        """        

        if file['mimeType'] == 'application/vnd.google-apps.folder':
            if recursive:
                # only delete a folder if is explicitly asked
                file.Trash()
            else: 
                l = self._get_files_by_query(f"'{file['id']}' in parents and trashed=false")
                if len(l) > 0:
                    raise FolderNotEmpty(file['title'])
                else:
                    # if the folder is empty, delete it
                    file.Trash()
        else:
            # if is a file, delete it
            file.Trash()


    def cp(self, src_path, dst_path, new_name = None):
        """copy a file or folder

       
        """
        self.check_path(src_path)
        self.check_path(dst_path)

        log.debug(f"#" * 50)

        log.debug(f"cp {src_path} {dst_path}")

        folder = self.ls(dst_path, get_folder=True)[0]

        try:
            folder = self.ls(src_path, get_folder=True)[0]
            log.debug("it's a folder!")

            old_name = folder['title']

            log.debug(f"copying folder {old_name}")

            new_folder_path = f"{dst_path}/{new_name or old_name}"

            log.debug(f"new_folder_path {new_folder_path}")

            folder = self.mkdir(new_folder_path)

            for f in self.ls(src_path):
                self.cp(f"{src_path}/{f['title']}", new_folder_path)


        except FolderNotFound:
            file = self.ls(src_path, get_folder=False)[0]

            log.debug("it's a file!")
            log.debug(f"copying file {file[0]['title']}")
  
            file.Copy(folder, new_name)

            
            
    # make the input take a path
    def download(self, file: "GoogleDriveFile", download_path) -> None:
        """download a file into a local path. 
        if the file is a folder download recurdively it's content

        Args:
            file (GoogleDriveFile): the file to download
            download_path (str): the local path where to download the file

        Raises:
            TODO: #2 specialize the exception
            Exception: if the format of the file is not recognized
        """        

        if file['mimeType'] == 'application/vnd.google-apps.folder':
            os.mkdir(f"{download_path}/{file['title']}")

            # use ls instead
            for f in self._get_files_by_query(f"'{file['id']}' in parents and trashed=false"):
                self.download(f, f"{download_path}/{file['title']}")
        else:
            if file['mimeType'] not in export_guide:
                #2
                raise Exception(f"Unsupported file type: {file['mimeType']}")

            file.GetContentFile(f"{download_path}/{file['title']}", mimetype=export_guide[file['mimeType']])

            with open(f"{download_path}/{file['title']}.metadata", 'w') as f:
                json.dump(file.metadata, f, indent=4)


    # fatta da copilot
    def upload(self, path: str, folder_id='root') -> None:
        if not os.path.exists(path):
            raise Exception(f'Path {path} does not exist')

        if os.path.isdir(path):
            #os.makedirs(f"{basepath}/{path}", exist_ok=True)
            for f in os.listdir(path):
                self.upload(f"{path}/{f}", folder_id)
        else:
            file = self.drive.CreateFile({
                'title': os.path.basename(path),
                'parents': [{'id': folder_id}]
                })

            file.SetContentFile(path)
            file.Upload()

            with open(f"{path}.metadata", 'w') as f:
                json.dump(file.metadata, f, indent=4)
                

    
