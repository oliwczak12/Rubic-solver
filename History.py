class History:
    def __init__(self):
        self.undo_history = []
        self.redo_history = []

    def addToUndo(self, grid):
        self.undo_history.append(grid.__dict__.copy())
        if len(self.undo_history) >= 6:
            self.undo_history.pop(0)

    def addToRedo(self, grid):
        self.redo_history.append(grid.__dict__.copy())
        if len(self.redo_history) >= 6:
            self.redo_history.pop(0)

    def undo(self, grid):
        if self.undo_history:
            self.addToRedo(grid)
            return self.undo_history.pop()
        else:
            return None

    def redo(self, grid):
        if self.redo_history:
            self.addToUndo(grid)
            return self.redo_history.pop()
        else:
            return None