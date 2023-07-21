
import datetime
import re
import base64
import os
import sys

def generate_icons_folder_name(bookmark_export_name : str) -> str:

    # Turn a path from "/path/to/some/raleighs-file.txt" into "raleighs-file"
    bookmarks_file_basename = (os.path.splitext(bookmark_export_name)[0]).split("/")[-1]

    return (datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "__" +  bookmarks_file_basename)
    

def get_extension_from_base64(icon_base64 : str) -> str:
    
    mime_type_extension_regex = re.compile("data:image\/(.+);")

    return re.match(mime_type_extension_regex, icon_base64).group(1)


def extract_bookmark_icon(icons_folder_name : str, bookmark_name_or_url : str, icon_image_data : str) -> str:
    """
    Bookmark icons in Chrome, are stored like: data:image/png;base64,<BASE64-DATA>

    so extract the base64 data into the given file 
    """

    # Filenames can't be anything that isn't alphanumeric
    icon_filename = (re.sub(r"\W", "", bookmark_name_or_url)) + "." + get_extension_from_base64(icon_image_data)

    icon_base64_data_only = "".join(icon_image_data.split(",")[1::])

    if (len(icon_base64_data_only) < 10):
        print("[ERROR] Image icon data corrupted?")
        sys.exit(1)

    icon_full_path = os.path.join(icons_folder_name, icon_filename)

    with open(icon_full_path, 'wb') as icon_file_hndl:

        icon_file_hndl.write(base64.b64decode(icon_base64_data_only))
        #print(f"[DEBUG] Created {icon_filename}")

    return icon_full_path
    