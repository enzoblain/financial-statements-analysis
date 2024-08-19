import os, re

from typing import List

def _get_file_name(report):
    html_file_name_tag = report.find("HtmlFileName")
    xml_file_name_tag = report.find("XmlFileName")

    if html_file_name_tag:
        return html_file_name_tag.text
    elif xml_file_name_tag:
        return xml_file_name_tag.text
    else:
        return ""

def _is_statement_file(short_name_tag, long_name_tag, file_name):
    return (
        short_name_tag is not None
        and long_name_tag is not None
        and file_name
        and "Statement" in long_name_tag.text
    )

def is_file_in_directory(file_name, directory_path):
    if not os.path.isdir(directory_path):
        raise ValueError(f"Provided directory path '{directory_path}' is not valid.")

    file_path = os.path.join(directory_path, file_name)
    return os.path.isfile(file_path)


def search_occurrences(pattern: str, items: List[str]) -> List[str]:
    if not isinstance(pattern, str) or not isinstance(items, list):
        raise TypeError("Pattern must be a string and items must be a list of strings.")
    
    if any(not isinstance(item, str) for item in items):
        raise TypeError("All items in the list must be strings.")
    
    matched_items = []
    
    try:
        for index, item in enumerate(items):
            if re.search(pattern, item):
                matched_items.append(item)
    except re.error as e:
        raise ValueError(f"Invalid regular expression pattern: {e}")

    return matched_items

