import psycopg2


class DBConnection:
    def __init__(self, host="localhost", port='5432', dbname="TPC-H", user="postgres", password=""):
        # Initialize the class variables
        self.cursor = None
        self.connection = None
        self.query = ""
        self.queryPlan = {}
        self.annotatedPlan = ""

        try:
            # Connecting to the database and initializing the cursor as class variables
            self.connection = psycopg2.connect(
                host=host, port=port, dbname=dbname, user=user, password=password)
            self.cursor = self.connection.cursor()
            print("Connected to PostgreSQL successfully!")

        except (Exception, psycopg2.Error) as error:
            # Error handling
            print("Error while connecting to PostgreSQL: ", error)

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

        rawOutput = self.cursor.fetchall()
        plan = rawOutput[0][0][0]['Plan']
        self.queryPlan = plan

        return self.queryPlan