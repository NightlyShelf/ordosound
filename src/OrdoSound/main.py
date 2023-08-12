from pyfiglet import Figlet
from colorama import Fore, just_fix_windows_console
import os
import sys
from os import path, rename, chdir
from shazam import Shazam
from music_tag import load_file
from requests import get
import glob

if __name__ == '__main__':

    just_fix_windows_console()
    print(Fore.LIGHTCYAN_EX + Figlet(font='roman', width=1000).renderText('OrdoSound'))
    print(Fore.LIGHTGREEN_EX + ' by NightlyShelf ')
    print(Fore.GREEN + ' v. 1.0 MIT License 2023')
    print(Fore.WHITE + '')

    if len(sys.argv) < 2 or (len(sys.argv) > 2 and sys.argv[2].lower() != 'y' and sys.argv[2].lower() != 'n'):
        print(Fore.RED+"Error: incorrect arguments.")
        input(Fore.WHITE + "Press any key to exit...")
        sys.exit(1)
    _path = sys.argv[1]


    def fix_file(filepath):
        print(Fore.WHITE+f'File: {filepath}')
        with open(filepath, "rb") as f:
            file = f.read()
        with Shazam(file) as shazam:
            result = shazam.result
        if 'track' not in result:
            print(Fore.RED+"Error: Could not recognize track. Skipping...")
            return
        has_cover = False
        if 'images' in result["track"]:
            has_cover = True
            print(Fore.BLUE+"Cover: " + result["track"]["images"]["coverarthq"])
            url = result["track"]["images"]["coverarthq"]
            r = get(url, allow_redirects=True)
            with open('cover.jpg', 'wb') as f:
                f.write(r.content)
        title = result["track"]["title"]
        artist = result["track"]["subtitle"]
        album = result["track"]["sections"][0]["metadata"][0]["text"]
        genre = result["track"]["genres"]["primary"]

        if " - " in title:
            album = artist
            artist, title = title.split(" - ")  # Some tracks "shazaming" incorrectly

        print(Fore.YELLOW+"Title: " + title)
        print(Fore.YELLOW+"Artist: " + artist)
        print(Fore.YELLOW+"Album: " + album)
        print(Fore.BLUE+"Link: " + result["track"]["share"]["href"])

        f = load_file(filepath)
        f['tracktitle'] = title
        f['artist'] = artist
        f['genre'] = genre
        #f['albumartist'] = artist
        f['album'] = album
        f['comment'] = ''

        if has_cover:
            with open(f'cover.jpg', 'rb') as cover:
                f['artwork'] = cover.read()
            os.remove(f'cover.jpg')

            f['artwork'].first.thumbnail([64, 64])
        else:
            f['artwork'] = None
        f.save()
        print(Fore.GREEN+'Successfully applied metadata.')

        chdir(path.dirname(filepath))
        name = f'{artist} - {title}'
        bad_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in bad_chars:
            name = name.replace(char, '')
        try:

            rename(path.basename(filepath), f'{name}.mp3')
        except FileExistsError:
            i = 1
            while True:
                if not path.exists(f'{name} ({i}).mp3'):
                    rename(path.basename(filepath), f'{name} ({i}).mp3')
                    break
                else:
                    i += 1

        print(Fore.GREEN+f'Successfully renamed to {artist} - {title}.mp3.')


    if path.isdir(_path):
        print(Fore.WHITE+f"Folder: {_path}")
        if not path.exists(_path):
            print(Fore.RED+"Error: specified folder not found.")
            input(Fore.WHITE + "Press any key to exit...")
            sys.exit(1)
        if sys.argv[2].lower() == 'y':
            print(Fore.GREEN+"Recursion begin...")
            files = glob.glob(_path + '\**\*.mp3', recursive=True)
            for file in files:
                fix_file(path.abspath(file))
        else:
            files = glob.glob(_path + '\*.mp3')
            for file in files:
                fix_file(path.abspath(file))
    else:
        if not path.exists(_path):
            print(Fore.RED+"Error: specified file not found.")
            input(Fore.WHITE+"Press any key to exit...")
            sys.exit(1)
        fix_file(_path)

    print(Fore.GREEN+"Done!")