from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext, loader
import  urllib.request
from xml.dom.minidom import parseString
from datetime import datetime, date, time
from pyquery import PyQuery

from .models import IkeaItem


def index(req):
    all_ikea_items = IkeaItem.objects.order_by('datetime')
    template = loader.get_template('ikealist/index.html')
    context = {'all_ikea_items': all_ikea_items}
    return render(req, 'ikealist/index.html', context)

def detail(req, ikea_id):
    ikea = get_object_or_404(IkeaItem, pk = ikea_id)
    return render(req, 'ikealist/detail.html', {'ikea': ikea})

def add (req):
    selected_article = req.POST['article'].replace('.', '')
    response = urllib.request.urlopen('http://www.ikea.com/ru/ru/catalog/products/' + selected_article + '/')
   
    html_str = response.read().decode('utf-8')
    pq = PyQuery(html_str)

    curritem = IkeaItem(count=0, datetime=datetime.now(), status='n')
    

    for s in pq('meta'):
        try:
            if (s.attrib['name'] == 'product_name'):
                curritem.product_name = s.attrib[''].text()
            elif (s.attrib['name']== 'category_name'):
                curritem.category_name = s.attrib['content'].text()
            elif (s.attrib['name'] == 'price'):
                curritem.price = s.attrib['content'].text()
            elif (s.attrib['name'] == 'partnumber'):
                curritem.code = s.attrib['content'].text()
            elif (s.attrib['name'] == 'og:url'):
                curritem.url = s.attrib['content'].text()
            elif (s.attrib['name'] == 'og:image'):
                curritem.picture_url = s.attrib['content'].text()
        except Exception as ex:
            print('Error')

    curritem.save()
    return render(req, 'ikealist/detail.html', {'ikea': curritem})


