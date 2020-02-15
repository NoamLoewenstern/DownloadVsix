import os
from os.path import join, isdir, exists, basename
import subprocess
import logging
import json
from time import sleep
import requests
from progress.bar import Bar
from constants import OUTPUT_DIR, URL_EXTENSION_API, CMD_LIST_EXTENSIONS, \
    EXTENSION_PATTERN, DEBUG, ERROR_DOWNLOADING_FILEPATH, WAIT_SECONDS, CHUNK_SIZE
from vscode_extensions import VSCodeExtensions

def init() -> None:
    if not isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s | %(levelname)s | %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S')




def fetch_and_save_extensions_as_vsix(extensions: list) -> dict:
    error_downloading = {}
    for extension in extensions:
        author, ext_name, version = (match_obj := EXTENSION_PATTERN.match(extension)) \
            and match_obj.groups() or ()
        vsix_filename = f'{author}.{ext_name}-{version}.vsix'
        vsix_filepath = join(OUTPUT_DIR, vsix_filename)
        if exists(vsix_filepath) and not DEBUG:
            logging.info(f'Already Exists {vsix_filename}')
            continue
        logging.info(f'Downloading {vsix_filename}')
        url = URL_EXTENSION_API.format(author=author, name=ext_name, version=version)
        with requests.get(url, stream=True) as resp:
            content_length = int(resp.headers['Content-length'])
            print(f'{content_length=}')
            if content_length < 500:
                logging.error(f'{vsix_filename} with url: {url}')
                error_downloading[vsix_filename] = {
                    'filename': f'{author}.{ext_name}-{version}.vsix',
                    'author': author,
                    'ext_name': ext_name,
                    'version': version,
                    'url': url,
                }
                continue
            progress_bar = Bar('Downloading', max=int(content_length // CHUNK_SIZE) + 1)
            resp.raise_for_status()
            with open(vsix_filepath, 'wb') as fh_new_ext:
                for chunk in resp.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk: # filter out keep-alive new chunks
                        fh_new_ext.write(chunk)
                        progress_bar.next()
                print()
    return error_downloading


def main():
    init()
    vscode_ext=VSCodeExtensions()
    list_extensions=vscode_ext.get_list_installed_extensions()
    while error_downloading := fetch_and_save_extensions_as_vsix(list_extensions):
        with open(ERROR_DOWNLOADING_FILEPATH, 'w') as f:
            f.write(json.dumps(error_downloading))
        sleep(WAIT_SECONDS)
        logging.info(f"some extensions didn't manage to download. sleeping for {WAIT_SECONDS} min.")
    print('finished!')



if __name__ == '__main__':
    main()
