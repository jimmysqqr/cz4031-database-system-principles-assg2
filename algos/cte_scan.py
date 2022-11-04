"""
CTE Scan Node Processor
"""

import annotation

def cte_scan(plan, isStart=False):
    output = annotation.getConnector(isStart)

    # If node type is "CTE Scan" 
    if plan["Node Type"] == "CTE Scan":
        output += "perform CTE scan on the relation: " + plan["CTE Name"]
        
        # Check if there is a condition in the index scan
        if "Index Cond" in plan:
            output += ", based on the following condition(s) "+ plan["Index Cond"].replace('::text', '')

        # Check if there are extra filters on the output of the CTE scan
        if "Filter" in plan:
            output += ". CTE scan output is further filtered based on these condition(s): " + plan["Filter"].replace('::text', '')

        output += ". "
        
    return output