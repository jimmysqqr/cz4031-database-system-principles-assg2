"""
GroupAggregate Node Processor
"""
import annotation


def aggregate(plan, output):
    output_string = ""

    # Aggregate row that are already sorted (from a sorted attr or index scan)
    # also process GROUP BY and/or HAVING/FILTER operator if necessary
    if plan["Strategy"] == "Sorted":
        annotation.processPlan(plan["Plans"][0], output)
        if "Group Key" in plan:
            if len(plan["Group Key"]) == 1:
                output_string += "The sorted rows are grouped based on the key: "
                output_string += plan["Group Key"][0].replace("::text", "")
            else:
                output_string += "The sorted rows are grouped based on the keys: ("
                for key in plan["Group Key"]:
                    output_string += key.replace("::text", "") + ", "
                output_string = output_string[:-2] + ")"
        if "Filter" in plan:
            output_string += " and filter the groups based on these condition(s): " + plan["Filter"].replace(
                "::text", "")
        output_string += "."

    # aggregate function + group by operator
    if plan["Strategy"] == "Hashed":
        annotation.processPlan(plan["Plans"][0], output)
        if len(plan["Group Key"]) == 1:
            output_string += "All rows are hashed and grouped based on the key: "
            output_string += plan["Group Key"][0].replace("::text", "")
        else:
            output_string += "All rows are hashed and grouped based on the keys: ("
            for key in plan["Group Key"]:
                output_string += key.replace("::text", "") + ", "
            output_string = output_string[:-2] + ")"
        output_string += ", then the desired row of each group is aggregated and outputted."

    # aggregate functions only: COUNT, MAX, MIN, etc...
    if plan["Strategy"] == "Plain":
        annotation.processPlan(plan["Plans"][0], output)
        output_string += "Aggregate the output."

    output.append(output_string)
    return
