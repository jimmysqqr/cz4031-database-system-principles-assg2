import json 
import psycopg2

class DBConnection:
    def __init__(self, host="localhost", port='5432', dbname="TPC-H", user="postgres", password=""):
        self.cursor = None
        self.connection = None
        # Initialize the class variables

        try:
            # Connecting to the database and initializing the cursor as class variables
            self.connection = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
            self.cursor = self.connection.cursor()
            print("Connected to PostgreSQL successfully!")

        except (Exception, psycopg2.Error) as error:
            # Error handling
            print("Error while connecting to PostgreSQL: ", error)

        finally:
            # Closing the database connection
            if self.connection is not None:
                self.cursor.close()
                self.connection.close()
                print("PostgreSQL connection has been closed.")

if __name__ == '__main__':
    p = DBConnection(host="localhost", port="5432", dbname="TPC-H", user="postgres", password="chellappas")
    print(p)

