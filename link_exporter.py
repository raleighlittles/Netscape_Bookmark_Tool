import os
import typing

def write_bookmark_links_to_file(bookmark_links : typing.List, output_file_name : str):
    
    with open(output_file_name, 'w') as output_file:
        for link in sorted(bookmark_links):
            # You'd think writelines would use newlines, but it doesn't...
            output_file.write(link + "\n")