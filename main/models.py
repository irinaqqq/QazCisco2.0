from django.db import models
from django.db.models import Q
class Network(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Interface(models.Model):
    name = models.CharField(max_length=50)
    device = models.ForeignKey('Device', on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=15)
    
    
class Device(models.Model):
    DEVICE_TYPES = (
        ('router', 'Router'),
        ('switch', 'Switch'),
        ('pc', 'PC'),
    )

    name = models.CharField(max_length=50)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=15, default='')
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPES, default='router')
    interfaces = models.ManyToManyField(Interface, related_name='devices', blank=True)

    def __str__(self):
        return self.name
    def get_connections(self):
        return Connection.objects.filter(Q(device1=self) | Q(device2=self))
    def is_connected_to(self, other_device, checked_devices=None):
        if checked_devices is None:
            checked_devices = set()
        checked_devices.add(self)

        connections = Connection.objects.filter(Q(device1=self, device2=other_device) | Q(device1=other_device, device2=self))
        if connections.exists():
            return True

        for connection in self.connections1.all():
            if connection.device2 not in checked_devices:
                if connection.device2.is_connected_to(other_device, checked_devices):
                    return True

        for connection in self.connections2.all():
            if connection.device1 not in checked_devices:
                if connection.device1.is_connected_to(other_device, checked_devices):
                    return True

        return False



class Connection(models.Model):
    device1 = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='connections1', default=1, null=True)
    interface1 = models.ForeignKey(Interface, on_delete=models.CASCADE, related_name='connections1')
    device2 = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='connections2', default=1, null=True)
    interface2 = models.ForeignKey(Interface, on_delete=models.CASCADE, related_name='connections2')

    class Meta:
        unique_together = ('device1', 'interface1', 'device2', 'interface2')
