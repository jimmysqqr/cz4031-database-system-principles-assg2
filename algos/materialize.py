"""
Materialize Node Processor
"""

import annotation

def materialize(plan, output):
    output_string = ""

    if "Plans" in plan:
        for child in plan["Plans"]:
            annotation.processPlan(child, output)

    if plan["Node Type"] == "Materialize":
        output_string += "Materialize the results in main memory to avoid re-computing the values."

    output.append(output_string)
    return