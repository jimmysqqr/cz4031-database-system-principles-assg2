from preprocessing import DBConnection
from annotation import processPlan
from getpass import getpass
from collections import deque

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

        testQuery1 = "select * from customer limit 5;"
        testQuery2 = "select p_name, s_name from part, supplier, partsupp where ps_suppkey = s_suppkey and ps_partkey = p_partkey and ps_availqty >1000 and s_acctbal > 100000 and p_size = 10;"
        testQuery3 = "select * from customer C, orders O where C.c_custkey = O.o_custkey;"
        plan = obj.getQueryPlan(testQuery2)
        # print(plan)
        

        # Initialise a queue to store the pre-order traversal of the query plan operator tree
        q = deque()

        print(plan)
        output = processPlan(plan, q, isStart=True)
        print(output)
        for item in q:
            print(item)

        obj.getAltQueryPlans()
        
        obj.closeConnection()

if __name__ == '__main__':
    Application.main()
