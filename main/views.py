from django.shortcuts import render, redirect
from .models import Network, Device
from .forms import *
from django.views import View
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
def network_list(request):
    networks = Network.objects.all()
    context = {
        'networks': networks,
    }
    return render(request, 'network_list.html', context)

from django.shortcuts import render
from django.contrib import messages
from .forms import PingForm
from .models import Network, Device, Connection

def network_detail(request, pk):
    network = Network.objects.get(pk=pk)
    devices = network.device_set.all()
    connections = Connection.objects.filter(device1__in=devices).select_related('device1', 'interface1', 'device2', 'interface2')

    # Check device connection status
    for device in devices:
        connected = False
        for connection in connections:
            if connection.device1 == device or connection.device2 == device:
                connected = True
                break
        device.is_connected = connected

    if request.method == 'POST':
        form = PingForm(request.POST)
        if form.is_valid():
            device1 = form.cleaned_data['device1']
            device2 = form.cleaned_data['device2']
            if device1.is_connected_to(device2):
                messages.success(request, f'Пинг сәтті өтті: {device1.name} қосылған {device2.name}')
            else:
                messages.error(request, f'Пингтің бұзылуы: {device1.name} қосылмаған {device2.name}')
    else:
        form = PingForm()

    context = {
        'network': network,
        'devices': devices,
        'connections': connections,
        'ping_form': form,
    }
    return render(request, 'network_detail.html', context)



def device_list(request):
    devices = Device.objects.all()
    return render(request, 'device_list.html', {'devices': devices})

def device_detail(request, pk):
    device = get_object_or_404(Device, pk=pk)
    interfaces = device.interfaces.all()
    connections = device.get_connections()
    if request.method == 'POST':
        interface_form = InterfaceForm(request.POST)
        if interface_form.is_valid():
            interface = interface_form.save(commit=False)
            interface.device = device
            interface.save()
    else:
        interface_form = InterfaceForm()
    
    return render(request, 'device_detail.html', {'device': device, 'interface_form': interface_form, 'connections': connections})

def device_add(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('device_list')
    else:
        form = DeviceForm()

    return render(request, 'device_add.html', {'form': form})

class NetworkCreateView(View):
    def get(self, request):
        form = NetworkForm()
        return render(request, 'network_form.html', {'form': form})

    def post(self, request):
        form = NetworkForm(request.POST)
        if form.is_valid():
            network = form.save()
            return redirect('network_detail', pk=network.pk)
        return render(request, 'network_form.html', {'form': form})
    
    
def connection_create(request, pk):
    devices = Device.objects.all()
    if request.method == 'POST':
        form = DeviceSelectForm(request.POST)
        if form.is_valid():
            device1 = form.cleaned_data['device1']
            device2 = form.cleaned_data['device2']
            if not device1.interface_set.exists() or not device2.interface_set.exists():
                # Вывод сообщения об ошибке, если устройства не имеют интерфейсов
                error_message = "Бір немесе екі құрылғыда интерфейстер жоқ"
                return render(request, 'connection_form.html', {'devices': devices, 'form': form, 'error_message': error_message})
            interface1 = device1.interface_set.first()
            interface2 = device2.interface_set.first()
            if not is_same_network(interface1.ip_address, interface2.ip_address, '255.255.255.0'):
                # Вывод сообщения об ошибке, если устройства находятся в разных подсетях
                error_message = "Құрылғылар бір желіде емес"
                return render(request, 'connection_form.html', {'devices': devices, 'form': form, 'error_message': error_message})
            if device1.network == device2.network:
                return redirect('connection_create2', pk1=device1.pk, pk2=device2.pk)
            else:
                messages.error(request, 'Құрылғылар бір желіде емес')
    else:
        form = DeviceSelectForm()

    return render(request, 'connection_form.html', {'devices': devices, 'form': form})




def connection_create2(request, pk1, pk2):
    device1 = get_object_or_404(Device, pk=pk1)
    device2 = get_object_or_404(Device, pk=pk2)
    interfaces1 = device1.interface_set.all()
    interfaces2 = device2.interface_set.all()

    if request.method == 'POST':
        form = ConnectionForm(device1, device2, request.POST)
        if form.is_valid():
            connection = form.save(commit=False)
            connection.device1 = device1
            connection.device2 = device2
            connection.save()
            return redirect('device_detail', pk=device1.pk)
    else:
        form = ConnectionForm(device1, device2)
    return render(request, 'connection_form2.html', {'form': form, 'interfaces1': interfaces1, 'interfaces2': interfaces2})



def is_same_network(ip_address1, ip_address2, subnet_mask):
    # Преобразование IP-адреса в список чисел
    ip1 = [int(x) for x in ip_address1.split('.')]
    ip2 = [int(x) for x in ip_address2.split('.')]
    subnet = [int(x) for x in subnet_mask.split('.')]

    # Проверка, находятся ли IP-адреса в одной подсети
    for i in range(4):
        if (ip1[i] & subnet[i]) != (ip2[i] & subnet[i]):
            return False
    return True


def device_delete(request, pk, pk2):
    device = get_object_or_404(Device, pk=pk)
    device.delete()
    return redirect('network_detail', pk=device.network.pk)

def connection_delete(request, pk, id):
    connection = get_object_or_404(Connection, pk=id)
    network_pk = connection.device1.network.pk
    connection.delete()
    return redirect('network_detail', pk=network_pk)
