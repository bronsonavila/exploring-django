from django.shortcuts import render


# All views must accept a `request` parameter, even if not actually used.
def home(request):
    return render(request, 'home.html')
