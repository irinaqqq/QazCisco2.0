from django import forms
from .models import *

from django import forms
from .models import *
from django.core.validators import RegexValidator

class DeviceForm(forms.ModelForm):
    DEVICE_TYPES = (
        ('router', 'Router'),
        ('switch', 'Switch'),
        ('pc', 'PC'),
    )
    
    device_type = forms.ChoiceField(choices=DEVICE_TYPES)

    class Meta:
        model = Device
        fields = ['name', 'ip_address', 'network', 'device_type']
        labels = {
            'name': 'Құрылғы атауы',
            'ip_address': 'IP мекенжайы',
            'network': 'Желі',
            'device_type': 'Құрылғы түрі',
        }
    ip_address = forms.CharField(validators=[RegexValidator(
        regex=r'^(\d{1,3}\.){3}\d{1,3}$',  # Regex pattern for IP address
        message='Invalid IP address format. Enter a valid IP address in the format X.X.X.X',
        code='invalid_ip_address'
    )])   
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['network'].empty_label = 'Желіні таңдаңыз'


class InterfaceForm(forms.ModelForm):
    class Meta:
        model = Interface
        fields = ['name', 'ip_address']
        labels = {
            'name': 'Интерфейс атауы',
            'ip_address': 'IP мекенжайы'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ip_address'].required = False


        
class NetworkForm(forms.ModelForm):
    class Meta:
        model = Network
        fields = ['name']
        labels = {
            'name': 'Атауы',
        }       
        widgets = {
            'name': forms.TextInput(attrs={'size': 30, 'class': 'form-control input-padding'}),
        }

from django import forms
from .models import Connection, Device, Interface

class DeviceSelectForm(forms.Form):
    device1 = forms.ModelChoiceField(queryset=Device.objects.all())
    device2 = forms.ModelChoiceField(queryset=Device.objects.all())




class ConnectionForm(forms.ModelForm):
    class Meta:
        model = Connection
        fields = ['interface1', 'interface2']

    def __init__(self, device1, device2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['interface1'].queryset = Interface.objects.filter(device=device1)
        self.fields['interface2'].queryset = Interface.objects.filter(device=device2)
        self.fields['interface1'].widget.attrs['class'] = 'form-control'
        self.fields['interface2'].widget.attrs['class'] = 'form-control'
        
class PingForm(forms.Form):
    device1 = forms.ModelChoiceField(queryset=Device.objects.all(), label='Құрылғы 1')
    device2 = forms.ModelChoiceField(queryset=Device.objects.all(), label='Құрылғы 2')



