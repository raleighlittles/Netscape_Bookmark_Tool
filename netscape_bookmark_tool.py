"""@package docstring

File: netscape_bookmark_tool.py
 
https://learn.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/platform-apis/aa753582(v=vs.85)

"""
import argparse
import os
import pdb
import lxml.html
import csv
import datetime
import requests

# locals
import icon_exporter
import link_exporter



def get_timestamp_from_epoch(epoch : str) -> str:
    """
    """
    return datetime.datetime.fromtimestamp(int(epoch)).strftime("%Y%m%d%H%M")

def parse_bookmarks_export(bookmark_export_filename : str):

    #all_bookmarks_links = list()

    all_bookmarks = list()

    html_doc_root = lxml.html.parse(bookmark_export_filename).getroot()

    icons_export_folder_name = icon_exporter.generate_icons_folder_name(argparse_args.input_bookmark_file)
    os.makedirs(icons_export_folder_name)

    num_bookmarks_found = 0
    num_icons_exported = 0

    for bookmark_elem in html_doc_root.iter('a'):

        bookmark_obj = dict.fromkeys(["bookmark_name", "bookmark_url", "bookmark_icon_filename", "bookmark_date_created_epoch", "bookmark_date_created_timestamp", "is_accessible"])

        num_bookmarks_found += 1

        # Initialize name
        bookmark_obj["bookmark_name"] = bookmark_elem.text

        # Initialize URL
        bookmark_link = bookmark_elem.attrib['href']
        bookmark_obj['bookmark_url'] = bookmark_link

        # Check if the URL is accessible by trying to access it
        is_url_accessible = True
        try:
            #print(f"[DEBUG] Checking validity of URL: {bookmark_link}")
            is_url_accessible = requests.get(bookmark_link, timeout=5, verify=False).ok

        except:
            is_url_accessible = False

        bookmark_obj["is_accessible"] = is_url_accessible

        bookmark_added_epoch = bookmark_elem.attrib["add_date"]
        bookmark_obj["bookmark_date_created_epoch"] = bookmark_added_epoch

        bookmark_added_date = get_timestamp_from_epoch(bookmark_added_epoch)
        bookmark_obj["bookmark_date_created_timestamp"] = datetime.datetime.fromtimestamp(int(bookmark_added_epoch)).strftime('%c')

        icon_image_data_key = "icon"

        if icon_image_data_key not in bookmark_elem.attrib:
            print("[WARNING] Bookmark found with no icon")
            continue

        icon_image_data = bookmark_elem.attrib[icon_image_data_key]

        icon_image_filename = ""

        if bookmark_elem.text is not None:
            icon_image_filename = icon_exporter.extract_bookmark_icon(icons_export_folder_name, (bookmark_added_date + "__" + bookmark_elem.text), icon_image_data)
        
        else:
            icon_image_filename = icon_exporter.extract_bookmark_icon(icons_export_folder_name, (bookmark_added_date + "__" + bookmark_link), icon_image_data)

        bookmark_obj["bookmark_icon_filename"] = icon_image_filename
        num_icons_exported += 1
        
        all_bookmarks.append(bookmark_obj)

    link_exporter.write_bookmark_links_to_file([bookmark["bookmark_url"] for bookmark in all_bookmarks], "bookmark_links.txt")

    with open("all_bookmarks.csv", 'w') as csv_file:

        csv_writer = csv.writer(csv_file)

        # Header columns
        csv_writer.writerow(all_bookmarks[0].keys())

        for bookmark in sorted(all_bookmarks, key=lambda k: k["bookmark_date_created_epoch"]):
            csv_writer.writerow(list(bookmark.values()))

    

    print("==========FINISHED==========")
    print(f"Exported {num_bookmarks_found} bookmarks, with {num_icons_exported} icons")

if __name__ == "__main__":
    argparse_parser = argparse.ArgumentParser()

    argparse_parser.add_argument("-f", "--input-bookmark-file", type=str, help="The full path to the Netscape format bookmark file", required=True)

    argparse_args = argparse_parser.parse_args()

    parse_bookmarks_export(argparse_args.input_bookmark_file)

