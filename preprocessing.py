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
        self.prefixSumJoin = list()
        self.nodeCount = 1

        # For evaluating the representative alternative query plans
        self.altQueryPlans = list()
        self.queryCostDict = dict()
        self.joinTreeCostDict = dict()
        self.nodeList = list()

        try:
            # Connecting to the database and initializing the cursor as class variables
            self.connection = psycopg2.connect(
                host=host, port=port, dbname=dbname, user=user, password=password)
            self.connection.autocommit = True
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
        try:
            self.cursor.execute(
                f"EXPLAIN (FORMAT JSON) {self.query}")
        except Exception as e:
            err_msg_list = str(e).split('\n')
            err_msg = err_msg_list[0]
            for msg in err_msg_list:
                if "HINT" in msg:
                    err_msg += f"\n{msg}"
            return err_msg
        else:
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

    def getAdjList(self, queryPlan, result):
        """
        This method performs a post order DFS traversal on the query plan (a nested dictionary) and returns an adjacency list of operators as a dict type
            { parent node : [child node 1, child node 2, ...] }

        We use a count to keep track of the number of nodes visited and append it to the end of each node to make it unique 
        (else, there would be multiple Seq Scan's will be taken as the same node, when actually they are distinct Seq Scan's in the QEP)
            {
                "Hash Join#1" : ["Seq Scan#2", "Aggregate#3"], 
                "Aggregate#3" : ["Sort#4", "Seq Scan#5"]
            }
        """

        # Leaf node
        if 'Plans' not in queryPlan:
            if self.nodeCount == 1:
                self.nodeList.append(
                    f"{queryPlan['Node Type']}#{self.nodeCount}")
            curIterCount = self.nodeCount
            self.nodeCount += 1
            return [result, curIterCount]

        # Node with child nodes
        else:
            # Name the parent node, increment the count
            planNodeType = f"{queryPlan['Node Type']}#{self.nodeCount}"
            if planNodeType not in self.nodeList:
                self.nodeList.append(planNodeType)

            # Keep track of count in this recursion iteration
            curIterCount = self.nodeCount
            self.nodeCount += 1

            # DFS: keep traversing until leaf node is reached
            for subplan in queryPlan['Plans']:
                nextIterCount = self.getAdjList(subplan, result)[1]

                # Name the child node, increment the count
                subplanNodeType = f"{subplan['Node Type']}#{nextIterCount}"
                if subplanNodeType not in self.nodeList:
                    self.nodeList.append(subplanNodeType)

                # Add the child node to its parent node in the adjacency list
                if planNodeType in result:
                    result[planNodeType].append(subplanNodeType)
                else:
                    result[planNodeType] = [subplanNodeType]

            # return curIterCount (OR, in the 1st iteration, return the final result)
            return [result, curIterCount]


    def getTotalCost(self, postOrder):
        """
        This method evaluates the total estimated cost of the query plan scanning it's post order traversal.
        """
        result = 0

        for op in postOrder:
            result += op[1]

        return result


    def getPrefixSumJoin(self):
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
                currSum = 0
                # Reset the curSum to 0 (This helps isolate the cost of the join operator better)

        return result


    def evaluateAQP(self, postOrder, key):
        """
        NOTE: This method would only be called if the query has a join operation.
        """
        self.prefixSumJoin = self.getPrefixSumJoin()

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
                currSum = 0
                # Reset the curSum to 0 (This helps isolate the cost of the join operator better)

        self.joinTreeCostDict[key] = result

    def getAltQueryPlans(self):
        """
        This method would return a few representative AQPs by playing around with the default setting of the planner.

        Specifically,

        1. We disabled certain join algorithms as we feel the choice of join algorithm is a crucial companent in a QEP. PostgreSQL allows us to disable Merge, Hash and NL joins.
        2. Coming to the data access methods, we are going under the assumption the planner would choose the most efficient access method. Plus it's not as 'interesting' to play with.
        3. Regarding the other miscellaneous methods, we shall toggle them wrt to the join, eg:- don't turn of sort if theres a merge join.

        To reduce the search space we are going to perform an informed 'switching off' of the operators. As this method is likely to be called after the qep is generated, we shall 
        leverage the preorder traversal (stored in q) to help us switch off operators that appear in the query. [eg:- only turn off merge join if it's actually being used in the qep]

        """
        self.altQueryPlans = list()
        self.postOrder = self.getPostOrder(self.queryPlan, [])
        self.estimatedCost = self.getTotalCost(self.postOrder)

        if (self.hasJoin):
            joins = ['HASHJOIN', 'MERGEJOIN', 'NESTLOOP', 'HASHJOIN']
            for i in range(3):
                j1, j2 = joins[i], joins[i+1]
                self.cursor.execute(f"SET ENABLE_{j1} TO OFF;")
                self.cursor.execute(f"SET ENABLE_{j2} TO OFF;")
                # Turn off the joins in pairs

                self.cursor.execute(
                    f"EXPLAIN (FORMAT JSON) {self.query}")
                rawOutput = self.cursor.fetchall()
                # Execute query and fetch the query execution plan from PostgreSQL

                altPlan = rawOutput[0][0][0]['Plan']
                self.altQueryPlans.append(altPlan)
                # Collect the alternative query plans

                self.cursor.execute(f"SET ENABLE_{j1} TO ON;")
                self.cursor.execute(f"SET ENABLE_{j2} TO ON;")
                # Re-enable the joins in pairs

                # self.cursor.execute("SHOW ALL")
                # rawOutput = self.cursor.fetchall()
                # print(rawOutput)
                # For debugging, prints the runtime configuration

                aqp = self.getPostOrder(self.altQueryPlans[i], [])
                cost = self.getTotalCost(aqp)
                # Computing the postorder of the AQP and it's estimated total cost

                key = list(
                    set(['HASHJOIN', 'MERGEJOIN', 'NESTLOOP']) - set([j1, j2]))[0]
                self.queryCostDict[key] = cost
                # Adding the cost to a class dictionary (key is just a protracted way to retrieve the join type!)

                self.evaluateAQP(aqp, key)
                # Evaluating the relative increase (or decrease) in cost when the operator is swapped out in the query plan

        else:
            """
            Room for extension. We personally feel it's only necessary to retrieve the AQPs for annotating the joins as it gives the user valuable insight on how 
            the different join algorithms affect the cost of the query. However when it comes to index scan it is well know that the Sequential Scan is the worst 
            scan a query could execute. We assume the QEP would prefer other scans if applicable and knowing the cost difference would not provide much insight.

            Hence we do not retrieve the AQPs for queries without joins.
            """
            pass

        #print(f"{len(self.altQueryPlans)} alternate query plans were retrieved.")
        return
