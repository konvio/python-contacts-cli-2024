import os

def get_file_path(filename = "") -> str:
    """Get user home dir

    Args:
        filename (str): file name to get home path

    Returns:
        str: Path to user dir, else, current working dir
    """
    try:
        folder = os.path.expanduser('~')
    except Exception as e:
        folder = os.getcwd()
    
    if filename and filename != '':
        folder = folder + "\\" + filename

    return folder