from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {
        'title': 'PITHIA e-Science Centre Home',
    })

def index_admin(request):
    return render(request, 'index_admin.html', {
        'title': 'PITHIA e-Science Centre Home - Admin',
    })