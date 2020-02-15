from os.path import realpath, join, dirname
import re
CUR_DIR = dirname(realpath(__file__))
OUTPUT_DIR = join(CUR_DIR, 'extensions')
URL_EXTENSION_API = 'https://marketplace.visualstudio.com/_apis/public/gallery/publishers/{author}/vsextensions/{name}/{version}/vspackage'
CMD_LIST_EXTENSIONS = 'cmd /c code --list-extensions --show-versions'.split(' ')
CMD_VSCODE_VERSION = 'cmd /c code --version'
EXTENSION_PATTERN = re.compile(r'(?P<author>\S+?)\.(?P<ext_name>\S+?)@(?P<version>\d+\.\d+\.\d+)')
DEBUG = False
ERROR_DOWNLOADING_FILEPATH = join(CUR_DIR, 'ERROR_DOWNLOADING.json')
WAIT_SECONDS = 60
CHUNK_SIZE = 8192
