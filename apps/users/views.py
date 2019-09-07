from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def test(request):
    a = 1 / 0
    return HttpResponse("hello88", content_type='application/json')