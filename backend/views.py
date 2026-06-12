from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'pages/dashboard.html')

def about(request):
    return render(request, 'pages/about.html')