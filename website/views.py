from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from .models import AsmePipe, FlangeRating
from .calcs import *
import json
#import os

# Data directory
#data_dir = os.path.join(os.path.dirname(__file__), 'data')

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
        try:
            DT = float(request.POST.get('inputDesignTemp', 65))  # Default to 65 if no input
            DP = float(request.POST.get('inputDesignPress', 15.0))  # Default to 18.0 if no input
        except ValueError:
            DT = None  # Fallback to default value if input is invalid
            DP = None
        
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
        if flange_rating_list:
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

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                table_html = render_to_string('website/pipe_data_flange_table.html', {
                    'organised_flange_data': organised_flange_data,
                    'unique_flange_ratings': unique_flange_ratings,
                    'DT' : DT,
                    'DP': DP,
                })
                return JsonResponse({'table_html': table_html})
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                table_html = render_to_string('website/pipe_data_flange_table.html', {
                    'organised_flange_data': None,
                    'unique_flange_ratings': None,
                    'DT' : None,
                    'DP': None,
                })
                return JsonResponse({'table_html': table_html})
    else:
        DT = 65  # Default diameter if not POST request
        DP = 15.0  # Default diameter if not POST request
        return render(request, 'website/pipe_data_flange.html', {
            'DT': DT,
            'DP': DP,
        })


def calc_xsa(request):
    if request.method == 'POST':
        try:
            dia = float(request.POST.get('inputDia', 25))  # Default to 25 if no input
            pipeXSA = calculate_XSA(dia)
        except ValueError:            
            pipeXSA = None 
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'pipeXSA': f"{pipeXSA:.2f}"})        
    else:
        dia = None  # Default diameter if not POST request
        pipeXSA = 0

    return render(request, 'website/calc_xsa.html', {
        'pipeXSA': pipeXSA,
        'dia': dia,
    })

