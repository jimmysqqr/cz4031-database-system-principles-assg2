import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QScrollArea
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap
from PyQt6 import QtWidgets, QtCore
from annotation import processCosts, processPlan
import graphviz

class MainWindow(QMainWindow):
    def __init__(self,obj):
        super(MainWindow, self).__init__()
        self.dbObj = obj
        self.setFixedSize(1200, 700)
        self.initUI()


    """
    Function to separate the # from the query names E.g.(Sequentialscan#1)
    """
    def substring_before(self,s, delim):
        return s.partition(delim)[0]


    """
    Function to display the traversal tree
    """
    def treeDisplay(self):
        f = graphviz.Digraph(filename = "hello.gv")

        query = self.textEdit.toPlainText()
        plan = self.dbObj.getQueryPlan(query)
        adjList = self.dbObj.getAdjList(plan, {})[0]

        # orderList = self.dbObj.getPostOrder(plan, {})
        # print(orderList)

        self.dbObj.nodeCount = 1

        for node in self.dbObj.nodeList:
            f.node(node,self.substring_before(node,"#"))

        for annotate in adjList:
            if len(adjList[annotate]) != 0 :
                for annotateString in adjList[annotate]:
                    f.edge(annotate,annotateString)


        # names = ["A","B","C","D","E","F","G","H"]
        # positions = ["CEO","Team A Lead","Team B Lead", "Staff A","Staff B", "Staff C", "Staff D", "Staff E"]
        # for name, position in zip(names, positions):
        #     f.node(name, position)
        
        # #Specify edges
        # f.edge("A","B"); f.edge("A","C") #CEO to Team Leads
        # f.edge("B","D"); f.edge("B","E") #Team A relationship
        # f.edge("C","F"); f.edge("C","G"); f.edge("C","H") #Team B relationship
        
        f.render("temp_img",format="png", view=False)

        self.im = QPixmap("./temp_img.png")
        self.imgLabel.setPixmap(self.im)
        self.imgLabel.setFixedHeight(self.im.size().height())
        self.imgLabel.setFixedWidth(self.im.size().width())


    """
    Function to call annotate query function
    """
    def annotateQuery(self):
        #to get the text use
        query = self.textEdit.toPlainText()
        plan = self.dbObj.getQueryPlan(query)
        output = []
        processPlan(plan, output)

        new_output = processCosts(output, self.dbObj)

        data=[]
        for i,x  in enumerate(new_output):
            data.append(str(i+1)+ '.     ' + x)
            self.el1.setText("\n".join(data))
        

    def initUI(self):
        self.setWindowTitle("My App")
        layout = QtWidgets.QVBoxLayout()


        # Create a form layout for the label and line edit
        topLayout = QtWidgets.QFormLayout()
        # Add a label and a line edit to the form layout
        self.textEdit = QtWidgets.QTextEdit(self)
        self.queryLabel = QtWidgets.QLabel(self)
        self.queryLabel.setText('Enter query here:')
        layout.addWidget(self.queryLabel)
        layout.addWidget(self.textEdit)


        # Annotate Query button
        topBtn = QtWidgets.QPushButton('Annotate Query')
        layout.addWidget(topBtn)
        topBtn.clicked.connect(self.annotateQuery)


        # Annotate Query text display
        self.el1 = QtWidgets.QTextEdit(self)
        self.el1.setReadOnly(True)
        layout.addWidget(self.el1)

        # Visualize Query Plan button
        botBtn = QtWidgets.QPushButton('Visualize Query Plan')
        layout.addWidget(botBtn)
        botBtn.clicked.connect(self.treeDisplay)

        # Image Label for displaying tree
        self.imgLabel = QtWidgets.QLabel(self)
        self.im = QPixmap("./Empty.png",)
        # self.imgLabel.setScaledContents(True)
        self.imgLabel.setPixmap(self.im)

        # Scroll area to have the image label contained inside
        self.imgScrollArea = QScrollArea()
        self.imgScrollArea.setWidget(self.imgLabel)
        self.imgScrollArea.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imgScrollArea.setFixedWidth(1190)

        # Grid layout for the Image label
        self.grid = QtWidgets.QGridLayout()
        self.grid.addWidget(self.imgScrollArea,10,10,alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(self.grid)
        
        
        # Sets final layout to widget
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(widget)

    


# app = QApplication([])
# app.setStyle('Fusion')
# window = MainWindow()
# window.show()

# app.exec()