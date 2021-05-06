import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from django.shortcuts import render

from final_project.es_wrapper.es_wrapper import es_results_wrapper


def homepage(request):
    return render(request, 'home.html')


def results(request):
    if request.method == "POST":
        query = request.POST.get('search')
        if query:
            results = es_results_wrapper(query)
            return render(request, 'results.html', {'pdf': results})
