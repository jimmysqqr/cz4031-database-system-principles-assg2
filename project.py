from interface import MainWindow
from PyQt6.QtWidgets import QApplication
from preprocessing import DBConnection
from annotation import processPlan
from annotation import processCosts
from getpass import getpass
import os
import json


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

        obj = DBConnection(host="localhost", port="5432",
                           dbname="TPC-H", user="postgres", password=password)

        # Remember to change this path appropriately. I had to add this otherwise Graphviz doesn't work for me
        os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'

        app = QApplication([])
        app.setStyle('Fusion')
        window = MainWindow()
        window.show()
        app.exec()

        # Read in a query from one of the sql files in /sample_queries
        fd = open("sample_queries/1.sql", "r")
        testQuery = fd.read()
        fd.close()

        group1 = """
            SELECT p_brand FROM part group by p_brand
        """
        
        hash1 = "select * from customer C, orders O where C.c_custkey = O.o_custkey;"

        cte1 = """
            with cte1 as (
                select * from customer
            ), cte2 as (
            select * from orders, cte1 where o_orderkey < 1000
            )
            select * from cte1 C, cte2 O where C.c_custkey = O.o_custkey;
        """

        append4 = """
            select p_brand from part where p_size < 2
            except
            select p_brand from part where p_size > 20;
        """
    
        plan = obj.getQueryPlan(testQuery)
        obj.getAltQueryPlans()

        # print(json.dumps(plan, indent=4))
        adjList = obj.getAdjList(plan, {})[0]
        obj.nodeCount = 1
        print(json.dumps(adjList, indent=4))
        # print(obj.postOrder)

        # These attributes for the diff in cost of the whole query plans
        # print("Cost of QEP: {}".format(obj.estimatedCost))
        # for k,v in obj.queryCostDict.items():
        #     print("AQP with {} enabled: ".format(k))
        #     print("Total cost of AQP: {}".format(v))
        #print(f"Increase in Estimated Cost = {round(cost-self.estimatedCost, 2)}")
        #print(f"Relative increase in estimated cost = {round((cost-self.estimatedCost)/self.estimatedCost, 2)}")

        # These attributes for the diff in cost of each join sub tree (idea is their relative difference approximates the increase/decrease in cost!)
        # print("Cost of subtrees in QEP: ")
        # print(obj.prefixSumJoin)

        # for k, v in obj.joinTreeCostDict.items():
        #     print("AQP with {} enabled: ".format(k))
        #     print("Relative increase in cost of subtrees: {}".format(v))
        # print(obj.joinTreeCostDict.keys())
        # print("Cost of join subtrees in QEP: {}".format(self.prefixSumJoin))
        # print("Relative increase in cost of join subtrees in AQP: {}".format(diff))

        obj.closeConnection()

        # print(json.dumps(plan, indent=4))

        # Initialize the output as a list, which will get filled with annotations. The list items are displayed on GUI in point form
        output = []
        processPlan(plan, output)

        new_output = processCosts(output, obj)
        print(new_output)
        
if __name__ == '__main__':
    Application.main()
