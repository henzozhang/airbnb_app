from django.shortcuts import render

# Create your views here.
def home_view(request):
    
    # import pudb;pu.db()
    return render(request, 'afficharge/home_page.html')

def about_view(request):
    return render(request, 'divers/about_page.html')