from numpy import interp
import ast
from typing import List, Dict, Any
import math
# Functions
def parse_list_from_string(data: str) -> List[int]:
    """Safely parse a list of integers from a string."""
    return ast.literal_eval(data)

def calc_max_p(pipe_spec_list, design_t, design_p):
    """Calculate the maximum pressure for each pipe spec based on design temperature."""
    try:
        for pipe_spec in pipe_spec_list:
            if design_t > max(pipe_spec['temp_range']):
                pipe_spec["calculated_max_p"] = 0
            elif design_t < -29:
                pipe_spec["calculated_max_p"] = 0
            else:
                x = pipe_spec['temp_range']
                y = pipe_spec['max_p']
                # Interpolate max pressure based on Design Temperature
                pipe_spec["calculated_max_p"] = round(interp(design_t, x, y), 2)
            # Check if the required Design Pressure is higher than the calculated maximum
            pipe_spec["acceptable"] = design_p <= pipe_spec["calculated_max_p"]
    except TypeError:
        pipe_spec_list = None
    return pipe_spec_list

def calculate_XSA(dia):
    """Calculate the cross sectional area of a pipe spec based on diameter."""
    return round(math.pi* (dia / 2) ** 2)