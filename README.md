Image File Sorter
=================

This script is designed to sort image files in a given directory based on their date information. The script extracts the date information from the filename using regular expressions and updates the date information in the image file's EXIF data.

Usage
-----

1.  Change the `directory` and `output_dir` variables to specify the input and output directories, respectively.
2.  Run the script.
3.  The script will move the image files to the output directory, maintaining the folder structure, and update the date information in the image file's EXIF data.

Requirements
------------

This script requires the following libraries:

-   `os`
-   `re`
-   `datetime`
-   `PIL`
-   `piexif`

Make sure these libraries are installed before running the script.

Regular Expressions
-------------------

The script uses a list of regular expressions to extract the date information from the filename. The regular expressions are stored in the `regex_patterns` list. You can modify this list to add or remove regular expressions.

Limitations
-----------

This script has only been tested with the provided regular expressions and may not work with all types of image files. Additionally, the script currently only supports JPEG and MP4 files.
