from treelib import Node, Tree
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QSize
from PyQt6 import QtWidgets

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setFixedSize(640, 480)
        self.initUI()

    def tree_display(self):
        tree = Tree()
        tree.create_node("Harry", "harry")  # No parent means its the root node
        tree.create_node("Jane",  "jane"   , parent="harry")
        tree.create_node("Bill",  "bill"   , parent="harry")
        tree.create_node("Diane", "diane"  , parent="jane")
        tree.create_node("Mary",  "mary"   , parent="diane")
        tree.create_node("Mark",  "mark"   , parent="jane")
        tree.create_node("Dog",  "dog"   , parent="mary")
        tree.save2file("test.txt",line_type="ascii-em")
        text=open('test.txt').read()
        self.el1.setText(text)

    def get_input(self):
        self.el2.setText(self.line.text())

    def initUI(self):
        self.setWindowTitle("My App")
        layout = QtWidgets.QVBoxLayout()


        # Create a form layout for the label and line edit
        topLayout = QtWidgets.QFormLayout()
        # Add a label and a line edit to the form layout
        self.line = QtWidgets.QLineEdit(self)
        self.nameLabel = QtWidgets.QLabel(self)
        self.nameLabel.setText('Name:')
        topLayout.addRow(self.nameLabel, self.line)
        layout.addLayout(topLayout)

        topBtn = QtWidgets.QPushButton('Top')
        layout.addWidget(topBtn)
        topBtn.clicked.connect(self.tree_display)

        botBtn = QtWidgets.QPushButton('Bottom')
        layout.addWidget(botBtn)
        botBtn.clicked.connect(self.get_input)


        self.el1 = QtWidgets.QTextEdit(self)
        self.el1.setReadOnly(True)
        layout.addWidget(self.el1)

        self.el2 = QtWidgets.QTextEdit(self)
        layout.addWidget(self.el2)
        
        
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        # Set the central widget of the Window.
        self.setCentralWidget(widget)

    


app = QApplication([])
app.setStyle('Fusion')
window = MainWindow()
window.show()

app.exec()