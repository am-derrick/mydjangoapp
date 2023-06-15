from django.shortcuts import render


def signup(request):
    """sign up view"""
    return render(request, 'signup.html')
