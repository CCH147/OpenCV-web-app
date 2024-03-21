from django.db import models

  
class alldata(models.Model):
    
    year_Choice = (
        ('2019', '2019年'),
        ('2020', '2020年'),
        ('2021', '2021年'),
        ('2022', '2022年'),
        ('2023', '2023年'),
    )
    Season_Choice = (
        ('Spring', '春'),
        ('Summer', '夏'),
        ('Autumn', '秋'),
        ('Winter', '冬'),
    )
    area_Choice =  (
        ('North',  '北部'),
        ('Middle', '中部'),
        ('South',  '南部'),
        ('East',   '東部'),
    )
  
    year = models.CharField(max_length = 255,choices= year_Choice)
    season = models.CharField(max_length = 255, choices= Season_Choice)
    area = models.CharField(max_length = 255, choices= area_Choice)
    self_avg = models.DecimalField(max_digits=20, decimal_places=2,blank=True, null=True, default=0)
    industry_avg = models.DecimalField(max_digits=20, decimal_places=2,blank=True, null=True, default=0)


class enddate(models.Model):
    year = models.CharField(max_length = 255)
    month = models.CharField(max_length = 255)
    
class Image(models.Model):
    Original = models.ImageField(null=True, blank=True)
    Img = models.ImageField(null=True,blank=True)