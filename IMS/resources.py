from import_export import resources
from django.utils.translation import ugettext_lazy as _
from .models import Data

class DataResource(resources.ModelResource):
    class Meta:
        model = Data
        fields = ('install_date', 'serial', 'hostname', 'status__status', 'place', 'vendor__vendor', 'location__location', 'part__part', 'description', 'next_serial' )
        labels = {
            'install_date': _('설치일'),
        }
