"""
Sort Node Processor
"""

import annotation


def sort(plan, output):
    # Recursive call
    if "Plans" in plan:
        for child in plan["Plans"]:
            annotation.processPlan(child, output)

    # Process Sort node type
    if plan["Node Type"] == "Sort":
        output_string = "Output results are sorted based on attribute "

        if "DESC" in str(plan["Sort Key"]):
            output_string += str(plan["Sort Key"]
                                 ).replace("DESC", "") + " in descending order."
        else:
            output_string += str(plan["Sort Key"]) + " in ascending order."

    output.append(output_string)
    return
