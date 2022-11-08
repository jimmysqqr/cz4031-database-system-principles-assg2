"""
Group Node Processor
"""

import annotation

def group(plan, output):
    # Recursive step
    if "Plans" in plan:
        annotation.processPlan(plan['Plans'][0], output)

    # Building the annotation for Group operator
    if len(plan["Group Key"]) == 1:
        output_string = "The output from the previous operation is grouped based on the key: "
        output_string += plan["Group Key"][0].replace("::text", "")

    else:
        output_string = "The output from the previous operation is grouped based on the tuple of keys: ("

        for key in plan["Group Key"]:
            output_string += key.replace("::text", "") + ", "
        output_string = output_string[:-2] + ")"

    output_string += "."

    output.append(output_string)

    return
