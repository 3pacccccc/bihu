from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def test(request):
    return HttpResponse("hello 2", content_type='application/json')