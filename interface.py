from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap
from PyQt6 import QtWidgets, QtCore
import graphviz

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setFixedSize(640, 480)
        self.initUI()

    def tree_display(self):
        f = graphviz.Digraph(filename = "hello.gv")
        names = ["A","B","C","D","E","F","G","H"]
        positions = ["CEO","Team A Lead","Team B Lead", "Staff A","Staff B", "Staff C", "Staff D", "Staff E"]
        for name, position in zip(names, positions):
            f.node(name, position)
        
        #Specify edges
        f.edge("A","B"); f.edge("A","C") #CEO to Team Leads
        f.edge("B","D"); f.edge("B","E") #Team A relationship
        f.edge("C","F"); f.edge("C","G"); f.edge("C","H") #Team B relationship
        
        f.render("temp_img",format="png", view=False)

        text=open('test.txt', encoding="utf8").read()
        self.el1.setText(text)

        self.im = QPixmap("./temp_img.png")
        self.imgLabel.setPixmap(self.im)

    def get_input(self):
        self.el2.setText(self.line.text())

    def initUI(self):
        self.setWindowTitle("My App")
        layout = QtWidgets.QVBoxLayout()



        # Create a form layout for the label and line edit
        topLayout = QtWidgets.QFormLayout()
        # Add a label and a line edit to the form layout
        self.line = QtWidgets.QLineEdit(self)
        self.queryLabel = QtWidgets.QLabel(self)
        self.queryLabel.setText('Query:')
        topLayout.addRow(self.queryLabel, self.line)
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

        self.imgLabel = QtWidgets.QLabel(self)
        self.im = QPixmap("./Empty.png")
        self.imgLabel.setScaledContents(True)
        self.imgLabel.setPixmap(self.im)


        self.grid = QtWidgets.QGridLayout()
        self.grid.addWidget(self.imgLabel,10,10)
        layout.addLayout(self.grid)
        
        
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        # Set the central widget of the Window.
        self.setCentralWidget(widget)

    


app = QApplication([])
app.setStyle('Fusion')
window = MainWindow()
window.show()

app.exec()