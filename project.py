import os
from getpass import getpass
from interface import MainWindow
from PyQt6.QtWidgets import QApplication


class Application():
    def __init__(self):
        pass

    def main():
        """
        Default values for DBConnection:

        host = "localhost"      {PostgreSQL choses this by default}
        port = "5342"           {Default port chosen by PostgreSQL}
        dbname = "TPC-H"        {This depends on your database schema intialization}
        username = "postgres"   {Default username set by PostgreSQL}
        password = ""           {Please enter the password for your PostgreSQL server}

        Do change the parameters to your liking.
        """
        # User inputs the password and we can connect to PostgreSQL
        password = getpass("Please input your PostgreSQL password: ")

        # Remember to change this path appropriately. I had to add this otherwise Graphviz doesn't work for me
        os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'

        app = QApplication([])
        app.setStyle('Fusion')
        window = MainWindow(password)
        window.show()
        app.exec()


if __name__ == '__main__':
    Application.main()
