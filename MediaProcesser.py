import re
import os
import datetime
from PIL import Image
import piexif
import os


def extract_date(filename):
    global prev
    for pattern in regex_patterns:
        match = re.search(pattern, filename)
        if match:
            date_str = match.group(1)
            date_str = re.sub(r'\D', '', date_str)
            print(date_str)
            if prev is not pattern:
                print("*****************new*****************************")
            prev = pattern
            if len(date_str) >= 10 and date_str.isdigit() and 946684800 <= int(date_str[:10]) <= 1893456000:
                return datetime.datetime.utcfromtimestamp(int(date_str[:10]))
            else:
                date_format = pattern_to_date_format.get(len(date_str))
                if date_format is None and len(date_str) > 8:
                    date_str = date_str[:8]
                    date_format = pattern_to_date_format.get(len(date_str))
                return datetime.datetime.strptime(date_str, date_format)

    print(f"No match for: {filename}")
    return None


def get_exif_date(file_path):
    try:
        img = Image.open(file_path)
        exif_data = img._getexif()
        if exif_data and 36867 in exif_data:
            exif_date = datetime.datetime.strptime(
                exif_data[36867], '%Y:%m:%d %H:%M:%S')
            return exif_date
    except Exception as e:
        print(f"Error while processing {file_path}: {e}")
    return None


def process_file(file_path, file_date):
    exif_date = get_exif_date(file_path)
    if exif_date and file_date.date() != exif_date.date():
        return True
    elif exif_date is None:
        return True
    print('Date already correct:')
    return False


def update_exif_date(file_path, new_date):
    try:
        img = Image.open(file_path)

        # Check if the image has EXIF data
        if 'exif' in img.info:
            exif_data = piexif.load(img.info['exif'])
        else:
            # Create a new, empty EXIF data dictionary
            exif_data = {'0th': {}, 'Exif': {}, 'GPS': {},
                         'Interop': {}, '1st': {}, 'thumbnail': None}

        # Update the DateTimeOriginal (tag 36867) in the Exif IFD
        exif_data['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_date.strftime(
            '%Y:%m:%d %H:%M:%S').encode('utf-8')

        # Save the modified image with the updated EXIF data
        exif_bytes = piexif.dump(exif_data)
        img.save(file_path, exif=exif_bytes)
    except Exception as e:
        print(f"Error while updating EXIF data in {file_path}: {e}")


def sorting_key(filename):
    for index, pattern in enumerate(regex_patterns):
        if re.search(pattern, filename):
            return index
    return len(regex_patterns)


def move_file(file, root, directory):
    # Get the relative path within the original directory
    relative_path = os.path.relpath(root, directory)

    # Create the corresponding directories in the output directory
    output_subdir = os.path.join(output_dir, relative_path)
    if not os.path.exists(output_subdir):
        os.makedirs(output_subdir)

    # Move the file to the new directory, maintaining the folder structure
    output_file_path = os.path.join(output_subdir, file)
    os.rename(file_path, output_file_path)
    return output_file_path


directory = 'D:\\Mi10T'
output_dir = 'D:\\Sorted'
prev = ''

notchanged = []

