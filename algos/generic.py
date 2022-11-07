"""
Generic Node Processor
"""
import annotation

def generic(plan, output):
    # Process unknown node type
    # output = annotation.getConnector(isStart)

    output_string = "Perform " + plan["Node Type"] + ". "

    if "Plans" in plan:
        for child in plan["Plans"]:
            output_string += " " + annotation.processPlan(child)

    output.append(output_string)
    return 