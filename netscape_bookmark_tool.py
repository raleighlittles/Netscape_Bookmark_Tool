"""@package docstring

File: netscape_bookmark_tool.py
 
https://learn.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/platform-apis/aa753582(v=vs.85)

"""
import argparse
import os
import lxml.html
import datetime

# locals
import icon_exporter
import link_exporter

def get_friendly_time_from_timestamp(timestamp : str) -> str:
    """
    """
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime("%Y%m%d%H%M")

def parse_bookmarks_export(bookmark_export_filename : str):

    all_bookmarks_links = list()

    html_doc_root = lxml.html.parse(bookmark_export_filename).getroot()

    icons_export_folder_name = icon_exporter.generate_icons_folder_name(argparse_args.input_bookmark_file)
    os.makedirs(icons_export_folder_name)

    num_bookmarks_found = 0
    num_icons_exported = 0

    for bookmark_elem in html_doc_root.iter('a'):

        num_bookmarks_found += 1

        bookmark_link = bookmark_elem.attrib['href']

        all_bookmarks_links.append(bookmark_link)

        icon_image_data_key = "icon"

        if icon_image_data_key not in bookmark_elem.attrib:
            print("[WARNING] Bookmark found with no icon")
            continue

        icon_image_data = bookmark_elem.attrib[icon_image_data_key]

        bookmark_added_date = get_friendly_time_from_timestamp(bookmark_elem.attrib['add_date'])

        if bookmark_elem.text is not None:
            icon_exporter.extract_bookmark_icon(icons_export_folder_name, (bookmark_added_date + "__" + bookmark_elem.text), icon_image_data)
        
        else:
            icon_exporter.extract_bookmark_icon(icons_export_folder_name, (bookmark_added_date + "__" + bookmark_link), icon_image_data)

        num_icons_exported += 1

    link_exporter.write_bookmark_links_to_file(all_bookmarks_links, "bookmark-links.txt")

    print("==========FINISHED==========")
    print(f"Exported {num_bookmarks_found} bookmarks, with {num_icons_exported} icons")

if __name__ == "__main__":
    argparse_parser = argparse.ArgumentParser()

    argparse_parser.add_argument("-f", "--input-bookmark-file", type=str, help="The full path to the Netscape format bookmark file", required=True)

    argparse_args = argparse_parser.parse_args()

    parse_bookmarks_export(argparse_args.input_bookmark_file)

