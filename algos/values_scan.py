"""
Values Scan Node Processor
"""
import annotation

def values_scan(plan, output):
    # Process Values Scan node type
    output_string = "The query processor will scan the literal VALUES clause. "
    
    output.append(output_string)
    return