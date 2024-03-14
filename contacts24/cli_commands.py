from typing import Dict 


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


def get_help(commands: Dict[str, Command]) -> str:
    """Generate help based on the available list of commands

    Returns:
        str: Help table
    """
    message = "\n"
    
    padding_command = len("Command")
    padding_description = len("Description")
    padding_format = len("Format")
    
    for name, command in commands.items():
        if command.is_hidden:
            continue
        padding_command = max([padding_command, len(name)])
        padding_description = max([padding_description, len(command.description)])
        padding_format = max([padding_format, len(command.format)])
    
    border = (("| {0:-^%s} " % padding_command) + ("| {0:-^%s} |" % padding_description) + (" {0:-^%s} |\n" % padding_format)).format("-")
    
    message += border
    message += (("| {0:^%s} " % padding_command) + ("| {1:^%s} |" % padding_description) + (" {2:^%s} |\n" % padding_format)).format("Command", "Description", "Format")
    message += border
    
    for name, command in commands.items():
        if command.is_hidden:
            continue
        message += (("| {0:<%s} " % padding_command) + ("| {1:<%s} |" % padding_description) + (" {2:<%s} |\n" % padding_format)).format(command.name, command.description, command.format)
    message += border
    
    return message
