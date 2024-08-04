from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import AsmePipe, FlangeRating
from numpy import interp
import ast
from typing import List, Dict, Any
import json
#import os

# Data directory
#data_dir = os.path.join(os.path.dirname(__file__), 'data')

# Functions
def parse_list_from_string(data: str) -> List[int]:
    """Safely parse a list of integers from a string."""
    return ast.literal_eval(data)

def calc_max_p(pipe_spec_list, design_t, design_p):
    """Calculate the maximum pressure for each pipe spec based on design temperature."""
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
    return pipe_spec_list

# Create your views here.
def home(request):
    return render(request, 'website/home.html',
                  {})

def pipe_data_sch(request):
    # Import engineering data
    asme_pipe = AsmePipe.objects.all()
    return render(request, 'website/pipe_data_sch.html',
                  {'asme_pipe': asme_pipe},
                  )


def pipe_data_flange(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        DT = data.get('design_temp')
        DP = data.get('design_press')
        print(DT, DP)
        # Your existing logic to calculate flange data
        flange_ratings = FlangeRating.objects.all()
        flange_data = []
        flange_ratings_set = set()
        for item in flange_ratings:
            max_pressure = parse_list_from_string(item.max_pressure)
            temp_range = parse_list_from_string(item.temp_range)
            pipe_class = {
                "material": item.material,
                "flange_rating": item.flange_rating,
                "max_p": max_pressure,
                "temp_range": temp_range
            }
            flange_data.append(pipe_class)
            flange_ratings_set.add(int(item.flange_rating))

        unique_flange_ratings = sorted(flange_ratings_set)
        flange_rating_list = calc_max_p(flange_data, DT, DP)

        organised_flange_data = {}
        for spec in flange_rating_list:
            material = spec['material']
            flange_rating = spec['flange_rating']
            if material not in organised_flange_data:
                organised_flange_data[material] = {}
            organised_flange_data[material][flange_rating] = {
                'max_p': spec['calculated_max_p'],
                'design_t': DT,
                'allowable': spec['acceptable']
            }

        return JsonResponse({
            'organised_flange_data': organised_flange_data,
            'unique_flange_ratings': unique_flange_ratings,
            'DT': DT,
            'DP': DP,
        })

    else:
        
        flange_ratings = FlangeRating.objects.all()

        # Save data to a list of dictionaries
        flange_data = []
        flange_ratings_set = set()
        for item in flange_ratings:
            max_pressure = parse_list_from_string(item.max_pressure)
            temp_range = parse_list_from_string(item.temp_range)
            pipe_class = {
                "material": item.material,
                "flange_rating": item.flange_rating,
                "max_p": max_pressure,
                "temp_range": temp_range
            }
            # Add to flange_data list
            flange_data.append(pipe_class)
            # Add to set of unique flange ratings
            flange_ratings_set.add(int(item.flange_rating))

        # Convert set to sorted list
        unique_flange_ratings = sorted(flange_ratings_set)
        
        # User Input DP & DT
        DT = 230  # deg C
        DP = 54  # barg

        flange_rating_list = calc_max_p(flange_data, DT, DP)

        # Organise data by material and flange rating
        organised_flange_data = {}
        #print(flange_rating_list)
        for spec in flange_rating_list:
            material = spec['material']
            flange_rating = spec['flange_rating']
            if material not in organised_flange_data:
                organised_flange_data[material] = {}
            organised_flange_data[material][flange_rating] = {'max_p':spec['calculated_max_p'],
                                                              'design_t': DT,
                                                              'allowable': spec['acceptable']}

        return render(request, 'website/pipe_data_flange.html', {
            'organised_flange_data': organised_flange_data,
            'unique_flange_ratings': unique_flange_ratings,
            'DT': DT,
            'DP': DP,
        })
##def pipe_data_flange(request):
##    # Import engineering data
##    flange_ratings = FlangeRating.objects.all()
##
##    # Save data to a list of dictionarys
##    flange_data = []
##    for item in flange_ratings:
##
##        max_pressure = item.max_pressure.split("[")[1].split(']')[0].split(",")
##        max_pressure = [eval(i) for i in max_pressure]
##        temp_range = item.temp_range.split("[")[1].split(']')[0].split(",")
##        temp_range = [eval(i) for i in temp_range]
##
##        pipe_class = {"material" : item.material,
##             "flange_rating": item.flange_rating,
##             "max_p": max_pressure,
##             "temp_range": temp_range
##             }
##        # Add to flange_data list
##        flange_data.append(pipe_class)
##    # User Input DP & DT
##    DT = 230 #deg C
##    DP = 54 # barg
##
##    def calc_max_p(pipe_spec_list, design_t, design_p):
##        # Loop through pipe specs and calculate max pressure for each pipe spec based on design temp
##        # For each pipe_spec in the list set X and Y co-ordinates for interpolation
##        print(pipe_spec_list)
##        for pipe_spec in pipe_spec_list:
##            if design_t > max(pipe_spec['temp_range']):
##                pipe_spec["calculated_max_p"] = 0
##            elif design_t < -29:
##                pipe_spec["calculated_max_p"] = 0
##            else:
##                x = pipe_spec['temp_range']
##                y = pipe_spec['max_p']
##                # Interpolate max pressure based on Design Temperature
##                pipe_spec["calculated_max_p"] = round(interp(design_t, x, y),2)
##            # Check if the required Design Pressure is higher than the calculated maximum
##            if design_p > pipe_spec["calculated_max_p"]:
##                pipe_spec["acceptable"] = False
##            else:
##                pipe_spec["acceptable"] = True
##        return pipe_spec_list
##
##    flange_rating_list = calc_max_p(flange_data, DT, DP)
##    
##    return render(request, 'website/pipe_data_flange.html',
##                  {'flange_rating_list': flange_rating_list,
##                   'DT': DT,
##                   'DP': DP},
##                  )
