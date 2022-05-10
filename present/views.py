from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'present/index.html', {
        'title': 'Model Execution Form',
    })