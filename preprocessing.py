import psycopg2


class DBConnection:
    def __init__(self, host="localhost", port='5432', dbname="TPC-H", user="postgres", password=""):
        # Initialize the class variables

        # For the database connection
        self.cursor = None
        self.connection = None

        # For the input query and query plan information
        self.query = ""
        self.queryPlan = dict()

        # For holding statistics about the query plan
        self.postOrder = list()
        self.hasJoin = False
        self.estimatedCost = 0

        # For evaluating the representative alternative query plans
        self.prefixSumJoin = list()
        self.altQueryPlans = list()

        try:
            # Connecting to the database and initializing the cursor as class variables
            self.connection = psycopg2.connect(
                host=host, port=port, dbname=dbname, user=user, password=password)
            self.cursor = self.connection.cursor()
            print("Connected to PostgreSQL successfully!")

        except (Exception, psycopg2.Error) as error:
            # Error handling
            print("Error while connecting to PostgreSQL: ", error)
            exit()

    def closeConnection(self):
        """
        Method that closes the connection to PostgreSQL.
        """
        if self.connection is not None:
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection has been closed.")

    def getQueryPlan(self, query):
        """
        This function would receive the SQL query string and returns a JSON object (converted to dict) of the QEP returned by PostgreSQL.

        It works by leveraging the EXPLAIN keyword along with the following optional arguments,

        EXPLAIN ( option /[ option1, option2, ... ] ) statement

        where option can be one of the following:

            ANALYZE     : Ensures that the query is actually executed, allowing us to retrieve run time statistics {'Planning Time', 'Triggers', 'Execution Time'}. Defaults to FALSE.
            VERBOSE     : Display additional information regarding the plan. Defaults to FALSE.
            COSTS       : Include information on the estimated startup and total cost of each plan node, along with estimated output cardinality. This parameter defaults to TRUE.
            SETTINGS    : Include information on configuration parameters. Defaults to FALSE.
            BUFFERS     : Include information on buffer usage. Defaults to FALSE.
            WAL         : Include information on Write Ahead Logging record generation. May only be used when ANALYZE is also enabled. Defaults to FALSE.
            TIMING      : Include actual startup time and time spent in each node in the output.  May only be used when ANALYZE is also enabled. Defaults to TRUE.
            SUMMARY     : Include summary information (e.g., totaled timing information) after the query plan. Included by default when ANALYZE is used but otherwise isn't.
            FORMAT      : Specify the output format { TEXT | XML | JSON | YAML }. Defaults to TEXT.

        Have used FORMAT JSON for now, maybe can add ANALYZE and VERBOSE?
        """
        self.query = query
        self.cursor.execute(
            f"EXPLAIN (FORMAT JSON) {self.query}")

        # Need to peel away the wrappers from the raw output
        rawOutput = self.cursor.fetchall()
        plan = rawOutput[0][0][0]['Plan']
        self.queryPlan = plan

        return self.queryPlan

    def getPostOrder(self, queryPlan, result):
        """
        This method performs a post order breadth traversal (DFS) on the query plan (a nested dictionary) and returns a list of the operators in the same order.
        It also sets the 'hasJoin' class variable.
        """
        if 'Plans' in queryPlan:
            for subPlan in queryPlan['Plans']:
                self.getPostOrder(subPlan, result)
        # DFS

        if (not self.hasJoin and queryPlan['Node Type'] in ['Nested Loop', 'Hash Join', 'Merge Join']):
            self.hasJoin = True
        # Set the hasJoin attribute if the query plan has a join operator

        temp = [queryPlan['Node Type'], queryPlan['Total Cost']]
        result.append(temp)
        # Format the dict

        return result

    def getOperatorSet(self, postOrder):
        """
        This method creates a set of all the various opertors used in the query plan by scanning it's post order traversal.
        """
        result = set()

        for op in postOrder:
            result.add(op[0])

        return result

    def getTotalCost(self, postOrder):
        """
        This method evaluates the total estimated cost of the query plan scanning it's post order traversal.
        """
        result = 0

        for op in postOrder:
            result += op[1]

        return result

    def generatePrefixSumJoin(self):
        """
        This method returns a list of the cost of the subtrees rooted by a join operator in the query plan operator tree.
        It also checks if a 'Gather' operator is used after the join.

        NOTE: We only call this method for the optimal QEP. It will be used later for evaluating the AQPs.
        """

        currSum = 0
        result = list()
        joins = set(['Nested Loop', 'Hash Join', 'Merge Join'])

        for i in range(len(self.postOrder)):
            op = self.postOrder[i]
            currSum += op[1]

            if (op[0] in joins):
                if (i < len(self.postOrder)-1 and self.postOrder[i+1][0] == 'Gather'):
                    currSum += self.postOrder[i+1][1]
                    i += 1
                # Check for Gather operators

                result.append(round(currSum, 2))
                #currSum = 0

        self.prefixSumJoin = result

    def evaluateAQP(self, postOrder):
        """
        NOTE: This method would only be called if the query has a join operation.
        """
        if len(self.prefixSumJoin) == 0:
            self.generatePrefixSumJoin()

        currSum = 0
        result = list()
        joins = set(['Nested Loop', 'Hash Join', 'Merge Join'])

        for i in range(len(postOrder)):
            op = postOrder[i]
            currSum += op[1]

            if (op[0] in joins):
                if (i < len(postOrder)-1 and postOrder[i+1][0] == 'Gather'):
                    currSum += postOrder[i+1][1]
                    i += 1
                # Check for Gather operators

                result.append(round(currSum, 2))
                #currSum = 0

        diff = [round(result[i] - self.prefixSumJoin[i], 2)
                for i in range(len(result))]
        print("Cost of join subtrees in QEP: {}".format(self.prefixSumJoin))
        print("Relative increase in cost of join subtrees in AQP: {}".format(diff))

    def getAltQueryPlans(self):
        """
        This method would return a few representative AQPs by playing around with the default setting of the planner.

        Specifically,

        1. We disabled certain join algorithms as we feel the choice of join algorithm is a crucial companent in a QEP. PostgreSQL allows us to disable Merge, Hash and NL joins.
        2. Coming to the data sccess methods, we are going under the assumption the planner would choose the most efficient access method. Plus it's not as 'interesting' to play with.
        3. Regarding the other miscellaneous methods, we shall toggle them wrt to the join, eg:- don't turn of sort if theres a merge join.

        To reduce the search space we are going to perform an informed 'switching off' of the operators. As this method is likely to be called after the qep is generated, we shall 
        leverage the preorder traversal (stored in q) to help us switch off operators that appear in the query. [eg:- only turn off merge join if it's actually being used in the qep]

        """
        self.postOrder = self.getPostOrder(self.queryPlan, [])
        self.estimatedCost = self.getTotalCost(self.postOrder)

        print("Origical QEP")
        print(self.postOrder)
        print(f"Total Estimated Cost = {round(self.estimatedCost, 2)}")
        print()

        if (self.hasJoin):
            joins = ['HASHJOIN', 'MERGEJOIN', 'NESTLOOP', 'HASHJOIN']
            for i in range(3):
                j1, j2 = joins[i], joins[i+1]
                self.cursor.execute(f"SET ENABLE_{j1} TO OFF;")
                self.cursor.execute(f"SET ENABLE_{j2} TO OFF;")
                # Turn off the joins in pairs

                self.cursor.execute(
                    f"EXPLAIN (FORMAT JSON) {self.query}")
                # Need to peel away the wrappers from the raw output
                rawOutput = self.cursor.fetchall()
                altPlan = rawOutput[0][0][0]['Plan']
                self.altQueryPlans.append(altPlan)
                # Collect the alternative query plans

                self.cursor.execute(f"SET ENABLE_{j1} TO ON;")
                self.cursor.execute(f"SET ENABLE_{j2} TO ON;")
                # Re-enable the joins in pairs

                # self.cursor.execute("SHOW ALL")
                # rawOutput = self.cursor.fetchall()
                # print(rawOutput)
                # # For debugging, prints the runtime configuration

                print(f"Alternative Query Plan {i}")
                print(f"Operators disabled: {j1} and {j2}")
                aqp = self.getPostOrder(self.altQueryPlans[i], [])
                cost = self.getTotalCost(aqp)
                print(aqp)
                print()
                print(
                    f"Increase in Estimated Cost = {round(cost-self.estimatedCost, 2)}")
                print(
                    f"Relative increase in estimated cost = {round((cost-self.estimatedCost)/self.estimatedCost, 2)}")
                print()
                self.evaluateAQP(aqp)
                print("\n\n")

            else:
                pass

        return self.altQueryPlans
