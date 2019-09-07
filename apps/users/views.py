from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.


def test(request):
    return HttpResponse("hello 5", content_type='application/json')


def verify(request):
    return HttpResponse('pycB7iWgN8uTQBUx8PiEjsRfPlqOXglff63pCTCLtsM.vQCFhMEdspQRFGVJje2AbyO-qe2ynoA7WcDqKELIIoA', content_type='application/json')
