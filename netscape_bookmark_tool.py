"""@package docstring

File: netscape_bookmark_tool.py
 
https://learn.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/platform-apis/aa753582(v=vs.85)

"""
import argparse
import os
import lxml.html
import re
import pdb
import sys
import base64
import datetime

def get_friendly_time_from_timestamp(timestamp : str) -> str:
    """
    """
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime("%Y%m%d%H%M")

def generate_icons_folder_name(bookmark_export_name : str) -> str:
    """
    
    """

    # Turn a path from "/path/to/some/raleighs-file.txt" into "raleighs-file"
    bookmarks_file_basename = (os.path.splitext(bookmark_export_name)[0]).split("/")[-1]

    return (datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "__" +  bookmarks_file_basename)
    

def get_extension_from_base64(icon_base64 : str) -> str:
    mime_type_extension_regex = re.compile("data:image\/(.+);")

    return re.match(mime_type_extension_regex, icon_base64).group(1)


def extract_bookmark_icon(icons_folder_name : str, bookmark_name_or_url : str, icon_image_data : str):
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

    with open(os.path.join(icons_folder_name, icon_filename), 'wb') as icon_file_hndl:

        icon_file_hndl.write(base64.b64decode(icon_base64_data_only))
        print(f"[DEBUG] Created {icon_filename}")
    

if __name__ == "__main__":
    argparse_parser = argparse.ArgumentParser()

    argparse_parser.add_argument("-f", "--input-bookmark-file", type=str, help="The full path to the Netscape format bookmark file", required=True)

    argparse_parser.add_argument("-s", "--sort-order", type=str, help="The order in which to sort the bookmarks, when re-exported. 'add' for Date-Added, 'mod' for Date-Modified, 'abc' for lexicographic order.")

    argparse_args = argparse_parser.parse_args()

    html_doc_root = lxml.html.parse(argparse_args.input_bookmark_file).getroot()

    icons_export_folder_name = generate_icons_folder_name(argparse_args.input_bookmark_file)
    os.makedirs(icons_export_folder_name)

    num_bookmarks_found = 0
    num_icons_exported = 0

    for bookmark_elem in html_doc_root.iter('a'):

        num_bookmarks_found += 1

        icon_image_data_key = "icon"

        if icon_image_data_key not in bookmark_elem.attrib:
            print("[WARNING] Bookmark found with no icon")
            continue

        icon_image_data = bookmark_elem.attrib[icon_image_data_key]

        bookmark_added_date = get_friendly_time_from_timestamp(bookmark_elem.attrib['add_date'])

        if bookmark_elem.text is not None:
            extract_bookmark_icon(icons_export_folder_name, (bookmark_added_date + "__" + bookmark_elem.text), icon_image_data)
        
        else:
            extract_bookmark_icon(icons_export_folder_name, (bookmark_added_date + "__" + bookmark_elem.attrib['href']), icon_image_data)

        num_icons_exported += 1

    print("===FINISHED===")
    print(f"Exported {num_bookmarks_found} bookmarks, with {num_icons_exported} icons")