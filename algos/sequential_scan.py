"""
Sequential Scan Node Processor
"""

import annotation

def sequential_scan(plan, isStart=False):
    # Process Sequential Scan node type
    output = annotation.getConnector(isStart)

    output += "perform Sequential Scan on relation: "

    # State the relation name
    if "Relation Name" in plan:
        output += plan["Relation Name"]
    
    # State the alias if it's different from the relation name
    if "Alias" in plan and plan["Relation Name"]!=plan["Alias"]:
        output += " as " + plan["Alias"]

    # Check if the sequential scan was done with a filter
    if "Filter" in plan:
        output += ", with condition: "
        output += plan['Filter'].replace("::text", "")

    output += ". "

    return output
    
