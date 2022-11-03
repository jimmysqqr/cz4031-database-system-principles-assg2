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

        cte1 = """
            with cte1 as (
                select * from customer
            ), cte2 as (
            select * from orders, cte1 where o_orderkey < 1000
            )
            select * from cte1 C, cte2 O where C.c_custkey = O.o_custkey;
        """
        cte2 = """
            with cte1 as (
                select n_name, n_nationkey, n_regionkey
                from nation
            ), cte2 as (
                select o_custkey, o_orderkey from orders, cte1
                where o_orderdate >= '1994-01-01'
                and o_orderdate < '1995-01-01'
                and n_name = 'INDONESIA' or n_name = 'INDIA'
            )
            select
                n_name,
                sum(l_extendedprice * (1 - l_discount)) as revenue
                from
                customer,
                cte2,
                lineitem,
                supplier,
                cte1,
                region
                where
                c_custkey = o_custkey
                and l_orderkey = o_orderkey
                and l_suppkey = s_suppkey
                and c_nationkey = s_nationkey
                and s_nationkey = n_nationkey
                and n_regionkey = r_regionkey
                and r_name = 'ASIA'
                and c_acctbal > 10
                and s_acctbal > 20
                group by
                n_name
                order by
                revenue desc;
        """
        
        plan = obj.getQueryPlan(cte1)
        aqps = obj.getAltQueryPlans()
        obj.closeConnection()

        print(json.dumps(plan, indent=4))

        output = processPlan(plan, isStart=True)
        print(output)

if __name__ == '__main__':
    Application.main()
