from django.shortcuts import render, redirect
from django.http import JsonResponse

# Create your views here.


def index(request):
    return JsonResponse({"user": "unti"})

def home(request):
    return redirect("http://localhost:5173/")
