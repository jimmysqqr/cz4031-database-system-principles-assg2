"""
Limit Node Processor
"""

import annotation

def limit(plan, output):
    # Process the child node fist
    annotation.processPlan(plan["Plans"][0], output)
    
    output_string = "Scanning of data is restricted to " + str(plan["Plan Rows"]) + " entries only."

    output.append(output_string)
    return