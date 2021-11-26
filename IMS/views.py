from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import HttpResponse
from tablib import Dataset
from .models import Data, Part, Delivery
from .form import DataForm, DeliveryForm
from .resources import DataResource
from .sendmail import sendmail

# Create your views here.

@login_required
def dashboard(request):
    parts = Part.objects.values("part")

    part_list = []
    for i in range(len(parts)-1):
        a = list(parts[i].values())
        part_list.append(a[0])

    all_statistics = []
    for part in part_list:
        part_statistics = []

        print(Data.objects)
        total = Data.objects.filter(part__part=part)
        total_cnt = total.count()

        stock = Data.objects.filter(part__part=part, status="2")
        stock_cnt = stock.count()

        apply = Data.objects.filter(part__part=part, status="3")
        apply_cnt = apply.count()

        rma = Data.objects.filter(part__part=part, status="1")
        rma_cnt = rma.count()

        part_statistics.append(part)
        part_statistics.append(total_cnt)
        part_statistics.append(stock_cnt)
        part_statistics.append(apply_cnt)
        part_statistics.append(rma_cnt)
        all_statistics.append(part_statistics)

    return render(request, 'IMS/main.html', {'all_statistics': all_statistics})

@login_required
def data_list(request):
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    # 조회
    datas = Data.objects.order_by('-created_date')
    # 페이징처리
    paginator = Paginator(datas, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    return render(request, 'IMS/data_list.html', {'datas': page_obj})

@login_required
def data_detail(request, pk):
    data = get_object_or_404(Data, pk=pk)
    return render(request, 'IMS/data_detail.html', {'data': data})

@login_required
def data_new(request):
    if request.method == "POST":
        form = DataForm(request.POST)
        created_date = timezone.now()
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.created_date = created_date
            data.save()
            return redirect('data_detail', pk=data.pk)
    else:
        form = DataForm()
    return render(request, 'IMS/data_edit.html', {'form': form})

@login_required
def data_edit(request, pk):
    data = get_object_or_404(Data, pk=pk)
    if request.method == "POST":
        form = DataForm(request.POST, instance=data)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.created_date = timezone.now()
            data.save()
            return redirect('data_detail', pk=data.pk)
    else:
        form = DataForm(instance=data)
    return render(request, 'IMS/data_edit.html', {'form': form})

@login_required
def data_delete(request, pk):
    data = Data.objects.get(pk=pk)
    data.delete()
    return redirect('IMS/list')

@login_required
def search(request):
    datas = Data.objects.all().order_by('-id')
    q = request.POST.get('q', "")
    if q:
        datas = datas.filter(
            Q(serial__icontains=q) |
            Q(hostname__icontains=q) |
            Q(description__icontains=q) |
            Q(vendor__vendor__icontains=q) |
            Q(part__part__icontains=q) |
            Q(status__status__icontains=q) |
            Q(next_serial__icontains=q)
        )
        return render(request, 'IMS/search.html', {'datas': datas, 'q': q})
    else:
        return render(request, 'IMS/search.html')

@login_required
def data_export(request):
    person_resource = DataResource()
    dataset = person_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}_data.xls"'.format(timezone.now())
    return response

@login_required
def data_import(request):
    if request.method == 'POST':
        person_resource = DataResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())
        result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'IMS/data_list.html')

# RMA시스템 뷰
@login_required()
def delivery_list(request):
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    # 조회
    deliverys = Delivery.objects.order_by('-created_date')
    # 페이징처리
    paginator = Paginator(deliverys, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    return render(request, 'IMS/delivery_list.html', {'deliverys': page_obj})

@login_required()
def delivery_detail(request, pk):
    delivery = get_object_or_404(Delivery, pk=pk)
    return render(request, 'IMS/delivery_detail.html', {'delivery': delivery})

@login_required()
def delivery_new(request):
    if request.method == "POST":
        form = DeliveryForm(request.POST)
        created_date = timezone.now()
        if form.is_valid():
            delivery = form.save(commit=False)
            delivery.creator = request.user
            delivery.created_date = created_date
            delivery.save()
            sendmail(delivery)
            return redirect('delivery_detail', pk=delivery.pk)
    else:
        form = DeliveryForm()
    return render(request, 'IMS/delivery_edit.html', {'form': form})

@login_required()
def delivery_edit(request, pk):
    delivery = get_object_or_404(Delivery, pk=pk)
    if request.method == "POST":
        form = DeliveryForm(request.POST, instance=delivery)
        if form.is_valid():
            delivery = form.save(commit=False)
            delivery.creator = request.user
            delivery.created_date = timezone.now()
            delivery.save()
            return redirect('delivery_detail', pk=delivery.pk)
    else:

        form = DeliveryForm(instance=delivery)
    return render(request, 'IMS/delivery_edit.html', {'form': form})

@login_required
def delivery_search(request):
    deliverys = Delivery.objects.all().order_by('-id')
    q = request.POST.get('q', "")
    if q:
        deliverys = deliverys.filter(
            Q(creator_id__icontains=q) |
            Q(rma_num__icontains=q) |
            Q(serial__icontains=q) |
            Q(vendor__icontains=q) |
            Q(part__icontains=q) |
            Q(status__icontains=q)
        )
        return render(request, 'IMS/delivery_search.html', {'deliverys': deliverys, 'q': q})
    else:
        return render(request, 'IMS/delivery_search.html')