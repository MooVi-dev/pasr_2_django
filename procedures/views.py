import os
from datetime import datetime
from django.db.models import Sum
from django.db.models.functions import TruncDate, TruncDay
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView

from procedures.forms import ProcedureForm
from procedures.models import Procedure
from users.models import User
from graphs.service import load_file as service_load_file
import graphs.settings as settings


class ProcedureListView(ListView):
    """Список с группировкой"""
    model = Procedure

    def get_queryset(self):
        procedures = Procedure.objects.all().annotate(publish_date=TruncDate('docPublishDate'), ).order_by(
            'publish_date')
        return procedures


class ProcedureView(ListView):
    """Список лотов"""
    model = Procedure
    queryset = Procedure.objects.all()


@csrf_exempt
def load_file(request):
    doc_path = os.path.join(settings.DOWNLOAD_FOLDER, request.body.decode('utf-8'))
    data_to_db = service_load_file(doc_path)
    for data_item in data_to_db:
        new_lot = Procedure()
        new_lot.purchaseNumber = data_item.purchaseNumber
        docPublishDate = datetime.strptime(data_item.docPublishDate, "%Y-%m-%dT%H:%M:%S.%f%z")
        new_lot.docPublishDate = docPublishDate
        new_lot.purchaseObjectInfo = data_item.purchaseObjectInfo
        new_lot.regNum = data_item.regNum
        new_lot.fullName = data_item.fullName
        new_lot.maxPrice = data_item.maxPrice
        new_lot.save()

    return JsonResponse({'data': 'ok'})


class ProcedureCreate(CreateView):
    """Добавление лотов"""
    model = Procedure
    form_class = ProcedureForm


def graph(request):
    procedures = Procedure.objects.filter()
    procedures_all_total = procedures.count()
    context = {'procedures_all_total': procedures_all_total}
    return render(request, 'graphs.html', context)


def home(request):
    return render(request, 'procedures/home.html')


def lots_chart(request):
    labels = []
    data = []

    queryset = Procedure.objects.values('docPublishDate').annotate(price=Sum('maxPrice')).order_by('price')
    for entry in queryset:
        labels.append(entry['docPublishDate'])
        data.append(entry['price'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def data_by_curators(request):
    curators = Procedure.objects.all().values("curator").distinct()
    dates = Procedure.objects.all().values("docPublishDate").distinct().order_by('docPublishDate')

    labels = []
    json_dict = []
    for e in dates:
        labels.append(e['docPublishDate'])
    for e in curators:
        id = e['curator']
        price_by_curators = Procedure.objects.filter(curator=id).order_by('docPublishDate')
        prices = [0] * len(labels)
        for price in price_by_curators:
            # print(f'maxPrice = {price.maxPrice}, docPublishDate = {price.docPublishDate}')
            prices[labels.index(price.docPublishDate)] += price.maxPrice
        try:
            user_name = str(User.objects.get(id=id))
        except Exception as err:
            user_name = ''
        item_dict = dict()
        item_dict['label'] = user_name
        item_dict['backgroundColor'] = '#6dae7f'
        item_dict['data'] = prices
        json_dict.append(item_dict)

    # price_by_all = Procedure.objects.annotate(tranc_date=TruncDay('docPublishDate'),).values('maxPrice').annotate(
    price_by_all = Procedure.objects.annotate(sum_price=Sum('maxPrice')).order_by('docPublishDate')
    prices = [0] * len(labels)
    for price in price_by_all:
        # print('5')
        # print(price)
        # print(price.docPublishDate)
        print(f'maxPrice = {price.sum_price}, docPublishDate = {price.docPublishDate}')
        prices[labels.index(price.docPublishDate)] += price.sum_price
    item_dict = dict()
    item_dict['label'] = 'all'
    item_dict['backgroundColor'] = '#1dae7f'
    item_dict['data'] = prices
    json_dict.append(item_dict)

    print(json_dict)

    return JsonResponse(data={
        'data': json_dict,
        'labels': labels
    })
