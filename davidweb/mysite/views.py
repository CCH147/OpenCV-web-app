from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http.response import StreamingHttpResponse
import requests
import json
from mysite import models
from mysite import filter
from mysite import forms
from mysite import camera 
import cv2
import numpy as np
from django.conf import settings
from unidecode import unidecode
import random
import os
import sys
from subprocess import PIPE, run
from django.core.files.storage import FileSystemStorage


def home(request):
    return render(request, "mysite/nav.html")

 
def index(request):
    alldata = models.alldata.objects.all()
    end = models.enddate.objects.all()
    
    alldataFilter = filter.alldataFilter(queryset=alldata)
    
    if request.method == "POST":
        alldataFilter = filter.alldataFilter(request.POST, queryset=alldata)
 
    context = {
        'alldataFilter': alldataFilter,
        'enddate': end
    }
 
    return render(request, 'mysite/index.html', context)


def chart(request):
    alldata = models.alldata.objects.all()
    end = models.enddate.objects.all()
    alldataFilter = filter.alldataFilter(queryset=alldata)
 
    if request.method == "POST":
        alldataFilter = filter.alldataFilter(request.POST, queryset=alldata)
 
    context = {
        'alldataFilter': alldataFilter,
        'enddate': end
    }
 
    return render(request, 'mysite/chart2.html', context)

def our(request):
    end = models.enddate.objects.all()
    context = {
        'enddate': end
    }
    return render(request, 'mysite/our.html', context)

def datasum(request):
    alldata = models.alldata.objects.all()
    end = models.enddate.objects.all()
    alldataFilter = filter.alldataFilter(queryset=alldata)
 
    if request.method == "POST":
        alldataFilter = filter.alldataFilter(request.POST, queryset=alldata)
 
    context = {
        'alldataFilter': alldataFilter,
        'enddate': end
    }
    return render(request, 'mysite/datasum.html', context)

def image_view(request):

    form = forms.ImageForm()

    if request.method == 'POST':
        try:
            file = request.FILES['Original']
            obj_got, created = forms.Image.objects.get_or_create(Original = file)
            image = cv2.imread(obj_got.Original.path)

            if request.POST.get('filter') == 'Gray':
                effect=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

            if request.POST.get('filter') == 'Blur':           
                kernel = np.ones((5,5),np.float32)/25
                effect = cv2.filter2D(image,-1,kernel)

            if request.POST.get('filter') == 'Bright':
                effect=cv2.convertScaleAbs(image, beta=60)

            if request.POST.get('filter') == 'LessBright':
                effect=cv2.convertScaleAbs(image, beta=-60)

            if request.POST.get('filter') == 'Sharp':
                kernel = np.array([[-1, -1, -1], [-1, 9.5, -1], [-1, -1, -1]])
                effect = cv2.filter2D(image, -1, kernel)

            if request.POST.get('filter') == 'Sepia':
                img_sepia = np.array(image, dtype=np.float64)
                img_sepia = cv2.transform(img_sepia, np.matrix([[0.272, 0.534, 0.131],
                                        [0.349, 0.686, 0.168],
                                        [0.393, 0.769, 0.189]]))
                img_sepia[np.where(img_sepia > 255)] = 255
                effect = np.array(img_sepia, dtype=np.uint8)

            if request.POST.get('filter') == 'Sketch(Gray)':
                effect, sk_color = cv2.pencilSketch(image, sigma_s=60, sigma_r=0.07, shade_factor=0.1)

            if request.POST.get('filter') == 'Sketch(Colour)':
                sk_grey, effect = cv2.pencilSketch(image, sigma_s=60, sigma_r=0.07, shade_factor=0.1)

            if request.POST.get('filter') == 'HDR':
                effect=cv2.detailEnhance(image, sigma_s=12, sigma_r=0.15)

            if request.POST.get('filter') == 'Invert':
                effect=cv2.bitwise_not(image)

            cv2.imwrite(os.path.join(settings.MEDIA_ROOT, f'filtered_{obj_got.Original}'), effect)
            obj_got.Img = f'filtered_{obj_got.Original}'
            obj_got.save()
            return render(request, 'mysite/filtered.html',{'obj': obj_got})
        except Exception as err:
            print(err)
            return HttpResponse(status=500)
    return render(request, 'mysite/Image.html', {'form' : form})

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
def webcam(request):
	return StreamingHttpResponse(gen(camera.VideoCamera()),
					            content_type='multipart/x-mixed-replace; boundary=frame')
def index_webcam(request):
    return render(request, "mysite/webcam.html")
