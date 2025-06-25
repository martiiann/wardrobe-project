from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def shop(request):
    return render(request, 'shop.html')

def mens_clothing(request):
    return render(request, 'mens.html')  # You'll create this page later

def womens_clothing(request):
    return render(request, 'womens.html')  # You'll create this page later
