from django.shortcuts import render

from final_project.es_wrapper.es_wrapper import es_results_wrapper


def index(request):
    return render(request, 'index.html')


def search(request):
    if request.method == 'GET':
        query = request.GET.get('word')
        if query:
            results = es_results_wrapper(query)
            return render(request, 'search.html', {'results': results})
