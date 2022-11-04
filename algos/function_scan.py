"""
Function Scan Node Processor
"""

import annotation

def function_scan(plan, isStart=False):
    output = annotation.getConnector(isStart)

    output += "The function " + plan["Function Name"] + " is executed and a set of records is outputted."

    return output