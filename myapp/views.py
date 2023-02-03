from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from myapp.management.commands import stocks, drawer
import mplfinance as mf
from myapp.models import Trades
from django_pandas.io import read_frame
import pandas as pd


def index(request):
    plt = drawer.get_svg2http_response(250, "7203.jp")
    return HttpResponse(plt)


def home(request):
    return redirect("http://localhost:5173/")
