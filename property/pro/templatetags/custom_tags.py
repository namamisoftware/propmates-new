from django import template
from pro.models import CommercialProperty, ResidentialProperty  # apne model path ke hisab se

register = template.Library()

@register.filter
def instanceof(obj, class_name):
    if class_name == "CommercialProperty":
        return isinstance(obj, CommercialProperty)
    elif class_name == "ResidentialProperty":
        return isinstance(obj, ResidentialProperty)
    return False  
    