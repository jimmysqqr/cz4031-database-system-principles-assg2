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
                           dbname="TPC-H", user="postgres", password=password)

        # fd = open('./sql/2.sql', 'r')
        # testQuery = fd.read()
        # fd.close()

        testQuery1 = "select * from customer limit 5;"
        testQuery2 = "select p_name, s_name from part, supplier, partsupp where ps_suppkey = s_suppkey and ps_partkey = p_partkey and ps_availqty >1000 and s_acctbal > 100000 and p_size = 10;"
        testQuery3 = "select p_name, s_name from part, supplier, partsupp where ps_suppkey = s_suppkey and ps_partkey = p_partkey and ps_availqty >1000 and s_acctbal > 100000 and p_size = 10 group by p_name, s_name;"
        testQuery4 = """
                    select
                        l_returnflag,
                        l_linestatus,
                        sum(l_quantity) as sum_qty,
                        sum(l_extendedprice) as sum_base_price,
                        sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
                        sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
                        avg(l_quantity) as avg_qty,
                        avg(l_extendedprice) as avg_price,
                        avg(l_discount) as avg_disc,
                        count(*) as count_order
                    from
                        lineitem
                    where
                        l_shipdate <= date '1998-12-01' - interval ':1' day (3)
                    group by
                        l_returnflag,
                        l_linestatus
                    order by
                        l_returnflag,
                        l_linestatus;
        """
        plainAgg1 = "select count(p_size) from part"
        plainAgg2 = "select max(p_size) from part"

        hashedAgg1 = "select p_name, max(p_size) from part group by p_name;"
        hashedAgg2 = "select p_name, p_type, max(p_size) from part group by p_name, p_type;"

        sortedAgg1 = "select count(*) from part group by p_partkey;"
        sortedAgg2 = "select count(*) from part group by p_partkey having count(*)=1;"
#         sortedAgg3 = "select count(*) from partsupp group by ps_partkey;"
#         sortedAgg4 = """
#         select avg(p_size) 
# from (select * from part order by p_size) AS foo
# where p_size > 1
#         """


        plan = obj.getQueryPlan(sortedAgg2)
        # plan2 = obj.getQueryPlan(testQuery2)
        obj.closeConnection()

        # Initialise a queue
        q = deque()

        # parsed = json.loads(plan)
        print(json.dumps(plan, indent=4))
        # print(json.dumps(plan2, indent=4))

        # print(plan)

        output = processPlan(plan, isStart=True)
        print(output)
        for item in q:
            print(item)


if __name__ == '__main__':
    Application.main()
