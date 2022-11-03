"""
Unique Node Processor
"""
import annotation

def unique(plan, isStart=False):
    # Process Unique node type
    output = annotation.processPlan(plan["Plans"][0], isStart) + " "
    output += annotation.getConnector()
    output += "the sorted output will be scanned with the Unique operator and adjacent duplicates will be eliminated. "
    output += "The Unique operator is used as it is useful for DISTINCT clauses if the input is already sorted (the query also includes ORDER BY). "
    return output