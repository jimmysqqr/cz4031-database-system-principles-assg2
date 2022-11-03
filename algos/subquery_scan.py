"""
Subquery Scan Node Processor
"""
import annotation

def subquery_scan(plan, isStart=False):
    # Process Subquery Scan node type
    output = ""

    if "Plans" in plan:
        for child in plan["Plans"]:
            output += annotation.processPlan(plan, isStart)
            if start:
                start = False

    output += annotation.getConnector(isStart)
    output += "do a subquery scan on the output of the sub-query in earlier operations"

    # Check if the sequential scan was done with a filter
    if "Filter" in plan:
        output += ", with condition: "
        output += plan['Filter'].replace('::text', '')

    output += ". "
    return output