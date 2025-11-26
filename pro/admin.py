from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group
from django import forms
from django.urls import path
from unfold.admin import ModelAdmin
from django.shortcuts import redirect
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, PropertyType, Amenity, Slider, Country, RealEstateCompany ,Agent,Blogs, Testimonial 

admin.site.unregister(Group)
admin.site.site_header = "Property Finder"
admin.site.site_title = "Property Finder Admin"
admin.site.index_title = "Dashboard"


class AdminActionsMixin:
    # Row-level buttons
    def action_buttons(self, obj):
        return format_html(
            '<a class="button" href="/admin/{}/{}/{}/change/">✏️ Edit</a>&nbsp;'
            '<a class="button" href="/admin/{}/{}/{}/delete/">🗑️ Delete</a>',
            obj._meta.app_label, obj._meta.model_name, obj.id,
            obj._meta.app_label, obj._meta.model_name, obj.id,
        )
    action_buttons.short_description = "Actions"

    # Custom URLs
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("import/", self.admin_site.admin_view(self.import_view), name=f"{self.model._meta.model_name}_import"),
            path("export/", self.admin_site.admin_view(self.export_view), name=f"{self.model._meta.model_name}_export"),
        ]
        return custom_urls + urls

    # Import/Export views
    def import_view(self, request):
        return redirect(f"/admin/{self.model._meta.app_label}/{self.model._meta.model_name}/")

    def export_view(self, request):
        return redirect(f"/admin/{self.model._meta.app_label}/{self.model._meta.model_name}/")

    # Override changelist view to inject buttons
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['custom_toolbar_buttons'] = format_html(
            '<a class="button button-info" href="{}">📥 Import</a>&nbsp;'
            '<a class="button button-success" href="{}">📤 Export</a>',
            f'/admin/{self.model._meta.app_label}/{self.model._meta.model_name}/import/',
            f'/admin/{self.model._meta.app_label}/{self.model._meta.model_name}/export/',
        )
        return super().changelist_view(request, extra_context=extra_context)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
@admin.register(Amenity)
class AmenityAdmin(AdminActionsMixin , ModelAdmin):
    list_display = ("id", "name","created_at","action_buttons")
    list_display_links = ("name",)
    search_fields = ("name",)
@admin.register(PropertyType)
class PropertyTypeAdmin(AdminActionsMixin, ModelAdmin):
    list_display = ("id", "name", "looking_to","created_at","action_buttons")
    list_display_links = ("name",)
    list_filter = ("looking_to",)
@admin.register(Slider)
class SliderAdmin(AdminActionsMixin, ModelAdmin):
    list_display = ("title","image", "paragraph", "created_at","action_buttons")
    list_display_links = ("title",)
    search_fields = ("title", "paragraph")
    

@admin.register(RealEstateCompany)
class CompanyAdmin(AdminActionsMixin, ModelAdmin):
    list_display = ("id", "name", "email", "phone", "created_at","action_buttons")
    list_display_links = ("name",)
    search_fields = ("name", "email", "phone")
    list_filter = ("created_at",)


@admin.register(Agent)
class AgentAdmin(AdminActionsMixin, ModelAdmin):
    list_display = ("id", "name", "email", "phone", "created_at","action_buttons")
    list_display_links = ("name",)
    search_fields = ("name", "email", "phone", "license_no")
    list_filter = ("created_at",)
    fieldsets = (
    ("Personal Info", {
        "fields": ("name", "email", "phone", "image", "address")
    }),
    ("Work Info", {
        "fields": ("experience_years", "rating")
    }),
)


    

@admin.register(Blogs)
class BlogAdmin(AdminActionsMixin, ModelAdmin):
    list_display = ("id", "title", "image", "post_by", "created_at","action_buttons")
    list_display_links = ("title",)
    search_fields = ("title", "post_by")
    list_filter = ("created_at",)

@admin.register(Testimonial)
class TestimonialAdmin(AdminActionsMixin, ModelAdmin):
    list_display = ("id", "name",  "address","message", "created_at","action_buttons")
    list_display_links = ("name",)
    search_fields = ("name", "address")
    list_filter = ("created_at",)

@admin.register(Country)
class CountryAdmin(AdminActionsMixin, ModelAdmin):
    list_display = ("name", "created_at", "updated_at", "action_buttons")
    list_display_links = ("name",)
    search_fields = ("name",)
    
# class PaymentPlanInline(admin.TabularInline):
#     model = UserPaymentPlan
#     extra = 1
#     fields = ("payment_name", "payment_amount")
#     show_change_link = True  


# Register Property with inline
# @admin.register(UserProperty)  
# class PropertyAdmin(AdminActionsMixin, ModelAdmin): 
#     search_fields = ("city", "locality", "apartment_name", "user__email") 
#     list_display = ("id", "name", "looking_to", "property_type", "country", "created_at", "updated_at", "action_buttons") 
#     list_display_links = ("name",) 
#     list_filter = ("looking_to", "property_type", "city") 
#     filter_horizontal = ("amenities",) 
#     inlines = [PaymentPlanInline]  
#     fieldsets = ( 
#         ("Step 1: Basic Details", { "fields": ( "name","looking_to", "property_type","company") }), 
#         ("Step 2: Location", { "fields": ("country","city", "locality", "sub_locality", "apartment_name", "house_no") }), 
#         ("Step 3: Property Profile", { "fields": ( "bedrooms", "bathrooms", "balconies", "carpet_area", "builtup_area", "super_builtup_area", "furnishing_status", "expected_price", "all_inclusive", "price_negotiable", "description" ) }), 
#         ("Step 4: Media", { "fields": ("images","images2", "images3", "video", "brochure") }), 
#         ("Step 5: Amenities", { "fields": ("amenities", "parking_spaces", "parking_type", "facing") }), 
     
#     ) 
#     readonly_fields = ("created_at", "updated_at", "price_per_sqft") 


