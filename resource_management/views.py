from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'resource_management/index.html', {
        'title': 'Manage Resources'
    })