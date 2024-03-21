from mysite.models import alldata,enddate
import django_filters
 
class alldataFilter(django_filters.FilterSet):
    
    class Meta:
        model = alldata
        fields = '__all__'

class enddatefilter(django_filters.FilterSet):
    
    class Meta:
        model = enddate
        fields = '__all__'
