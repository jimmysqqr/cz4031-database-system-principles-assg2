# Limit

import annotation

def limit(plan, isStart = False):
    # Dict to add
    q_item = {}
    q_item["Mode Type"] = plan["Node Type"]
    q_item["Relation Name"] = plan["Relation Name"]
    q_item["Total Cost"] = plan["Total Cost"]

    queue.append(q_item)


    output = annotation.processPlan(plan["Plans"][0], queue, isStart)
    output = output + "Scanning of database is restricted to "
    sum_of_rows = plan["Plan Rows"]
    output = output + str(sum_of_rows) + " entries only."

    return output