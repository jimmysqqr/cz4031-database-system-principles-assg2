"""
Append Node Processor
"""

import annotation

def append(plan, output):
    output_string = ""

    # Explore the sub-plans of this node first (usually scan operators)
    if "Plans" in plan:
        for p in plan["Plans"]:
            annotation.processPlan(p, output)

    # usually set operators (UNION, INTERSECT, EXCEPT)
    if plan["Node Type"] == "Append":
        output_string += "The scan outputs are then combined."

    output.append(output_string)
    return output