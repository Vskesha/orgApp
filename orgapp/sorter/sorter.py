from colorama import init as init_colorama, Fore, Back, Style
from pathlib import Path
import re
import shutil
import sys

CYRYLIC = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюяёъы'
LATIN = (
    'a', 'b', 'v', 'h', 'g', 'd', 'e', 'ye', 'zh', 'z', 'y', 'i',
    'yi', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u',
    'f', 'kh', 'ts', 'ch', 'sh', 'sch', '', 'yu', 'ya', 'yo', '', 'y'
)

TRANS = {}
for c, l in zip(CYRYLIC, LATIN):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


IMAGES = []
VIDEO = []
DOCS = []
MUSIC = []
ARCHIVES = []
MY_OTHER = []

REGISTERED_EXTENSIONS = {
    'JPEG': IMAGES, 'PNG': IMAGES, 'JPG': IMAGES, 'SVG': IMAGES,
    'AVI': VIDEO, 'MP4': VIDEO, 'MOV': VIDEO, 'MKV': VIDEO,
    'DOC': DOCS, 'DOCX': DOCS, 'TXT': DOCS, 'PDF': DOCS, 'XLSX': DOCS, 'PPTX': DOCS,
    'MP3': MUSIC, 'OGG': MUSIC, 'WAV': MUSIC, 'AMR': MUSIC,
    'ZIP': ARCHIVES, 'GZ': ARCHIVES, 'TAR': ARCHIVES,
}

FOLDERS = []
KNOWN_EXTENSIONS = set()
UNKNOWN_EXTENSIONS = set()
SORTER_LOGO = """
 .oooooo..o                        .                     
d8P'    `Y8                      .o8                     
Y88bo.       .ooooo.  oooo d8b .o888oo  .ooooo.  oooo d8b
 `"Y8888o.  d88' `88b `888""8P   888   d88' `88b `888""8P
     `"Y88b 888   888  888       888   888ooo888  888    
oo     .d8P 888   888  888       888 . 888    .o  888    
8""88888P'  `Y8bod8P' d888b      "888" `Y8bod8P' d888b   
"""


def get_extension(file: Path) -> str:
    """
    returns uppercase extension of the given 'file'. This extension then
    will be used for determining the type of file (e.g. MUSIC, VIDEO)
    @param file: Path
    @return: str uppercase extension
    """
    return file.suffix[1:].upper()


def handle_archive(archive: Path, target_folder: Path) -> None:
    """
    unpacks given 'archive' to 'target_folder / sub_folder'
    (sub_folder named the same as archive without extension)
    Creates folders if they don't exist
    """
    if not target_folder.exists():
        target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(archive.name.replace(archive.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(archive, folder_for_file)
    except shutil.ReadError:
        print('Cannot unpack archive')
        folder_for_file.rmdir()
    archive.unlink()


def handle_file(file: Path, target_folder: Path) -> None:
    """
    Moves given 'file' to 'target_folder'. Creates 'target_folder' if it doesn't exist
    """
    if not target_folder.exists():
        target_folder.mkdir(exist_ok=True, parents=True)
    file.replace(target_folder / normalize(file.name))


def handle_folder(folder: Path) -> None:
    """
    removes given 'folder'
    """
    try:
        folder.rmdir()
    except OSError:
        print(f'Cannot remove folder "{folder}"')


def normalize(file_name: str) -> str:
    """
    makes transliteration of the given file_name to latin characters
    and replace all non-alphanumeric characters with '_'
    :param file_name: str, old file name
    :return: new file name
    """
    latin_name = file_name.translate(TRANS)
    parts = latin_name.rsplit('.', 1)
    parts[0] = re.sub(r'\W', '_', parts[0])
    return '.'.join(parts)


def sort_folder(folder: Path) -> None:
    """
    sorts files in the given 'folder' according to the REGISTERED_EXTENSIONS in 'file_parser.py'
    """
    traverse(folder)

    for file in IMAGES:
        handle_file(file, folder / 'images')

    for file in VIDEO:
        handle_file(file, folder / 'video')

    for file in DOCS:
        handle_file(file, folder / 'documents')

    for file in MUSIC:
        handle_file(file, folder / 'audio')

    for file in MY_OTHER:
        handle_file(file, folder / 'my_other')

    for archive in ARCHIVES:
        handle_archive(archive, folder / 'archives')

    for folder in FOLDERS[::-1]:
        handle_folder(folder)


def traverse(folder: Path) -> None:
    """
    recursively scans given 'folder' and:
      - adds all directories' paths to 'FOLDERS'
      - adds files' paths to proper lists (IMAGES, VIDEO, DOCS, MUSIC, ARCHIVES or MY_OTHER)
        based on file extension
      - adds all encountered extensions to KNOWN_EXTENSIONS or UNKNOWN_EXTENSIONS
        according to REGISTERED_EXTENSIONS
    @param folder: str - path to existing directory to parse
    @return: None
    """
    for element in folder.iterdir():
        if element.is_dir():
            if element.name in ('archives', 'video', 'audio', 'documents', 'images', 'my_other'):
                continue
            FOLDERS.append(element)
            traverse(element)
        else:
            ext = get_extension(element)
            if not ext:
                MY_OTHER.append(element)
            elif ext in REGISTERED_EXTENSIONS:
                KNOWN_EXTENSIONS.add(ext)
                container = REGISTERED_EXTENSIONS[ext]
                container.append(element)
            else:
                UNKNOWN_EXTENSIONS.add(ext)
                MY_OTHER.append(element)


def clean_folder():
    prepare()
    folder_to_sort = sys.argv[1] if len(sys.argv) > 1 else ''
    while True:
        path = Path(folder_to_sort).resolve()
        if not path.exists() or not path.is_dir():
            folder_to_sort = input(f'\nThere is no such folder "{folder_to_sort}"\n'
                                   f'Please enter the path to the existing folder\n'
                                   f'(enter nothing to sort current folder): {Fore.WHITE}')
        else:
            confirmation = input(
                f'\n{Fore.GREEN}Do You really want to sort {"this" if folder_to_sort else "current"} folder:\n"{path}"?\n'
                f'{Fore.RED}!!! CHANGES ARE IRREVERSIBLE !!! \n'
                f'{Fore.GREEN}type {Fore.WHITE}y / n {Fore.GREEN} or enter another path: {Fore.WHITE}')
            if confirmation.lower() == 'n':
                return
            if confirmation.lower() == 'y':
                break
            folder_to_sort = confirmation

    print(f'\nStart in folder "{path}"')
    sort_folder(path)
    print('Done')


def prepare():
    init_colorama()
    print(Fore.BLUE + Style.BRIGHT + SORTER_LOGO)
    print(f" {Fore.CYAN}                    Welcome to your sorting app!")


if __name__ == '__main__':
    clean_folder()
