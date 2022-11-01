# Limit

import annotation

def limit(plan, isStart = False):
    output = annotation.processPlan(plan["Plans"][0], isStart)
    output = output + " Scan area is limited to "
    sum_of_rows = plan["Plan Rows"]
    output = output + str(sum_of_rows) + " entries "

    return output