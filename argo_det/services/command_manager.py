
class CommandManager:
    """Manages a stack of commands for undo/redo functionality."""
    def __init__(self):
        self.undo_stack = []  # Stack for undo operations
        self.redo_stack = []  # Stack for redo operations

    def execute_command(self, command):
        """Execute a command and add it to the undo stack."""
        command.execute()
        self.undo_stack.append(command)
        self.redo_stack.clear()  # Clear the redo stack whenever a new command is executed

    def undo(self):
        """Undo the last command."""
        if self.undo_stack:
            command = self.undo_stack.pop()
            command.undo()
            self.redo_stack.append(command)

    def redo(self):
        """Redo the last undone command."""
        if self.redo_stack:
            command = self.redo_stack.pop()
            command.execute()
            self.undo_stack.append(command)

class CentralCommandManager:
    """Manages a single stack of commands for undo/redo, tracking which plot was affected."""
    def __init__(self):
        self.undo_stack = []  # Stack for undo operations
        self.redo_stack = []  # Stack for redo operations

    def execute_command(self, command):
        """Execute a command and add it to the undo stack."""
        command.execute()
        self.undo_stack.append(command)
        self.redo_stack.clear()  # Clear redo stack whenever a new command is executed

    def undo(self):
        """Undo the last command."""
        if self.undo_stack:
            command = self.undo_stack.pop()
            command.undo()
            self.redo_stack.append(command)

    def redo(self):
        """Redo the last undone command."""
        if self.redo_stack:
            command = self.redo_stack.pop()
            command.execute()
            self.undo_stack.append(command)

