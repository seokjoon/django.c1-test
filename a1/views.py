# from django.shortcuts import render

from rest_framework import generics
from .models import App
from .serializers import AppSerializer

# from django.http import HttpRequest
from django.http import HttpResponse

from django.shortcuts import redirect

from .crawling import exec

def foo(request):
	keyword = request.GET.get('keyword')
	outs = exec(keyword)
	# return HttpResponse(outs)
	return redirect('/app/')


class AppList(generics.ListCreateAPIView):
	queryset = App.objects.all()
	serializer_class = AppSerializer


class AppDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = App.objects.all()
	serializer_class = AppSerializer
