from pyfiglet import Figlet
from colorama import just_fix_windows_console, Fore
from os import path, walk
from shazam import Shazam
from music_tag import load_file
import requests

'''
# Header
just_fix_windows_console()
print(Fore.LIGHTCYAN_EX + Figlet(font='small').renderText('ORDOSOUND'))
print(Fore.LIGHTGREEN_EX + ' by NightlyShelf ')
print(Fore.GREEN + ' v. 1.0 MIT License 2023')
print(Fore.WHITE + '<==============================================>')


# Displaying error
def display_error(error_text, critical=False, error_code=1):
    print(Fore.RED + 'Error: ' + error_text)
    if critical:
        exit(error_code)


# Displaying warning
def display_warning(warning_text):
    print(Fore.YELLOW + 'Warning: ' + warning_text)


# File searching
def find_files(file, search_path) -> []:
    result = []
    for root, dir, files in walk(search_path):
        if file in files:
            result.append(path.join(root, file))
    return result


# Selecting working directory
dest = input('Enter the working directory: ')
if not path.exists(dest):
    display_error(f'"{dest}" does not exist.', True, 2)
if path.isfile(dest):
    display_error(f'"{dest}" is not a directory.', True, 2)


# Checking configs
if not input(Fore.BLUE + 'Skip searching configs? (y/N)') == 'y':
    print(Fore.WHITE+ 'Searching for config...')
    configs = []
    selected_config = ""
    isNew = False
    try:
        configs = find_files('ordomusic.json')
    except Exception as ex:
        display_error(ex.args[1], True, ex.args[0])

    # Multiple configs check
    if len(configs) > 1:
        display_warning('Multiple configs found. Please select which one to use or enter "N" to create the new one or '
                        'enter "S" to skip: ')
        configs_list = ''
        for i in range(len(configs)):
            configs += f'[{i}]: "{configs[i]}"{";" if i != len(configs)-1 else ":"} '

        # Using infinity loop to select correct variant
        while True:
            selected = input(configs_list)
            if selected == 'N':
                # New Config
                isNew = True
                while True:
                    new_config = input('Enter the path for new config or leave blank to use root directory (recommended): ')
                    if new_config == '':
                        new_config = path.join(dest, 'ordomusic.json')
                        try:
                            open(new_config, 'w').close()
                            break
                        except Exception as ex:
                            display_error(ex.args[1], False, ex.args[0])

                    else:
                        if not path.exists(new_config):
                            display_warning(f'Path "{new_config}" does not exist. Please select another path.')
                        else:
                            new_config = path.join(new_config, 'ordomusic.json')
                            try:
                                open(new_config, 'w').close()
                                break
                            except Exception as ex:
                                display_error(ex.args[1], False, ex.args[0])
                break

'''
with open('E:\муз\БИ 2\Bi-2 - Молитва (Из кф Молитва).mp3','rb') as f:
    file = f.read()
with Shazam(file) as shazam:
    result = shazam.result
for item in result["track"]["genres"]["primary"]:
    print(item)
'''print(result["track"]["images"]["coverarthq"])
url = result["track"]["images"]["coverarthq"]
r = requests.get(url, allow_redirects=True)
with open('cover.jpg','wb') as f:
    f.write(r.content)
print("Title: "+result["track"]["title"])
print("Artist: "+result["track"]["subtitle"])
print("Album: "+result["track"]["sections"][0]["metadata"][0]["text"])

f = load_file('')
f['tracktitle'] = result["track"]["title"]
f['artist'] = result["track"]["subtitle"]
f['album'] = result["track"]["sections"][0]["metadata"][0]["text"]
with open('cover.jpg','rb') as cover:
    f['artwork'] = cover.read()

f['artwork'].first.thumbnail([64,64])
f.save()
'''