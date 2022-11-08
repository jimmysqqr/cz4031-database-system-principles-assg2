"""
Function Scan Node Processor
"""


def function_scan(plan, output):
    # Build annotation for function scan
    output_string = "The function " + \
        plan["Function Name"] + " is executed and a set of records is outputted."

    output.append(output_string)

    return
