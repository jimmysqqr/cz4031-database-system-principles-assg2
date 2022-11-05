from preprocessing import DBConnection
from annotation import processPlan
from getpass import getpass
from collections import deque
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
                           dbname="TPC-H", user="terry", password=password)

        testQuery1 = "select * from customer limit 5;"
        testQuery2 = "select p_name, s_name from part, supplier, partsupp where ps_suppkey = s_suppkey and ps_partkey = p_partkey and ps_availqty >1000 and s_acctbal > 100000 and p_size = 10;"
        plan = obj.getQueryPlan(testQuery1)
        print(plan)
        print(type(plan))
        # dbname="TPC-H", user="terry", password=password)

        # testQuery1 = "select distinct p_size from part order by p_size;"
        # testQuery2 = "select p_name, s_name from part, supplier, partsupp where ps_suppkey = s_suppkey and ps_partkey = p_partkey and ps_availqty >1000 and s_acctbal > 100000 and p_size = 10;"
        # testQuery3 = "select * from customer C, orders O where C.c_custkey = O.o_custkey;"
        
        # Read in a query from one of the sql files in /sample_queries
        fd = open("sample_queries/2.sql", "r")
        testQuery = fd.read()
        fd.close()

        group1 = """
            SELECT p_brand FROM part group by p_brand
        """
        group2 = """
            select p_brand from part where p_size < 2
            intersect
            select p_brand from part where p_size > 20;
        """
        
        plan = obj.getQueryPlan(group2)
        aqps = obj.getAltQueryPlans()
        obj.closeConnection()

        print(json.dumps(plan, indent=4))

        output = processPlan(plan, isStart=True)
        print(output)

if __name__ == '__main__':
    Application.main()