regex_patterns = [
    r"IMG_(\d{8})_(\d{6})\.jpg",
    r"(\d{8})_(\d{6})\.jpg",
    r"^(\d{13})\.jpg",
    r"\d{5}sPORTRAIT_\d{5}_BURST(\d{17})_COVER\.jpg",
    r"IMG-(\d{8})-WA\d{4}\.jpg",
    r"\d{5}PORTRAIT_\d{5}_BURST(\d{17})\.jpg",
    r"IMG_(\d{8})_(\d{9})\.jpg",
    r"(\d{4}-\d{2}-\d{2} \d{2}\.\d{2}\.\d{2})\.jpg",
    r"IMG_(\d{4})\.JPG",
    r"B\d{3}_(\d{8})_(\d{6})\.jpg",
    r"FJIMG_(\d{8})_(\d{6})\.jpg",
    r"IMG_(\d{8})_(\d{6})-\d{2}\.jpeg",
    r"(\d{8})_(\d{6})\.mp\d",
    r"VID_(\d{8})_(\d{6})\.mp\d",
    r"VID-(\d{8})-WA\d{4}\.mp\d",
    r'Screenshot_(\d{8})-(\d{6})\.png',
    r'(\d{8})_(\d{6})-\d{2}\.jpeg',
    r'IMG_(\d{8})_(\d{9})_HDR\.jpg',
    r'Snapchat-(\d{10})\.jpg',
    r'Snapchat-(\d{9})\.jpg',
    r'\d{5}IMG_\d{5}_BURST(\d{17})_COVER\.jpg',
    r'IMG_(\d{8})_(\d{9})_\d\.jpg',
    r'FJIMG_(\d{8})_(\d{6})-\d{2}\.jpeg',
    r'VID_(\d{8})_(\d{6})_LS\.jpg',
    r'(\d{4}-\d{2}-\d{2} \d{2}\.\d{2}\.\d{2})_\d\.jpg',
    r'IMG_(\d{8})_(\d{6})_HDR\.jpg',
    r'DSC_(\d{4})\.JPG\.jpg',
    r'Screenshot_(\d{8})-(\d{6})_Chrome\.jpg',
    r'Snapchat-(\d{10})\.mp\d',
    r'IMG_(\d{8})_(\d{6})~\d{2}\.jpg',
    r'(\d{8})_(\d{6})\(\d\)\.jpg',
    r'Snapchat-(\d{9})\.mp\d',
    r'New Doc (\d{4}-\d{2}-\d{2} \d{2}\.\d{2}\.\d{2})_\d\.jpg',
    r'CameraZOOM-(\d{17})\.jpg',
    r'Screenshot_(\d{8})-(\d{6})_Instagram.jpg',
    r'IMG(\d{4})A.jpg',
    r'^(\d{12}).jpg',
    r'Screenshot_(\d{8})-(\d{6}).jpg',
    r'\d{5}sPORTRAIT_\d{5}BURST(\d{17})COVER-\d{2}.jpeg',
    r'IMG(\d{8})(\d{9})\d.jpg',
    r'(\d{8})(\d{6})LLS.jpg',
    r'Screenshot(\d{8})-(\d{6})WhatsApp.jpg',
    r'(\d{8})(\d{6})HDR.jpg',
    r'(\d{13})-\d{2}.jpeg',
    r'^(\d{8})(\d{6})\d{3}.mp\d',
    r'WIN(\d{8})\d{2}\d{2}\d{2}Pro.jpg',
    r'PicsArt(\d{13}).jpg',
    r'Screenshot(\d{8})-(\d{6})FaceApp.jpg',
    r'^(\d{8})(\d{6}).JPG.jpg',
    r'\d{5}sPORTRAIT\d{5}BURST(\d{17})COVER~\d{2}.jpg',
    r'^(\d{8})(\d{6})\d{3}.jpg',
    r'VID-(\d{8})-WA\d{4}.\dgp',
    r'Screenshot_(\d{8})-(\d{6})YouTube.jpg',
    r'B\d{3}(\d{8})(\d{6})-\d{2}.jpeg',
    r'DSC(\d{4}).JPG',
    r'Snapchat-(\d{8}).jpg',
    r'^(\d{13}).mp4'
]

pattern_to_date_format = {
    8: '%Y%m%d',
    12: '%Y%m%d%H%M',
    14: '%Y%m%d%H%M%S',
    13: '%s',  # UNIX timestamp in milliseconds
    10: '%s'  # UNIX timestamp in seconds
}

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for root, _, files in os.walk(directory):

    sorted_files = sorted(files, key=sorting_key)
    for file in sorted_files:
        print(f'file\n\n')
        file_date = extract_date(file)
        notchanged.append(file)
        if file_date:
            print(f'{file_date.date()}')

            file_path = os.path.join(root, file)
            if process_file(file_path, file_date):
                update_exif_date(file_path, file_date)
                print(
                    f'Updated Date: {get_exif_date(file_path).date()}')
            output_file_path = move_file(file, root, directory)
            notchanged.remove(file)
print(notchanged)
