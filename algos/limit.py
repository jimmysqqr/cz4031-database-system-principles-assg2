"""
Limit Node Processor
"""

import annotation

def limit(plan, output):
    # Process the child node fist
    annotation.processPlan(plan["Plans"][0], output)

    output_string = "Takes data from the previous operation and sorts based on attribute "

    if "DESC" in str(plan["Sort Key"]):
            output_string += str(plan["Sort Key"]).replace("DESC", "") + " in descending order. "
    else:
        output_string += str(plan["Sort Key"]) + " in ascending order. "

    output_string += "The sorted output is stored in " + plan["Sort Space Type"] + ". "
    
    # output_string = "Scanning of database is restricted to "
    # sum_of_rows = plan["Plan Rows"]
    # output_string += str(sum_of_rows) + " entries only."

    output.append(output_string)
    return