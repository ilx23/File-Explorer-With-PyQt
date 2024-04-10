import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QWidget, QFileSystemModel, \
    QAction, QMenu, QInputDialog, QLineEdit
from PyQt5.QtCore import Qt, QDir, QModelIndex, QFile


class FileExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("File Explorer")
        self.setGeometry(100, 100, 800, 600)

        # File tree view
        self.tree_view = QTreeView()
        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(""))

        self.create_actions()
        self.create_menus()

        layout = QVBoxLayout()
        layout.addWidget(self.tree_view)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def create_actions(self):
        self.copy_action = QAction("Copy", self)
        self.copy_action.setShortcut(Qt.CTRL + Qt.Key_C)
        self.copy_action.triggered.connect(self.copy)

        self.cut_action = QAction("Cut", self)
        self.cut_action.setShortcut(Qt.CTRL + Qt.Key_X)
        self.cut_action.triggered.connect(self.cut)

        self.paste_action = QAction("Paste", self)
        self.paste_action.setShortcut(Qt.CTRL + Qt.Key_V)
        self.paste_action.triggered.connect(self.paste)

        self.delete_action = QAction("Delete", self)
        self.delete_action.setShortcut(Qt.Key_Delete)
        self.delete_action.triggered.connect(self.delete)

        self.create_file_action = QAction("Create File", self)
        self.create_file_action.setShortcut(Qt.CTRL + Qt.Key_N)
        self.create_file_action.triggered.connect(self.create_file)

    def create_menus(self):
        self.tree_view.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.tree_view.addAction(self.copy_action)
        self.tree_view.addAction(self.cut_action)
        self.tree_view.addAction(self.paste_action)
        self.tree_view.addAction(self.delete_action)
        self.tree_view.addAction(self.create_file_action)

    def copy(self):
        self.copied_action = self.tree_view.currentIndex()
        self.copied_path = self.model.filePath(self.copied_action)

    def cut(self):
        self.copy()
        self.cut_mode = True

    def paste(self):
        if hasattr(self, "copied_path"):
            destination_index = self.tree_view.currentIndex()
            destination_path = self.model.filePath(destination_index)

            # Check if destination is a directory; if not, get the parent directory
            if not QDir(destination_path).exists():
                destination_path = QDir().filePath(destination_path)

            file_name = QDir(self.copied_path).dirName()
            new_path = QDir(destination_path).filePath(file_name)

            if hasattr(self, "cut_mode") and self.cut_mode:
                # For cut, move the file or directory
                if QDir().rename(self.copied_path, new_path):
                    del self.copied_path
                    del self.cut_mode
                    self.model.refresh(destination_index)
            else:
                # For copy, we need to differentiate between files and directories
                if QDir(self.copied_path).exists():  # Check if it's a directory
                    # Logic for copying directory not implemented in this snippet
                    pass
                else:
                    # Assuming it's a file if it's not a directory
                    QFile.copy(self.copied_path, new_path)
                    del self.copied_path
                    self.model.refresh(destination_index)

    def delete(self):
        index = self.tree_view.currentIndex()
        path = self.model.filePath(index)
        QDir().remove(path)

    def create_file(self):
        index = self.tree_view.currentIndex()
        path = self.model.filePath(index)
        new_file_name, ok = QInputDialog.getText(self, "Create File", "Enter File Name")
        if ok:
            new_file_path = QDir(path).filePath(new_file_name)
            with open(new_file_path, "w") as new_file:
                new_file.write("")

def main():
    app = QApplication(sys.argv)
    file_explorer = FileExplorer()
    file_explorer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()