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