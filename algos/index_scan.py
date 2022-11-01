"""
Index Scan Node Processor
"""

import annotation

def index_scan(plan, isStart=False):
    # Process Index Scan node type:
    output = annotation.getConnector(isStart)

    # If node type is "Index Scan"
    if plan["Node Type"]=="Index Scan" or plan["Node Type"] == "Index Only Scan":
        output += "perform index scan on relation: " + plan["Relation Name"]
        output += ", with index: " + plan["Index Name"]

        # Check if there is a condition in the index scan
        if "Index Cond" in plan:
            output += ", based on the following condition(s): " + plan["Index Cond"].replace('::text', '')

        # Check if there are extra filters on the output of the index scan
        if "Filter" in plan:
            output += ". Index scan output is further filtered based on these condition(s): " + plan["Filter"].replace('::text', '')

        output += ". "

    return output
