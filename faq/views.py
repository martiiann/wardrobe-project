from django.shortcuts import render

def faq_page(request):
    return render(request, 'faq/faq.html')
