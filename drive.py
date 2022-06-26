
import cachetools.func
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import GoogleDriveFile
import os
import json
import logging

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


export_guide = {
    "application/vnd.google-apps.document": "application/vnd.oasis.opendocument.text",
    "application/pdf": None
}


class Drive:

    def __init__(self, name, authpath, tmp_folder_name='tmp') -> None:
        self.autenticate(name, authpath)

        self.about = self.drive.GetAbout()
        self.name = self.about['name']

        self.create_tmp_folder(tmp_folder_name)

        
    def autenticate(self, name, authpath, debug=False):
        print(f'Authenticating "{name}"...', debug)

        gauth = GoogleAuth()

        cred_file = f"{authpath}/client_secrets.json"

        assert os.path.exists(cred_file), f"File {cred_file} not found"

        gauth.settings['client_config_file'] = cred_file
        
        cred_path = f'{authpath}/{name}/credentials.json'

        if os.path.exists(cred_path):
            print('Credentials file exists', debug)
            gauth.LoadCredentialsFile(cred_path)
            if gauth.access_token_expired:
                # Refresh them if expired
                os.remove(cred_path)
                gauth.LocalWebserverAuth()
        else:
            print('Credentials file does not exist', debug)
            os.makedirs(f"{authpath}/{name}", exist_ok=True)
            gauth.LocalWebserverAuth()
        
        gauth.SaveCredentialsFile(cred_path)

        print(f'Authenticated "{name}"', debug)

        self.drive: GoogleDrive = GoogleDrive(gauth)


    @cachetools.func.ttl_cache(maxsize=256, ttl=5 * 60)
    def _raw_list_files(self, query, debug=False) -> "list[GoogleDriveFile]":
        print(f"doing query: {query}", debug)
        return self.drive.ListFile({'q': query}).GetList()


    def create_tmp_folder(self, tmp_folder_name):
        tmp_query = self._raw_list_files(f"'root' in parents and trashed=false and title='{tmp_folder_name}'")
        if not tmp_query:
            self.tmp = self.drive.CreateFile({
                'title': f'{tmp_folder_name}',
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [{'id': 'root'}]
                })

            self.tmp.Upload()
        else:
            self.tmp = tmp_query[0]



    def list_files(self, path: str, folder_id='root', index=0, debug=False) -> "list[GoogleDriveFile]":
        if not path.startswith('/'):
            path = f'/{path}'
        if not path.endswith('/'):
            path = f'{path}/'

        print("\n" + "#" * 50, debug)
        print(f"list_files path {path}, index {index}", debug)

        folders = path.split('/')[:-1 or None]

        print(f"folder_id: {folder_id}", debug)
        l: "list[GoogleDriveFile]" = self._raw_list_files(f"'{folder_id}' in parents and trashed=false", debug)

        cache_path = '/'
        for folder in folders[1:index+1]:
            cache_path += f'{folder}/'
        
        if index == len(folders) - 1:
            print("exit condition", debug)
            return l

        index += 1

        next_folder = folders[index]

        print(f"next_folder {next_folder}", debug)

        for f in l:
            if f['title'] == next_folder and f['mimeType'] == 'application/vnd.google-apps.folder':
                print("recurse", debug)
                return self.list_files(path, f['id'], index, debug)
        
        raise Exception(f'Folder {next_folder} not found')


    # fatta da copilot
    def mkdir(self, path: str, debug=False) -> None:
        print(f"mkdir {path}", debug)



        self.drive.CreateFile({
            'title': path,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [{'id': 'root'}]
            }).Upload()
    

    def download(self, file: "GoogleDriveFile", path) -> None:

        if file['mimeType'] == 'application/vnd.google-apps.folder':
            os.mkdir(f"{path}/{file['title']}")
            for f in self.drive.ListFile({'q': f"'{file['id']}' in parents and trashed=false"}).GetList():
                self.download(f, f"{path}/{file['title']}")
        else:
            if file['mimeType'] not in export_guide:
                raise Exception(f"Unsupported file type: {file['mimeType']}")

            file.GetContentFile(f"{path}/{file['title']}", mimetype=export_guide[file['mimeType']])

            with open(f"{path}/{file['title']}.metadata", 'w') as f:
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