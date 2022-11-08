"""
Generic Node Processor
"""
import annotation

def generic(plan, output):
    # Process unknown node type
    output_string = "Perform " + plan["Node Type"] + ". "

    if "Plans" in plan:
        for child in plan["Plans"]:
            annotation.processPlan(child, output)

    output.append(output_string)
    return 