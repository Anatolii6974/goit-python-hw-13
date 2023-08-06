import re
import sys
import shutil
import logging
import concurrent.futures
from pathlib import Path

images = []
videos = []
documents = []
music = []
archives = []
unknown = []
unknown_ext = set()

# Get the file extension
def get_ext(path):
    ext = Path(path)
    return ext.suffix[1:].upper()

def normalize(name):
    # Cyrillic into Latin
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e',
        'є': 'ye', 'ж': 'zh', 'з': 'z', 'и': 'y', 'і': 'i', 'ї': 'yi', 'й': 'y',
        'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'shch', 'ь': '', 'ю': 'yu', 'я': 'ya', 'ы': 'y',
        'э': 'e', 'ё': 'yo', 'ъ': '',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H', 'Ґ': 'G', 'Д': 'D', 'Е': 'E',
        'Є': 'Ye', 'Ж': 'Zh', 'З': 'Z', 'И': 'Y', 'І': 'I', 'Ї': 'Yi', 'Й': 'Y',
        'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
        'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch',
        'Ш': 'Sh', 'Щ': 'Shch', 'Ь': '', 'Ю': 'Yu', 'Я': 'Ya', 'Ы': 'Y',
        'Э': 'E', 'Ё': 'Yo', 'Ъ': ''
    }

    # Replace of Cyrillic characters
    for cyrillic, latin in translit_dict.items():
        name = name.replace(cyrillic, latin)

    # Substitution of characters that are not Latin and numbers with a character '_'
    name = re.sub(r'[^a-zA-Z0-9]', '_', name)    

    return name


# Parsing the folder
def sort_files(path):
    basepath = Path(path)
    for entry in basepath.iterdir():
        if entry.is_dir():
            sort_files(entry)
        else: 
            ext = get_ext(entry)
            if ext in ['JPEG', 'PNG', 'JPG', 'SVG']:
                images.append(entry)
            elif ext in ['AVI', 'MP4', 'MOV', 'MKV']:
                videos.append(entry)    
            elif ext in ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']:
                documents.append(entry)
            elif ext in ['MP3', 'OGG', 'WAV', 'AMR']:
                music.append(entry)
            elif ext in ['ZIP', 'GZ', 'TAR']:
                archives.append(entry)
            else:
                unknown.append(entry)  
                unknown_ext.add(ext)

# Remove Empty Dir
def remove_empty_directories(directory):
    directory_path = Path(directory)

    for item in directory_path.iterdir():
        if item.is_dir():
            remove_empty_directories(item)

    # Check is dir empty
    if not any(directory_path.iterdir()):
        if directory_path.name not in ['images','videos','documents','music','archives']:
            # DEL
            directory_path.rmdir()

# Copy file to specified directory
def process_file(file, target_dir):
    logging.debug(f'greeting for: {target_dir}')
    path_dist = target_dir / f'{normalize(file.name.split(".")[0])}{file.suffix}'
    # shutil.copy(file, path_dist)   
    file.replace(path_dist)    
     


# -----------------------------------------------------------------------------

def main():
    # Start parsing
    path = Path(sys.argv[1])
    print(path)
    sort_files(path)

    # Making Directories
    for dir in ['images','videos','documents','music','archives']:
        new_dir = path / dir
        new_dir.mkdir(exist_ok = True)

    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')

    # Replace files 

    with concurrent.futures.ThreadPoolExecutor() as executor:

        for file in images:
            path_dist = path / 'images'
            executor.submit(process_file, file, path_dist) 

        for file in videos:
            path_dist = path / 'videos'
            executor.submit(process_file, file, path_dist)  

        for file in documents:
            path_dist = path / 'documents'
            # process_file(file, path_dist)
            # file.replace(path_dist)  
            executor.submit(process_file, file, path_dist)   

        for file in music:
            path_dist = path / 'music'
            executor.submit(process_file, file, path_dist) 

        for file in archives:
            archives_dir = path / 'archives'
            archive_name = file.stem
            target_dir = archives_dir / archive_name
            target_dir.mkdir(parents=True, exist_ok=True)
            # shutil.unpack_archive(str(file), str(target_dir))  
            executor.submit(shutil.unpack_archive, str(file), str(target_dir))     

    remove_empty_directories(path)    

    # Print unknown extention from set
    for t in unknown_ext:
        print(f'{t}')

if __name__ == '__main__':
    main()       