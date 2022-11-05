"""
Values Scan Node Processor
"""
import annotation

def values_scan(plan, isStart):
    # Process Values Scan node type
    output += annotation.getConnector(isStart)
    output += "the query processor will scan the literal VALUES clause. "

    return output