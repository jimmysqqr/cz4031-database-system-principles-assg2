"""
Append Node Processor
"""

import annotation

def append(plan, isStart=False):
    output = annotation.getConnector(isStart)

    # Explore the sub-plans of this node first (usually scan operators)
    if "Plans" in plan:
        for p in plan["Plans"]:
            output += annotation.processPlan(p, isStart) + " "
            if isStart:
                isStart = False

    # usually set operators (UNION, INTERSECT, EXCEPT)
    if plan["Node Type"] == "Append":
        output += "The scan outputs are then combined."

    return output