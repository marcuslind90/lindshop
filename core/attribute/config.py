from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AttributeConfig(AppConfig):
    label = 'attribute'
    name = 'lindshop.core.attribute'
    verbose_name = _('Attribute')
