"""
This is the main file which is used to traverse/parse the query plan
"""
import random

import algos.generic as generic_algo
import algos.nested_loop as nested_loop
import algos.sequential_scan as sequential_scan
import algos.index_scan as index_scan
import algos.subquery_scan as subquery_scan
import algos.unique as unique
import algos.values_scan as values_scan
import algos.group as group
import algos.hash as hash
import algos.function_scan as function_scan
import algos.cte_scan as cte_scan
import algos.append as append

# PlanTraverser class
class PlanTraverser:
    # Constructor
    def __init__(self):
        # Instance variables
        self.Generic = generic_algo.generic
        self.Nested_Loop = nested_loop.nested_loop
        self.Seq_Scan = sequential_scan.sequential_scan
        self.Index_Scan = index_scan.index_scan
        self.Subquery_Scan = subquery_scan.subquery_scan
        self.Unique = unique.unique
        self.Hash = hash.hash
        self.Function_Scan = function_scan.function_scan
        self.Values_Scan = values_scan.values_scan
        self.Group = group.group
        self.CTE_Scan = cte_scan.cte_scan
        self.Append = append.append

# Function to process a plan (which is in json format)
def processPlan(plan, isStart=False):
    # Instantiate the PlanTraverser class
    # This is where the recursion occurs
    traverser = PlanTraverser()

    try:
        # Get the traverser object's instance variable. Basically getting the correct algo for the node type
        processor = getattr(traverser, plan["Node Type"].replace(" ", "_"))

    except:
        # A generic algo to use if the particular Node Type cannot be found in the traverser object's instance variables
        processor = traverser.Generic
    
    processedPlan = startPlan(plan, isStart)
    processedPlan += processor(plan, isStart)
    return processedPlan

# TODO@darren: Change to include different connectors (different from wlee)
CONNECTORS = ["After that, ", "Then, ", "Next, ", "Subsequently, "]

# Get random word to connect two sentences together
def getConnector(isStart=False):
    if isStart:
        # TODO@darren: Remember to change this lol
        return "In the beninging, "

    return random.choice(CONNECTORS)

# Function to start the plan
def startPlan(plan, isStart=False):
    result = ""

    # Checking for InitPlan. # TODO@darren: figure out what this shit is 
    if "Parent Relationship" in plan:
        if plan["Parent Relationship"] == "InitPlan":
            result = getConnector(isStart)
            result += "The " + plan["Node Type"]
            result += " is the root node??? Not sure what this is yet"

    return result
