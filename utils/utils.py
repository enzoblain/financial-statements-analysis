import os, re

from typing import List

def _get_file_name(report):
    """
    Retrieves the file name from a report element.

    Parameters:
    - report (bs4.element.Tag): The report XML element.

    Returns:
    - str: The file name, or an empty string if not found.
    """
    html_file_name_tag = report.find("HtmlFileName")
    xml_file_name_tag = report.find("XmlFileName")

    if html_file_name_tag:
        return html_file_name_tag.text
    elif xml_file_name_tag:
        return xml_file_name_tag.text
    else:
        return ""

def _is_statement_file(short_name_tag, long_name_tag, file_name):
    """
    Checks if the file is a statement based on its tags and name.

    Parameters:
    - short_name_tag (bs4.element.Tag): The ShortName XML element.
    - long_name_tag (bs4.element.Tag): The LongName XML element.
    - file_name (str): The file name.

    Returns:
    - bool: True if the file is a statement, False otherwise.
    """
    return (
        short_name_tag is not None
        and long_name_tag is not None
        and file_name
        and "Statement" in long_name_tag.text
    )

def is_file_in_directory(file_name, directory_path):
    """
    Checks if a specific file exists within a given directory.

    Parameters:
        file_name (str): The name of the file to check.
        directory_path (str): The path to the directory where the file should be located.

    Returns:
        bool: True if the file exists in the directory, False otherwise.

    Raises:
        ValueError: If the directory path is not a valid directory.
    """
    if not os.path.isdir(directory_path):
        raise ValueError(f"Provided directory path '{directory_path}' is not valid.")

    file_path = os.path.join(directory_path, file_name)
    return os.path.isfile(file_path)


def search_occurrences(pattern: str, items: List[str]) -> List[str]:
    """
    Searches for occurrences of a given pattern in a list of strings and returns the strings where the pattern is found.

    Parameters:
        pattern (str): The regular expression pattern to search for.
        items (List[str]): The list of strings to search through.

    Returns:
        List[str]: A list of strings from the input list where the pattern was found.

    Raises:
        ValueError: If the pattern is not a valid regular expression.
    """
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

