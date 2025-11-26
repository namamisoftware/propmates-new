from django import forms
from .models import regesteruser

  



from django.contrib.contenttypes.forms import BaseGenericInlineFormSet
from django.contrib.contenttypes.models import ContentType
from .models import (
    CommercialProperty, ResidentialProperty,
    Office, Shop, Showroom, Warehouse, Factory, CommercialLand,
    Apartment, Villa, Townhouse, Studio, Penthouse, Duplex, Compound, ResidentialPlot,
    PropertyImage, ImageCategory, Payment
)

class AgentForm(forms.ModelForm):
    class Meta:
        model = regesteruser  
        fields = '__all__' 
        



from django import forms   
from .models import (
    CommercialProperty, ResidentialProperty, PropertyBase, 
    Office, Shop, Showroom, Warehouse, Factory, CommercialLand,
    Apartment, Villa, Townhouse, Studio, Penthouse, Duplex, Compound, ResidentialPlot
)


# ============================================================
# ✅ BASE FORM PART 1 (Basic Details)
# ============================================================
class BaseFormPart1(forms.ModelForm):  

    subtype = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True
    )

    class Meta:
        model = CommercialProperty
        fields = [
            "title",
            "description",
            "property_type",
            "subtype",
            "price",
            "price_type",
        ]

    def __init__(self, *args, **kwargs):
        category = kwargs.pop("category", None)   # ✅ GET category HERE
        super().__init__(*args, **kwargs)

        # ✅ Commercial Subtypes
        commercial_choices = [
            ("office", "Office"),
            ("shop", "Shop"),
            ("showroom", "Showroom"),
            ("warehouse", "Warehouse"),
            ("factory", "Factory"),
            ("land", "Commercial Land"),
        ]

        # ✅ Residential Subtypes
        residential_choices = [
            ("apartment", "Apartment"),
            ("villa", "Villa"),
            ("townhouse", "Townhouse"),
            ("studio", "Studio"),
            ("penthouse", "Penthouse"),
            ("duplex", "Duplex"),
            ("compound", "Compound"),
            ("plot", "Residential Plot"),
        ]

        # ✅ Assign based on category
        if category == "commercial":
            self.fields["subtype"].choices = commercial_choices
        else:
            self.fields["subtype"].choices = residential_choices

# class BaseFormPart1(forms.ModelForm):
#     class Meta:    
#         model = PropertyBase   # ← ABSTRACT MODEL (will be replaced dynamically)
#         fields = [
#             "title",
#             "description",
#             "property_type",
#             "subtype",
#             "price",
#             "price_type",
#         ]

#         widgets = {
#             "title": forms.TextInput(attrs={"class": "form-control"}),
#             "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
#             "property_type": forms.Select(attrs={"class": "form-control"}),
#             "subtype": forms.TextInput(attrs={
#                 "class": "form-control",
#                 "placeholder": "e.g. office / shop / apartment"
#             }),
#             "price": forms.NumberInput(attrs={"class": "form-control"}),
#             "price_type": forms.Select(attrs={"class": "form-control"}),
#         }


# ============================================================
# ✅ BASE FORM PART 2 (Location, Area, Additional Info)
# ============================================================
from django import forms
from .models import PropertyBase  # Make sure this is your abstract/base model

class BaseFormPart2(forms.ModelForm):
    class Meta:
        model = PropertyBase  # Abstract model
        fields = [
            "country", "city", "locality", "sub_locality",  
            "map_address", "latitude", "longitude",
            "area_sqft", "super_area",
            "furnishing", "parking_spaces", "washrooms",
            "payment_frequency", "deposit_amount",
            "maintenance_fees", "service_charge_included",  
            "available_from", "property_status", "ownership_type"  
        ]

        widgets = { 
            "country": forms.TextInput(attrs={"class": "form-control", "id": "countryInput"}),
            "city": forms.TextInput(attrs={"class": "form-control", "id": "cityInput"}),
            "locality": forms.TextInput(attrs={"class": "form-control", "id": "locality"}),
            "sub_locality": forms.TextInput(attrs={"class": "form-control", "id": "subLocality"}),

            "map_address": forms.TextInput(attrs={"class": "form-control", "id": "selectedAddress"}),
            "latitude": forms.NumberInput(attrs={"class": "form-control", "id": "latitude"}),
            "longitude": forms.NumberInput(attrs={"class": "form-control", "id": "longitude"}),

            "area_sqft": forms.NumberInput(attrs={"class": "form-control"}),
            "super_area": forms.NumberInput(attrs={"class": "form-control"}),

            "furnishing": forms.Select(attrs={"class": "form-control"}),
            "parking_spaces": forms.NumberInput(attrs={"class": "form-control"}),
            "washrooms": forms.NumberInput(attrs={"class": "form-control"}),

            "payment_frequency": forms.Select(attrs={"class": "form-control"}),
            "deposit_amount": forms.NumberInput(attrs={"class": "form-control"}),
            "maintenance_fees": forms.NumberInput(attrs={"class": "form-control"}),
            "service_charge_included": forms.NumberInput(attrs={"class": "form-control"}),

            "available_from": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "property_status": forms.Select(attrs={"class": "form-control"}),
            "ownership_type": forms.Select(attrs={"class": "form-control"}),
        }
# ==========================================
# ✅ COMMERCIAL SUBTYPE FORMS
# ============================================================

class OfficeForm(forms.ModelForm):
    class Meta:
        model = Office
        exclude = ["property"]
        widgets = {field: forms.TextInput(attrs={"class": "form-control"}) for field in model._meta.fields if field.name != "property"}


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        exclude = ["property"]


class ShowroomForm(forms.ModelForm):
    class Meta:
        model = Showroom
        exclude = ["property"]


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        exclude = ["property"]


class FactoryForm(forms.ModelForm):
    class Meta:
        model = Factory
        exclude = ["property"]


class CommercialLandForm(forms.ModelForm):
    class Meta:
        model = CommercialLand
        exclude = ["property"]


# ============================================================
# ✅ RESIDENTIAL SUBTYPE FORMS
# ============================================================

class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        exclude = ["property"]  


class VillaForm(forms.ModelForm):
    class Meta:
        model = Villa
        exclude = ["property"]


class TownhouseForm(forms.ModelForm):
    class Meta:
        model = Townhouse
        exclude = ["property"]


class StudioForm(forms.ModelForm):
    class Meta:
        model = Studio
        exclude = ["property"]


class PenthouseForm(forms.ModelForm):
    class Meta:
        model = Penthouse
        exclude = ["property"]


class DuplexForm(forms.ModelForm):
    class Meta:
        model = Duplex
        exclude = ["property"]


class CompoundForm(forms.ModelForm):
    class Meta:
        model = Compound
        exclude = ["property"]


class ResidentialPlotForm(forms.ModelForm):
    class Meta:
        model = ResidentialPlot
        exclude = ["property"]
