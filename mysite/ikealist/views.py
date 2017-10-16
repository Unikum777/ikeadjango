from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext, loader
import  urllib
from xml.dom.minidom import parseString
from datetime import datetime, date, time
from pyquery import PyQuery

from .models import IkeaItem
import re

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
    urllib_req = 'http://www.ikea.com/ru/ru/catalog/products/' + selected_article + '/'
    urllib_req_S = 'http://www.ikea.com/ru/ru/catalog/products/S' + selected_article + '/'
    
    response = ''

    try:
        response = urllib.request.urlopen(urllib_req)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            response = urllib.request.urlopen(urllib_req_S)
   
    html_str = response.read().decode('utf-8')
    pq = PyQuery(html_str)

    curritem = IkeaItem(count=0, datetime=datetime.now(), status='n')
    

    for s in pq.find('meta'):
        try:
            attrib_value = s.attrib['content']
            attrib_name = ''
            try:
                attrib_name = s.attrib['name']
            except:
                attrib_name = s.attrib['property']

            if (attrib_name == 'title'):
                curritem.title = attrib_value 
            elif (attrib_name == 'product_name'):
                curritem.product_name = attrib_value
            elif (attrib_name == 'category_name'):
                curritem.category_name = attrib_value
            elif (attrib_name == 'price'):
                curritem.price = re.sub(r'[\s\.–]', '', attrib_value)
            elif (attrib_name == 'partnumber'):
                curritem.code = attrib_value
            elif (attrib_name == 'og:url'):
                curritem.url = attrib_value
            elif (attrib_name == 'og:image'):
                curritem.picture_url = attrib_value
        except Exception as ex:
            print('Error ', ex)

    print (curritem)
    curritem.save()
    return render(req, 'ikealist/detail.html', {'ikea': curritem})


