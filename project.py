from preprocessing import DBConnection
from annotation import processPlan
from getpass import getpass
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

        # testQuery1 = "select distinct p_size from part order by p_size;"
        # testQuery2 = "select p_name, s_name from part, supplier, partsupp where ps_suppkey = s_suppkey and ps_partkey = p_partkey and ps_availqty >1000 and s_acctbal > 100000 and p_size = 10;"
        # testQuery3 = "select * from customer C, orders O where C.c_custkey = O.o_custkey;"
        
        # Read in a query from one of the sql files in /sample_queries
        fd = open("sample_queries/18.sql", "r")
        testQuery = fd.read()
        fd.close()
        
        plan = obj.getQueryPlan(testQuery)
        aqps = obj.getAltQueryPlans()
        obj.closeConnection()

        print(json.dumps(plan, indent=4))

        output = processPlan(plan, isStart=True)
        print(output)

if __name__ == '__main__':
    Application.main()
