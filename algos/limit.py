# Limit

import annotation

def limit(plan, isStart = False):
    output = annotation.processPlan(plan["Plans"][0], isStart)
    output = output + "Scanning of database is restricted to "
    sum_of_rows = plan["Plan Rows"]
    output = output + str(sum_of_rows) + " entries only."

    return output