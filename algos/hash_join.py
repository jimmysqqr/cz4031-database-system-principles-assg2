# Hash Join

import annotation

def hash_join(plan, isStart = False):
    # Process Hash Join

    output = ""

    temp = annotation.processPlan(plan["Plans"][1], isStart)
    output = output + temp + ""
    temp = annotation.processPlan(plan["Plans"][0])
    output = output + temp + ""

    output = output + "Next, Hash Join the 2 results from previous operations "
    output = output + plan["Join Type"] + "Join"

    if "Hash Cond" in plan:
        output = output + " with the condition " + plan["Hash Cond"].replace("::text", "") + "."
    else:
        output = output + "."

    return output