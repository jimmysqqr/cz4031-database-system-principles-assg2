from PyQt6.QtWidgets import QApplication, QMainWindow, QScrollArea
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap
from PyQt6 import QtWidgets, QtCore
from preprocessing import DBConnection
from annotation import processCosts, processPlan
import graphviz


class MainWindow(QMainWindow):
    def __init__(self, password):
        super(MainWindow, self).__init__()
        """
            The constructor creates a new connection to the database every time for security.
        """
        self.dbObj = obj = DBConnection(host="localhost", port="5432",
                                        dbname="TPC-H", user="postgres", password=password)
        self.setFixedSize(1200, 700)
        self.initUI()

    def treeDisplay(self):
        """
            Function to display the traversal tree
        """
        f = graphviz.Graph()

        query = self.textEdit.toPlainText()
        plan = self.dbObj.getQueryPlan(query)
        adjList = self.dbObj.getAdjList(plan, {})[0]
        nodeList = self.dbObj.nodeList

        self.dbObj.nodeCount = 1
        self.dbObj.nodeList = list()

        for node in nodeList:
            name = node.split('#')[0]
            f.node(node, name)

        for annotate in adjList:
            if len(adjList[annotate]) != 0:
                for annotateString in adjList[annotate]:
                    f.edge(annotate, annotateString)

        f.render("QueryPlan", format="png", view=False)

        self.im = QPixmap("./QueryPlan.png")
        self.imgLabel.setPixmap(self.im)
        self.imgLabel.setFixedHeight(self.im.size().height())
        self.imgLabel.setFixedWidth(self.im.size().width())

    def annotateQuery(self):
        """
            Function to call annotate query function
        """
        query = self.textEdit.toPlainText()
        plan = self.dbObj.getQueryPlan(query)
        self.dbObj.getAltQueryPlans()
        # Remember to retrieve the alternate query plans!

        output = []
        processPlan(plan, output)
        new_output = processCosts(output, self.dbObj)

        data = []
        for i, x in enumerate(new_output):
            data.append(str(i+1) + '.     ' + x)
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
        self.grid.addWidget(self.imgScrollArea, 10, 10,
                            alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(self.grid)

        # Sets final layout to widget
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(widget)
