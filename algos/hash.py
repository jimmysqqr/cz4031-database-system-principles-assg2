"""
Hash Node Processor
"""

import annotation

def hash(plan, isStart=False):

    if "Plans" in plan:
        output = annotation.processPlan(plan['Plans'][0], isStart)
    else:
        output = annotation.getConnector(isStart)
    
    output += " Hash index is created on the previous relation."

    return output