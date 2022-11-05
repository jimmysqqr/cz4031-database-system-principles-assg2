"""
GroupAggregate Node Processor
"""
import annotation
import json
def aggregate(plan, isStart=False):

    output = annotation.getConnector(isStart)

    # aggregate row that are already sorted (from a sorted attr or index scan)
    # also process GROUP BY and/or HAVING/FILTER operator if necessary
    if plan["Strategy"] == "Sorted":
        output = annotation.processPlan(plan["Plans"][0], isStart) + " "
        if "Group Key" in plan:
            if len(plan["Group Key"]) == 1:
                output += "The sorted rows are grouped based on the key: "
                output += plan["Group Key"][0].replace("::text", "")
            else:
                output += "The sorted rows are grouped based on the keys: ("
                for key in plan["Group Key"]:
                    output += key.replace("::text", "") + ", "
                output = output[:-2] + ")"
        if "Filter" in plan: 
            output += " and filter the groups based on these condition(s): " + plan["Filter"].replace("::text", "")
        output += "."
        return output

    # aggregate function + group by operator
    if plan["Strategy"] == "Hashed":
        output = annotation.processPlan(plan["Plans"][0], isStart) + " "
        if len(plan["Group Key"]) == 1:
            output += "All rows are hashed and grouped based on the key: "
            output += plan["Group Key"][0].replace("::text", "")
        else:
            output += "All rows are hashed and grouped based on the keys: ("
            for key in plan["Group Key"]:
                output += key.replace("::text", "") + ", "
            output = output[:-2] + ")"
        output += ", then the desired row of each group is aggregated and outputted."
        return output

    # aggregate functions only: COUNT, MAX, MIN, etc...
    if plan["Strategy"] == "Plain":
        output = annotation.processPlan(plan["Plans"][0], isStart) + " "
        output += "Aggregate the output."
        return output
