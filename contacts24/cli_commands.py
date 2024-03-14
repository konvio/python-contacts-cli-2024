class Command():
    """Command"""
    def __init__(self, name: str, func, description="", format = "", is_hidden = False):
        """_summary_

        Args:
            name (str): _description_
            func (function|lambda): command function
            description (str, optional): text description of the command. Defaults to "".
            format (str, optional): how to call command. Defaults to "".
            is_hidden (bool, optional): Is command hidden from the help output. Defaults to False.
        """
        self.name = name
        self.func = func
        self.description = description
        self.format = format
        self.is_hidden = is_hidden
        
    def __call__(self):
        return self.func
