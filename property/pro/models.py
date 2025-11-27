from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from smart_selects.db_fields import ChainedForeignKey
from django.utils import timezone

# ----------------- Custom User -----------------
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)   # 🔑 Password hashing
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class RoleModel(models.Model):
    
    role = models.CharField(max_length=20, default="agent")    
    
    def __str__(self):
        return self.role    
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    Country = models.CharField(max_length=255, blank=True, null=True)   
    state = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    locality = models.CharField(max_length=150, null=True, blank=True)  
    pincode = models.CharField(max_length=255, blank=True, null=True)    
    
    
    role = models.ForeignKey(  
        RoleModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )      
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'     # login field
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email


# ----------------- Property Type -----------------
class PropertyType(models.Model):
    LOOKING_TO_CHOICES = (
        (1, "Buy"),
        (2, "Rent"),
        (3, "Commercial Rent"),
        (4, "Commercial Buy"),
        (5, "New Project"),
    )

    looking_to = models.IntegerField(choices=LOOKING_TO_CHOICES)
    name = models.CharField(max_length=100)
    plot = models.IntegerField(default=0)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_looking_to_display()})"
        


# ----------------- Amenity -----------------
class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Amenity"
        verbose_name_plural = "Amenities"

    def __str__(self):
        return self.name


# ----------------- Country + Location-----------------

# ===============================
# COUNTRY MODEL
# ===============================
class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    currency = models.CharField(max_length=20, blank=True, null=True) 
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name
from django.utils import timezone  

# ===============================
# CITY MODEL
# ===============================
class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('country', 'name')
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return f"{self.name}, {self.country.name}"


# ===============================
# LOCATION MODEL
# ===============================
class Location(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="locations")
    name = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('city', 'name')
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        return f"{self.name}, {self.city.name}"


# ===============================
# LOCAL AREA MODEL
# ===============================     
class Local(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="locals")
    name = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('location', 'name')
        verbose_name = "Local Area"
        verbose_name_plural = "Local Areas"

    def __str__(self):
        return f"{self.name}, {self.location.name}"  
    
    
    


# ----------------- Slider -----------------
class Slider(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="sliders/")
    paragraph = models.TextField(help_text="Max 30 words")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ----------------- Blogs -----------------
class Blogs(models.Model):
    meta_title = models.CharField(max_length=255)
    meta_description = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="blog/", null=True, blank=True)
    post_by = models.CharField(max_length=150, blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
    def __str__(self):
        return self.title


# ----------------- Testimonial -----------------
class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="testimonial/", null=True, blank=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name   # 🔥 Fixed (was self.title before)


# ----------------- Real Estate Company -----------------
class RealEstateCompany(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to="company/", null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    registration_number = models.CharField(max_length=100, default=0)
    address = models.TextField(blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0, help_text="No. of years of experience")
    about = models.TextField(blank=True, null=True)
    
     # --- NEW FIELDS (added according to SQL table) ---
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    website = models.URLField(max_length=512, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    state = models.CharField(max_length=128, null=True, blank=True)
    country = models.CharField(max_length=64, default="India")
    pincode = models.CharField(max_length=20, null=True, blank=True)
    verified = models.BooleanField(default=False)

    # Timestamps   
    
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Real Estate Company"
        verbose_name_plural = "Real Estate Companies"

    def __str__(self):
        return self.name

# ----------------- Real Estate User -----------------
class regesteruser(models.Model):     
    # 🔹 Basic Details
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True, unique=True)
    password = models.CharField(max_length=100, blank=True)

    # 🔹 Address Information
    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=100, blank=True)
    
       
    
    # 🔹 Provider Details
    provider = models.CharField(max_length=100, blank=True)
    provider_id = models.IntegerField(blank=True, null=True)

    # 🔹 Status and Limits
    status = models.CharField(
        max_length=20,
        choices=[
            ("Active", "Active"),
            ("Inactive", "Inactive"),
            ("Pending", "Pending"),
        ],
        default="Pending"
    )  
    property_limit = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)

    # 🔹 Image
    image = models.ImageField(upload_to="user_images/", null=True, blank=True)

    # 🔹 Company Details
    company = models.ForeignKey(
        RealEstateCompany,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="agents",
         
    )    
    

    # 🔹 Other Info
    assign_id = models.IntegerField(default=0)
    user_type = models.IntegerField(default=0)

    # 🔹 Timestamps
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Registered User"
        verbose_name_plural = "Registered Users"

    def __str__(self):
        return self.name



# ----------------- Agent -----------------

class Agent(models.Model):
    
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="agent_profile",
        null=True,
        blank=True
    )  
    
       
    # Basic Info
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="agents/", null=True, blank=True)
    
    cv = models.FileField(upload_to="user_cvs/", null=True, blank=True)       

    # Professional Details
    experience_years = models.PositiveIntegerField(default=0)
    closed_deals = models.PositiveIntegerField(
        default=0,
        help_text="Total closed deals"
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0,
        help_text="Rating out of 5"
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ("Active", "Active"),
            ("Inactive", "Inactive"),
            ("Pending", "Pending"),
        ],
        default="Pending"
    )
    
     # Manager — One Manager can have many Agents
    manager = models.ForeignKey(
        "CustomUser",      
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="agents_under_me"
    )  
    
    # Preffered Role    
    Role = models.CharField(max_length=50, blank=True, null=True)                             
    # Self Location Info
    country = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    pincode = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True, null=True)
    
    # Pick Location. He want to join in that location ---------
    Pcountry = models.CharField(max_length=255, blank=True)
    Pstate = models.CharField(max_length=255, blank=True)
    Pcity = models.CharField(max_length=255, blank=True)
    Plocality = models.CharField(max_length=150, null=True, blank=True)      
    Ppincode = models.CharField(max_length=255, blank=True)
    Paddress = models.TextField(blank=True, null=True)         
    
    # Permissions / Role Management
    is_subadmin = models.IntegerField(default=0)
    manage_user = models.IntegerField(default=0)
    manage_user_property = models.IntegerField(default=0)
    manage_company = models.IntegerField(default=0)
    manage_property = models.IntegerField(default=0)

    # Meta Info
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Our Team"
        verbose_name_plural = "Our Team"

    def __str__(self):
        return f"{self.name} - {self.email}"  


class Leadquery(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
   

    class Meta:
        verbose_name = "Contact Query"
        verbose_name_plural = "Contact Queries"

    def __str__(self):
        return f"{self.name} - {self.email}"
    
class Contactquery(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
   

    class Meta:
        verbose_name = "Contact Query"
        verbose_name_plural = "Contact Queries"

    def __str__(self):
        return f"{self.name} - {self.email}"

from django.db import models


# ----------------- Main Property -----------------
class Property(models.Model):  
    LOOKING_TO_CHOICES = (
        (1, "Buy"),
        (2, "Rent"),
        (3, "Commercial Rent"),    
        (4, "Commercial Buy"),
        (5, "New Project"),
    )

    user = models.IntegerField(default=0)
    name = models.CharField(max_length=255, blank=True, null=True)
    looking_to = models.IntegerField(choices=LOOKING_TO_CHOICES)

    # Location
    city = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    sub_locality = models.CharField(max_length=100, blank=True, null=True)
    apartment_name = models.CharField(max_length=150, blank=True, null=True)
    house_no = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    # Financial / Lease
    currency = models.CharField(max_length=10, blank=True, null=True)
    lease = models.CharField(max_length=20, default=0, null=True)
    possession = models.CharField(max_length=20, default=0, null=True)
    possession_date = models.CharField(max_length=20, default=0, null=True)
    available = models.CharField(max_length=20, default=0, null=True)
    available_date = models.CharField(max_length=20, default=0, null=True)
    
    loan = models.CharField(max_length=20, default=0, null=True)
    # Property Details
    age = models.CharField(max_length=20, default=0, null=True)
    flooring = models.CharField(max_length=20, default=0, null=True)
    floor_no = models.CharField(max_length=20, default=0, null=True)
    total_floors = models.CharField(max_length=20, default=0, null=True)
    lift = models.CharField(max_length=20, default=0, null=True)
    office_type = models.CharField(max_length=20, default=0, null=True)
    bedrooms = models.IntegerField(default=0, null=True)
    bathrooms = models.IntegerField(default=0, null=True)
    balconies = models.IntegerField(default=0, null=True)

    # Area
    area_unit = models.CharField(max_length=20, default=0)
    carpet_area = models.FloatField(help_text="Area in sq.ft", null=True)
    ploat_area = models.FloatField(help_text="Area in sq.ft", default=0, null=True)
    ploat_no = models.IntegerField(default=0, null=True)
    builtup_area = models.FloatField(blank=True, null=True)
    super_builtup_area = models.FloatField(blank=True, null=True)
    furnishing_status = models.CharField(max_length=20, null=True)

    # Pricing
    expected_price = models.FloatField(blank=True, null=True)
    rent_type = models.CharField(max_length=20, default=0, null=True)
    rent_price = models.FloatField(blank=True, null=True)
    maintenance_price = models.FloatField(blank=True, null=True)
    price_per_sqft = models.FloatField(blank=True, null=True)
    all_inclusive = models.BooleanField(default=False, null=True)
    price_negotiable = models.BooleanField(default=True, null=True)

    # Media / Description
    description = models.TextField(blank=True, null=True)
    brochure = models.FileField(upload_to="pdfs/", blank=True, null=True)
    image2 = models.FileField(upload_to="property_images/", blank=True, null=True)
    image3 = models.FileField(upload_to="property_images/", blank=True, null=True)
    video = models.FileField(upload_to="videos/", blank=True, null=True)

    # Parking / Facing
    parking_spaces = models.IntegerField(default=0, null=True)
    parking_type = models.CharField(max_length=50, blank=True, null=True)
    facing = models.CharField(max_length=20, blank=True, null=True)

    # Meta
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)


# ----------------- User Property -----------------
class UserProperty(models.Model):
    LOOKING_TO_CHOICES = (  
        (1, "Buy"),
        (2, "Rent"),
        (3, "Commercial Rent"),  
        (4, "Commercial Buy"),
        (5, "New Project"),
    )

    # Relations
    # user = models.ForeignKey(
    #     "regesteruser",
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name="user_properties",
    # )
    company = models.ForeignKey(
        "RealEstateCompany",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="properties",
    )
    # agent = models.ForeignKey(
    #     "Agent",
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name="properties",
    # )     
    property_type = models.ForeignKey(
        "PropertyType",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="properties",
    )
    country = models.ForeignKey(
        "Country",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="properties",
    )

    # Basic Info
    name = models.CharField(max_length=255, blank=True, null=True)
    looking_to = models.IntegerField(choices=LOOKING_TO_CHOICES)
    city = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    sub_locality = models.CharField(max_length=100, blank=True, null=True)
    apartment_name = models.CharField(max_length=150, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    # Financial / Lease
    currency = models.CharField(max_length=10, blank=True, null=True)
    lease = models.CharField(max_length=20, default=0, null=True)
    possession = models.CharField(max_length=20, default=0, null=True)
    possession_date = models.CharField(max_length=20, default=0, null=True)
    available = models.CharField(max_length=20, default=0, null=True)
    available_date = models.CharField(max_length=20, default=0, null=True)
    
    loan = models.CharField(max_length=20, default=0, null=True)  
    # Property Details
    age = models.CharField(max_length=20, default=0, null=True)
    flooring = models.CharField(max_length=20, default=0, null=True)
    floor_no = models.CharField(max_length=20, default=0, null=True)
    total_floors = models.CharField(max_length=20, default=0, null=True)
    lift = models.CharField(max_length=20, default=0, null=True)
    office_type = models.CharField(max_length=20, default=0, null=True)
    bedrooms = models.IntegerField(default=0, null=True)
    bathrooms = models.IntegerField(default=0, null=True)
    balconies = models.IntegerField(default=0, null=True)

    # Area
    area_unit = models.CharField(max_length=20, default=0)
    carpet_area = models.FloatField(help_text="Area in sq.ft", null=True)
    ploat_area = models.FloatField(help_text="Area in sq.ft", default=0, null=True)
    ploat_no = models.IntegerField(default=0, null=True)
    builtup_area = models.FloatField(blank=True, null=True)
    super_builtup_area = models.FloatField(blank=True, null=True)
    furnishing_status = models.CharField(max_length=20, null=True)

    # Pricing
    expected_price = models.FloatField(blank=True, null=True)
    rent_type = models.CharField(max_length=20, default=0, null=True)
    rent_price = models.FloatField(blank=True, null=True)
    maintenance_price = models.FloatField(blank=True, null=True)
    price_per_sqft = models.FloatField(blank=True, null=True)
    all_inclusive = models.BooleanField(default=False, null=True)
    price_negotiable = models.BooleanField(default=True, null=True)

    # Media
    description = models.TextField(blank=True, null=True)
    brochure = models.FileField(upload_to="pdfs/", blank=True, null=True)
    image1 = models.FileField(upload_to="property_images/", blank=True, null=True)
    image2 = models.FileField(upload_to="property_images/", blank=True, null=True)
    image3 = models.FileField(upload_to="property_images/", blank=True, null=True)
    video = models.FileField(upload_to="videos/", blank=True, null=True)
    amenities = models.ManyToManyField("Amenity", blank=True, related_name="properties")

    # Parking / Facing
    parking_spaces = models.IntegerField(default=0, null=True)
    parking_type = models.CharField(max_length=50, blank=True, null=True)
    facing = models.CharField(max_length=20, blank=True, null=True)

    # Meta
    created_at = models.DateField(auto_now_add=True)
    expire_at = models.DateField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)


# ----------------- Payment Plan -----------------
class UserPaymentPlan(models.Model):
    property = models.ForeignKey(
        "UserProperty", on_delete=models.CASCADE, related_name="payment_plans"
    )
    payment_name = models.CharField(max_length=255)
    payment_amount = models.IntegerField(default=0)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Payment Plan"
        verbose_name_plural = "Payment Plans"

    def __str__(self):
        return f"{self.payment_name} - {self.payment_amount}"  


# ----------------- Property Images -----------------
class UserPropertyImage(models.Model):
    property = models.ForeignKey(
        "UserProperty", on_delete=models.CASCADE, related_name="images_set"
    )
    image = models.ImageField(upload_to="property_images/")
    created_at = models.DateTimeField(auto_now_add=True)

# ----------------- Payment Plan -----------------


class PaymentPlan(models.Model):
  
    payment_name = models.CharField(max_length=255)  
    payment_amount = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Payment Plan"
        verbose_name_plural = "Payment Plans"  

    def __str__(self):
        return f"{self.payment_name} - {self.payment_amount}"

# class PropertyImage(models.Model):
   
#     image = models.ImageField(upload_to="property_images/")
#     created_at = models.DateTimeField(auto_now_add=True) 
    
    
    
   
   
   
   
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey  
# New user Property Model Table..........

# ------------------ Property Base ------------------
class PropertyBase(models.Model):      

    # ---- CATEGORY OPTIONS ----  
    PROPERTY_CATEGORY = (
        ("residential", "Residential"),
        ("commercial", "Commercial"),
        ("pg", "PG / Shared Accommodation"),
        ("warehouse", "Warehouse"),
        ("agricultural", "Agricultural Land"),
        ("hotel", "Hotel / Serviced"),
        ("land", "Land / Plot"),    
        ("other", "Other"),
    )
    
  

    # ---- RELATION WITH PROPERTY TYPE TABLE ----
    property_type = models.ForeignKey(
        PropertyType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Buy, Rent, Commercial Buy, Commercial Rent, New Project"
    )
    
      # ---- USER WHO POSTED PROPERTY ----   
    user = models.ForeignKey(  
    "regesteruser",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="+",   # <<< FIXED
    )
    
      # ---- Company PROPERTIES----   
    RCompany = models.ForeignKey(  
    "RealEstateCompany",  
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="+",   # <<< FIXED
    )
  
    agent = models.ForeignKey(
    "Agent",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="+",   # <<< FIXED
)

    # ---- COMMON FIELDS ----
    title = models.CharField(max_length=255)
    description = models.TextField()

    category = models.CharField(max_length=50, choices=PROPERTY_CATEGORY)
    subtype = models.CharField(max_length=100)   # Apartment, Office, Shop, Villa, Warehouse, etc.

    # ---- LOCATION ----
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)  
    locality = models.CharField(max_length=150, blank=True, null=True)
    sub_locality = models.CharField(max_length=150, blank=True, null=True)
    map_address = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    # ---- AREA ----
    area_sqft = models.FloatField(blank=True, null=True)
    super_area = models.FloatField(blank=True, null=True)

    furnishing = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=(
            ("furnished", "Furnished"),
            ("semi", "Semi-Furnished"),
            ("unfurnished", "Unfurnished"),
        )
    )

    parking_spaces = models.IntegerField(blank=True, null=True)
    washrooms = models.IntegerField(blank=True, null=True)
    pantry = models.BooleanField(default=False)

    # ---- AMENITIES ----
    amenities = models.ManyToManyField(Amenity, blank=True)

    # ---- PRICING ----
    currency = models.CharField(max_length=10, default="INR")    
    price = models.FloatField()
    price_type = models.CharField(
        max_length=20,
        choices=(("fixed","Fixed"),("negotiable","Negotiable"))
    )


    payment_frequency = models.CharField(
        max_length=20,
       
        choices=(
            ("monthly","Monthly"),
            ("quarterly","Quarterly"),
            ("yearly","Yearly"),
           
        ),
        default="monthly"
    )

    deposit_amount = models.FloatField(blank=True, null=True)
    maintenance_fees = models.FloatField(blank=True, null=True)
    service_charge_included = models.BooleanField(default=False)

    # ---- Additional Info ----
    available_from = models.DateField(blank=True, null=True)
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ("Active", "Active"),
            ("Inactive", "Inactive"),
            ("Pending", "Pending"),
        ],
        default="Pending"
    )    
    property_status = models.CharField(
        max_length=50,
        choices=(
            ("ready","Ready"),
            ("under_construction","Under Construction"),
            ("offplan","Off-plan"),
        ),
        blank=True, null=True,
    )

    ownership_type = models.CharField(
        max_length=20,
        choices=(("freehold","Freehold"),("leasehold","Leasehold")),
        blank=True, null=True,
    )

    featured = models.BooleanField(default=False)

    # ---- TIMESTAMPS ----
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
   
   
   
# ----------------------------------------------------------
# ✅ COMMERCIAL PROPERTY
# ----------------------------------------------------------
class CommercialProperty(PropertyBase):
    """Base commercial model"""
    company = models.ForeignKey(
      RealEstateCompany,
      on_delete=models.SET_NULL,
      null=True,
      blank=True,
      related_name="commercial_properties",
)   
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    balcony = models.CharField(max_length=255, null=True, blank=True)
    view = models.CharField(max_length=255, null=True, blank=True)    
    model_type = models.CharField(max_length=50, default="commercial")
    featured_image = models.ImageField(upload_to="commercial_images/", null=True, blank=True)

# ------------------ OFFICE ------------------
class Office(models.Model):
    property = models.OneToOneField(CommercialProperty, on_delete=models.CASCADE)

    office_type = models.CharField(max_length=50)  # fitted, furnished...
    meeting_room = models.BooleanField(default=False)
    pantry = models.BooleanField(default=False)
    reception_area = models.BooleanField(default=False)
    total_desks = models.IntegerField(blank=True, null=True)
    conference_room = models.BooleanField(default=False)
    ac_system = models.CharField(max_length=50, blank=True, null=True)
    power_backup = models.BooleanField(default=False)
    view = models.CharField(max_length=50, blank=True, null=True)
    floor_number = models.IntegerField(blank=True, null=True)
    total_floors = models.IntegerField(blank=True, null=True)
    toilets_exclusive = models.BooleanField(default=False)
    lift_available = models.BooleanField(default=True)


# ------------------ SHOP / RETAIL ------------------
class Shop(models.Model):
    property = models.OneToOneField(CommercialProperty, on_delete=models.CASCADE)

    shop_type = models.CharField(max_length=50)
    frontage_ft = models.FloatField(blank=True, null=True)
    ceiling_height = models.FloatField(blank=True, null=True)
    power_load_kw = models.FloatField(blank=True, null=True)
    
    water_connection = models.BooleanField(default=False)
    suitable_for = models.CharField(max_length=255, blank=True, null=True)
    loading_dock = models.BooleanField(default=False)
    parking_spaces = models.IntegerField(blank=True, null=True)
    signage_allowed = models.BooleanField(default=True)


# ------------------ SHOWROOM ------------------
class Showroom(models.Model):
    property = models.OneToOneField(CommercialProperty, on_delete=models.CASCADE)

    showroom_type = models.CharField(max_length=100)
    total_area = models.FloatField()
    ceiling_height = models.FloatField(blank=True, null=True)
    glass_front = models.BooleanField(default=False)
    power_load_kw = models.FloatField()
    parking = models.IntegerField(blank=True, null=True)
    suitable_for = models.CharField(max_length=255, blank=True, null=True)
    visibility = models.CharField(max_length=50, blank=True, null=True)
    storage_room = models.BooleanField(default=False)


# ------------------ WAREHOUSE ------------------
class Warehouse(models.Model):
    property = models.OneToOneField(CommercialProperty, on_delete=models.CASCADE)

    builtup_area = models.FloatField()
    ceiling_height = models.FloatField(blank=True, null=True)
    power_load_kw = models.FloatField()
    loading_dock = models.BooleanField(default=False)
    truck_access = models.BooleanField(default=False)
    office_inside = models.BooleanField(default=False)
    mezzanine = models.BooleanField(default=False)
    fire_safety = models.BooleanField(default=False)
    security_cctv = models.BooleanField(default=False)
    road_access = models.CharField(max_length=50)
    parking_spaces = models.IntegerField(blank=True, null=True)
    warehouse_type = models.CharField(max_length=100)


# ------------------ FACTORY ------------------
class Factory(models.Model):
    property = models.OneToOneField(CommercialProperty, on_delete=models.CASCADE)

    factory_type = models.CharField(max_length=100)
    plot_area = models.FloatField()
    builtup_area = models.FloatField()
    ceiling_height = models.FloatField()
    power_load_kw = models.FloatField()
    water_connection = models.BooleanField(default=False)
    loading_dock = models.BooleanField(default=False)
    cranes_equipment = models.BooleanField(default=False)
    fire_safety = models.BooleanField(default=False)
    parking_area = models.IntegerField(blank=True, null=True)
    road_access = models.CharField(max_length=100)
    office_block = models.BooleanField(default=False)


# ------------------ COMMERCIAL LAND ------------------
class CommercialLand(models.Model):
    property = models.OneToOneField(CommercialProperty, on_delete=models.CASCADE)

    land_type = models.CharField(max_length=100)
    plot_area = models.FloatField()
    land_usage = models.CharField(max_length=255)
    ownership_type = models.CharField(max_length=20)
    boundary_wall = models.BooleanField(default=False)
    road_access = models.BooleanField(default=False)
    corner_plot = models.BooleanField(default=False)
    electricity_available = models.BooleanField(default=False)
    water_connection = models.BooleanField(default=False)
    nearby_landmark = models.CharField(max_length=255, blank=True, null=True)
    development_status = models.CharField(max_length=100)


# ----------------------------------------------------------
# ✅ RESIDENTIAL PROPERTY
# ----------------------------------------------------------
class ResidentialProperty(PropertyBase):
    """Base residential model"""   
    company = models.ForeignKey(
     RealEstateCompany,
     on_delete=models.SET_NULL,
     null=True,
     blank=True,  
     related_name="residential_properties",   
)
  
    featured_image = models.ImageField(upload_to="residential_images/", null=True, blank=True)
    model_type = models.CharField(max_length=50, default="residential")  
    bedrooms = models.CharField(max_length=10, blank=True, null=True)
    bathrooms = models.CharField(max_length=10, blank=True, null=True)
    balcony = models.BooleanField(default=False)
    view = models.CharField(max_length=50, blank=True, null=True)


# ------------------ APARTMENT ------------------
class Apartment(models.Model):
    property = models.OneToOneField(ResidentialProperty, on_delete=models.CASCADE)

    apartment_type = models.CharField(max_length=50)  
    floor_number = models.IntegerField(blank=True, null=True)
    total_floors = models.IntegerField(blank=True, null=True)
    built_year = models.IntegerField(blank=True, null=True)
    central_ac = models.BooleanField(default=False)
    maintenance_included = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)
    maids_room = models.BooleanField(default=False)
    study_room = models.BooleanField(default=False)
    appliances_included = models.BooleanField(default=False)


# ------------------ VILLA ------------------
class Villa(models.Model):
    property = models.OneToOneField(ResidentialProperty, on_delete=models.CASCADE)

    villa_type = models.CharField(max_length=50)
    plot_area = models.FloatField(blank=True, null=True)
    floors = models.IntegerField(blank=True, null=True)
    private_garden = models.BooleanField(default=False)
    private_pool = models.BooleanField(default=False)
    maids_room = models.BooleanField(default=False)
    drivers_room = models.BooleanField(default=False)
    storage_room = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)
    covered_parking = models.BooleanField(default=False)


# ------------------ TOWNHOUSE ------------------
class Townhouse(models.Model):
    property = models.OneToOneField(ResidentialProperty, on_delete=models.CASCADE)

    townhouse_type = models.CharField(max_length=50)
    plot_area = models.FloatField(blank=True, null=True)
    private_garden = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)
    maids_room = models.BooleanField(default=False)
    storage_room = models.BooleanField(default=False)
    parking_spaces = models.IntegerField(blank=True, null=True)
    community_view = models.BooleanField(default=False)
    gated_community = models.BooleanField(default=False)


# ------------------ STUDIO ------------------
class Studio(models.Model):
    property = models.OneToOneField(ResidentialProperty, on_delete=models.CASCADE)

    kitchen_type = models.CharField(max_length=50)
    bathroom_type = models.CharField(max_length=50)
    parking = models.BooleanField(default=False)
    maintenance_included = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)


# ------------------ PENTHOUSE ------------------
class Penthouse(models.Model):
    property = models.OneToOneField(ResidentialProperty, on_delete=models.CASCADE)

    floor_level = models.IntegerField()
    floors_inside = models.IntegerField(blank=True, null=True)
    private_pool = models.BooleanField(default=False)
    private_elevator = models.BooleanField(default=False)
    maids_room = models.BooleanField(default=False)
    storage_room = models.BooleanField(default=False)
    terrace = models.BooleanField(default=False)
    view = models.CharField(max_length=50)
    furnishing = models.CharField(max_length=50)


# ------------------ DUPLEX ------------------
class Duplex(models.Model):
    property = models.OneToOneField(ResidentialProperty, on_delete=models.CASCADE)

    levels = models.IntegerField()
    balcony_terrace = models.BooleanField(default=False)
    maids_room = models.BooleanField(default=False)
    furnishing = models.CharField(max_length=50)
    view = models.CharField(max_length=50)
    parking_spaces = models.IntegerField(blank=True, null=True)
    pets_allowed = models.BooleanField(default=False)


# ------------------ COMPOUND ------------------
class Compound(models.Model):
    property = models.OneToOneField(ResidentialProperty, on_delete=models.CASCADE)

    compound_name = models.CharField(max_length=100, blank=True, null=True)
    total_villas = models.IntegerField(blank=True, null=True)
    shared_pool = models.BooleanField(default=False)
    shared_gym = models.BooleanField(default=False)
    security = models.BooleanField(default=False)
    garden_area = models.BooleanField(default=False)
    kids_play_area = models.BooleanField(default=False)
    maintenance_included = models.BooleanField(default=False)


# ------------------ RESIDENTIAL PLOT ------------------
class ResidentialPlot(models.Model):
    property = models.OneToOneField(ResidentialProperty, on_delete=models.CASCADE)

    plot_area = models.FloatField()
    land_use = models.CharField(max_length=255)
    gated_community = models.BooleanField(default=False)
    corner_plot = models.BooleanField(default=False)
    road_access = models.BooleanField(default=False)
    utilities_available = models.BooleanField(default=False)
    development_status = models.CharField(max_length=100)


# Propertys Images And Videos.....................................................
class ImageCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)   

    def __str__(self):
        return self.name  
    
    
    
# ==========================================================================================
    
# R Ant C Images ...................................
    
class ResidentialPropertyImage(models.Model):
    property = models.ForeignKey(
        ResidentialProperty,
        on_delete=models.CASCADE,   
        related_name="media"
    )

    # Normal Image
    image = models.ImageField(
        upload_to="residential/images/",
        null=True,
        blank=True
    )

    exterior_image = models.ImageField(upload_to="residential/exterior/", null=True, blank=True)
    living_room_image = models.ImageField(upload_to="residential/living_room/", null=True, blank=True)
    bedroom_image = models.ImageField(upload_to="residential/bedroom/", null=True, blank=True)
    bathroom_image = models.ImageField(upload_to="residential/bathroom/", null=True, blank=True)
    kitchen_image = models.ImageField(upload_to="residential/kitchen/", null=True, blank=True)

    floor_plan_image = models.ImageField(upload_to="residential/floor_plan/", null=True, blank=True)
    master_plan_image = models.ImageField(upload_to="residential/master_plan/", null=True, blank=True)
    location_map_image = models.ImageField(upload_to="residential/location_map/", null=True, blank=True)

    # 360°    
    image_360 = models.ImageField(  
        upload_to="residential/images/360/",  
        null=True,
        blank=True
    )

    video_url = models.URLField(null=True, blank=True)
    video_file = models.FileField(
        upload_to="residential/videos/",
        null=True,
        blank=True
    )

    is_featured = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Media for {self.property.title}"


class CommercialPropertyImage(models.Model):  
    property = models.ForeignKey(
        CommercialProperty,
        on_delete=models.CASCADE,
        related_name="media"
    )

    # Normal Image
    image = models.ImageField(
        upload_to="commercial/images/",
        null=True,
        blank=True
    )
    
    exterior_image = models.ImageField(upload_to="residential/exterior/", null=True, blank=True)
    living_room_image = models.ImageField(upload_to="residential/living_room/", null=True, blank=True)
    bedroom_image = models.ImageField(upload_to="residential/bedroom/", null=True, blank=True)
    bathroom_image = models.ImageField(upload_to="residential/bathroom/", null=True, blank=True)
    kitchen_image = models.ImageField(upload_to="residential/kitchen/", null=True, blank=True)

    floor_plan_image = models.ImageField(upload_to="residential/floor_plan/", null=True, blank=True)
    master_plan_image = models.ImageField(upload_to="residential/master_plan/", null=True, blank=True)
    location_map_image = models.ImageField(upload_to="residential/location_map/", null=True, blank=True)  

    # 360°
    image_360 = models.ImageField(
        upload_to="commercial/images/360/",
        null=True,
        blank=True
    )

    video_url = models.URLField(null=True, blank=True)
    video_file = models.FileField(
        upload_to="commercial/videos/",
        null=True,
        blank=True
    )

    is_featured = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return f"Media for {self.property.title}"
#==========================================================================================================

class Payment(models.Model):    

    PAYMENT_PURPOSE = (
        ("booking", "Booking Payment"),
        ("rent", "Rent Payment"),
        ("deposit", "Security Deposit"),
        ("installment", "Installment"),
        ("maintenance", "Maintenance Fee"),
        ("service_charge", "Service Charge"),
        ("final_payment", "Final Payment"),
    )

    PAYMENT_METHOD = (
        ("cash", "Cash"),
        ("bank_transfer", "Bank Transfer"),
        ("cheque", "Cheque"),
        ("online", "Online Payment"),
        ("card", "Credit/Debit Card"),
        ("wallet", "Wallet / UPI"),
    )

    # ---- Generic FK to ANY property model ----
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True,   
        blank=True)
    property = GenericForeignKey("content_type", "object_id")

    user = models.ForeignKey(
        "regesteruser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+"
    )

    purpose = models.CharField(max_length=50, choices=PAYMENT_PURPOSE)
    method = models.CharField(max_length=50, choices=PAYMENT_METHOD)

    amount = models.FloatField()
    notes = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=(("pending", "Pending"), ("success", "Success"), ("failed", "Failed")),
        default="pending"
    )

    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    reference_no = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.property} - {self.amount} ({self.purpose})"
    
    
    

# --------------------------------------------
# Holiday Property Model
# --------------------------------------------
     
class HolidayProperty(models.Model):  
    # For Ageb=nt Asign 
    agent = models.ForeignKey(  
    "Agent",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="+",   # <<< FIXED
    )   
    # 🔹 Company Details 
    company = models.ForeignKey(
        RealEstateCompany,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="Holiday_Listing",
         
    ) 
    property_type = models.ForeignKey(
        PropertyType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Buy, Rent, Commercial Buy, Commercial Rent, New Project"
    ) 
    # ----- BASIC DETAILS -----   
    title = models.CharField(max_length=255)
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ("Active", "Active"),
            ("Inactive", "Inactive"),
            ("Pending", "Pending"),
        ],
        default="Pending"
    ) 
    
      # ---- USER WHO POSTED PROPERTY ----
    user = models.ForeignKey(  
    "CustomUser",  
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="+",   # <<< FIXED  
    )  
    
      # ---- Company PROPERTIES----   
    RCompany = models.ForeignKey(  
    "RealEstateCompany",  
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="+",   # <<< FIXED
    )  
      
    Subproperty_type = models.CharField(      
        max_length=50,  
        choices=(
            ("villa", "Villa"),
            ("apartment", "Apartment"),
            ("farmhouse", "Farmhouse"),
            ("studio", "Studio"),
            ("plot", "Plot"),
            ("cottage", "Cottage"),
        ),
        null=True, blank=True  
        
    )
    listing_type = models.CharField(
        max_length=20,
        choices=(("sale", "For Sale"), ("rent", "For Rent"), ("lease", "For Lease"))
    )
    currency = models.CharField(max_length=10, default="INR")
    price = models.FloatField()
    price_type = models.CharField(
        max_length=20,    
        choices=(("fixed","Fixed"),("negotiable","Negotiable"))
    ) 
    
    payment_frequency = models.CharField(
        max_length=20,
       
        choices=(
            ("monthly","Monthly"),
            ("quarterly","Quarterly"),
            ("yearly","Yearly"),
           
        ),
        default="monthly"
    )
    
    category = models.CharField(max_length=50, default="Holiday")    
    available_from = models.DateField(null=True, blank=True)
    available_to = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)  

    # ----- LOCATION -----
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    locality = models.CharField(max_length=150, blank=True, null=True)  
    address = models.TextField()
    landmark = models.CharField(max_length=150, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    # ----- PROPERTY SPECIFICATIONS -----
    bedrooms = models.IntegerField(blank=True, null=True)
    bathrooms = models.IntegerField(blank=True, null=True)
    balconies = models.IntegerField(blank=True, null=True) 
    builtup_area = models.FloatField(blank=True, null=True)
    carpet_area = models.FloatField(blank=True, null=True)
    plot_area = models.FloatField(blank=True, null=True)
    furnishing = models.CharField(
        max_length=20,
        choices=(("fully","Fully Furnished"),("semi","Semi Furnished"),("unfurnished","Unfurnished")),
        blank=True, null=True
    )
    floor_number = models.IntegerField(blank=True, null=True)
    total_floors = models.IntegerField(blank=True, null=True)
    parking_spaces = models.IntegerField(blank=True, null=True)
    facing_direction = models.CharField(
        max_length=20,
        choices=(("east","East"),("west","West"),("north","North"),("south","South")),
        blank=True, null=True
    )
    property_age = models.CharField(
        max_length=20,
        choices=(("new","New"),("5","<5 Years"),("10","5–10 Years"),("old",">10 Years")),
        blank=True, null=True
    )

    # ----- AMENITIES -----
    amenities = models.ManyToManyField("Amenity", blank=True)  

    # ----- NEARBY -----
    beach_distance = models.CharField(max_length=50, blank=True, null=True)
    market_distance = models.CharField(max_length=50, blank=True, null=True)
    restaurant_distance = models.CharField(max_length=50, blank=True, null=True)
    airport_distance = models.CharField(max_length=50, blank=True, null=True)

    # ----- OWNER / AGENT -----
    listed_by = models.CharField(
        max_length=20,
        choices=(("owner","Owner"),("agent","Agent"),("builder","Builder"))
    )
    owner_name = models.CharField(max_length=150)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    profile_photo = models.ImageField(upload_to="holiday_profiles/", blank=True, null=True)

    # ----- SEO -----
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    featured = models.BooleanField(default=False)

    # ----- TIMESTAMPS -----
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class HolidayPropertyImage(models.Model):
    property = models.ForeignKey(
        HolidayProperty,
        on_delete=models.CASCADE,
        related_name="media"
    )

    # Normal Image
    image = models.ImageField(
        upload_to="holiday/images/",
        null=True,
        blank=True
    )
    exterior_image = models.ImageField(upload_to="property_images/exterior/", null=True, blank=True)
    living_room_image = models.ImageField(upload_to="property_images/living_room/", null=True, blank=True)
    bedroom_image = models.ImageField(upload_to="property_images/bedroom/", null=True, blank=True)
    bathroom_image = models.ImageField(upload_to="property_images/bathroom/", null=True, blank=True)
    kitchen_image = models.ImageField(upload_to="property_images/kitchen/", null=True, blank=True) 
    floor_plan_image = models.ImageField(upload_to="property_images/floor_plan/", null=True, blank=True)
    master_plan_image = models.ImageField(upload_to="property_images/master_plan/", null=True, blank=True)
    location_map_image = models.ImageField(upload_to="property_images/location_map/", null=True, blank=True)
    
    # 360° Image
    image_360 = models.ImageField(
        upload_to="holiday/images/360/",
        null=True,
        blank=True
    )

    # Video URL
    video_url = models.URLField(null=True, blank=True)

    # Video File Upload
    video_file = models.FileField(
        upload_to="holiday/videos/",
        null=True,
        blank=True
    )

    is_featured = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Media for {self.property.title}"





# --------------------------------------------
# Agriculture Property Model
# --------------------------------------------
class AgricultureProperty(models.Model):
  # For Ageb=nt Asign 
  agent = models.ForeignKey(
    "Agent",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="+",   # <<< FIXED
    ) 
    # 🔹 Company Details
  company = models.ForeignKey(
        RealEstateCompany,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="Agriculture_Listing",
         
    ) 
  property_type = models.ForeignKey(
        PropertyType,
        on_delete=models.SET_NULL,  
        null=True,
        blank=True,
        default=2,  
  
    )
  
# ---- AMENITIES ----
  
  amenities = models.ManyToManyField(Amenity, blank=True)
  # Status
  status = models.CharField(
        max_length=20,
        choices=[
            ("Active", "Active"),
            ("Inactive", "Inactive"),
            ("Pending", "Pending"),
        ],
        default="Pending"
    ) 
      # ---- USER WHO POSTED PROPERTY ----
  user = models.ForeignKey(  
    "CustomUser",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="+",   # <<< FIXED  
  ) 
  
    # ---- Company PROPERTIES----   
  RCompany = models.ForeignKey(  
    "RealEstateCompany",  
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="+",   # <<< FIXED
    )
  
  payment_frequency = models.CharField(
        max_length=20,
       
        choices=(
            ("monthly","Monthly"),
            ("quarterly","Quarterly"),
            ("yearly","Yearly"),
           
        ),
        default="monthly"
    )
  category = models.CharField(max_length=50, default="Agriculture") 
# Step 1: Property Details
  total_area = models.DecimalField(max_digits=10, decimal_places=2, default=0)
  area_unit = models.CharField(max_length=50, default=0)


  water_source = models.CharField(max_length=100, blank=True, null=True)
  ownership_type = models.CharField(max_length=100, blank=True, null=True)


  soil_type = models.CharField(max_length=100, blank=True, null=True)
  current_use = models.CharField(max_length=150, blank=True, null=True)


  fenced_property = models.BooleanField(default=False)
  road_access = models.BooleanField(default=False)
  electricity_available = models.BooleanField(default=False)
  irrigation_system = models.BooleanField(default=False)

   
  currency = models.CharField(max_length=10, default="INR")
  expected_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

  title = models.CharField(max_length=255, blank=True, null=True)
  description = models.TextField(blank=True, null=True)

   # ----- LOCATION -----
  country = models.CharField(max_length=100)
  state = models.CharField(max_length=100)
  city = models.CharField(max_length=100)
  locality = models.CharField(max_length=150, blank=True, null=True)
  address = models.TextField()
  landmark = models.CharField(max_length=150, blank=True, null=True)
  pincode = models.CharField(max_length=10, blank=True, null=True)      
  latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
  longitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)

  
  
  created_at = models.DateTimeField(auto_now_add=True)


  def __str__(self):  
   return f"Agriculture Property - {self.total_area} {self.area_unit}"


class AgriculturePropertyImage(models.Model):
    
    property = models.ForeignKey(
        AgricultureProperty,
        on_delete=models.CASCADE,
        related_name="media"
    )

    # Normal Image
    image = models.ImageField(
        upload_to="holiday/images/",
        null=True,
        blank=True
    )

    # 360° Image
    image_360 = models.ImageField(
        upload_to="holiday/images/360/",
        null=True,
        blank=True
    )

    # Video URL
    video_url = models.URLField(null=True, blank=True)

    # Video File Upload
    video_file = models.FileField(
        upload_to="holiday/videos/",
        null=True,
        blank=True
    )

    is_featured = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Media for {self.property.title}"




# --------------------------------------------
# PG Property Model
# --------------------------------------------
class PGProperty(models.Model):
 # For Ageb=nt Asign 
 agent = models.ForeignKey(
    "Agent",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="+",   # <<< FIXED
    ) 
 # 🔹 Company Details
 company = models.ForeignKey(
        RealEstateCompany,  
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="PG_Listing",
         
    ) 
 property_type = models.ForeignKey(
        PropertyType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,   
        default=3,  
        help_text="Buy, Rent, Commercial Buy, Commercial Rent, New Project"
    )
 # Status
 status = models.CharField(
        max_length=20,
        choices=[
            ("Active", "Active"),
            ("Inactive", "Inactive"),
            ("Pending", "Pending"),
        ],
        default="Pending"
    )  
 user = models.ForeignKey(
    "CustomUser",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="+",
)    
     
   # ---- Company PROPERTIES----   
 RCompany = models.ForeignKey(  
    "RealEstateCompany",  
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="+",   # <<< FIXED
    )
 
 
 payment_frequency = models.CharField(
        max_length=20,
       
        choices=(
            ("monthly","Monthly"),
            ("quarterly","Quarterly"),
            ("yearly","Yearly"),
           
        ),  
        default="monthly"  
    )
 
 category = models.CharField(max_length=50, default="PG") 
 # ---- AMENITIES ----
 amenities = models.ManyToManyField(Amenity, blank=True)      
    
# Step 1: Property Details
 room_type = models.CharField(max_length=100) # Single / Double / Shared
 furnishing = models.CharField(max_length=100) # Fully / Semi / Unfurnished
 preferred_gender = models.CharField(max_length=20) # Male / Female / Any
 bedrooms = models.IntegerField(blank=True, null=True)
 bathrooms = models.IntegerField(blank=True, null=True)    

 minimum_stay = models.IntegerField() # in months
 total_beds = models.IntegerField(default=1)


 attached_bathroom = models.BooleanField(default=False)
 kitchen_access = models.BooleanField(default=False)
 laundry_access = models.BooleanField(default=False)  

 # Area -------
 total_area = models.DecimalField(max_digits=10, decimal_places=2, default=0)
 area_unit = models.CharField(max_length=50, default=0)
 
 
# Included Utilities
 electricity = models.BooleanField(default=False)
 water = models.BooleanField(default=False)
 wifi = models.BooleanField(default=False)
 cleaning = models.BooleanField(default=False)


 currency = models.CharField(max_length=10, default="INR")
 expected_price = models.DecimalField(max_digits=10, decimal_places=2) # Monthly

 title = models.CharField(max_length=255, blank=True, null=True)    
 description = models.TextField(blank=True, null=True)

 # ----- LOCATION -----
 country = models.CharField(max_length=100)
 state = models.CharField(max_length=100)
 city = models.CharField(max_length=100)
 locality = models.CharField(max_length=150, blank=True, null=True)  
 address = models.TextField()
 landmark = models.CharField(max_length=150, blank=True, null=True)
 pincode = models.CharField(max_length=10, blank=True, null=True)
 latitude = models.FloatField(blank=True, null=True)
 longitude = models.FloatField(blank=True, null=True)
  

 created_at = models.DateTimeField(auto_now_add=True)


 def __str__(self):
   return f"PG Property - {self.room_type} ({self.expected_price} {self.currency})"   


class PGPropertyImage(models.Model):
    property = models.ForeignKey(
        PGProperty,
        on_delete=models.CASCADE,
        related_name="media"
    )

    # Normal Image
    image = models.ImageField(
        upload_to="holiday/images/",
        null=True,
        blank=True
    )
    exterior_image = models.ImageField(upload_to="property_images/exterior/", null=True, blank=True)
    living_room_image = models.ImageField(upload_to="property_images/living_room/", null=True, blank=True)
    bedroom_image = models.ImageField(upload_to="property_images/bedroom/", null=True, blank=True)
    bathroom_image = models.ImageField(upload_to="property_images/bathroom/", null=True, blank=True)
    kitchen_image = models.ImageField(upload_to="property_images/kitchen/", null=True, blank=True) 
    floor_plan_image = models.ImageField(upload_to="property_images/floor_plan/", null=True, blank=True)
    master_plan_image = models.ImageField(upload_to="property_images/master_plan/", null=True, blank=True)
    location_map_image = models.ImageField(upload_to="property_images/location_map/", null=True, blank=True)

    # 360° Image
    image_360 = models.ImageField(
        upload_to="holiday/images/360/",
        null=True,
        blank=True
    )

    # Video URL
    video_url = models.URLField(null=True, blank=True)

    # Video File Upload
    video_file = models.FileField(
        upload_to="holiday/videos/",
        null=True,
        blank=True
    )

    is_featured = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Media for {self.property.title}"




# --------------------------------------------
# Business For Sale Property Model
# -------------------------------------- ------
 
class BusinessForSale(models.Model): 
  # For Ageb=nt Asign 
  agent = models.ForeignKey(
    "Agent",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="+",   # <<< FIXED
    )  
  # 🔹 Company Details
  company = models.ForeignKey(
        RealEstateCompany,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="business_listings",  
         
    )       
  property_type = models.ForeignKey(
        PropertyType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,  
        default=1,  
        help_text="Buy, Rent, Commercial Buy, Commercial Rent, New Project"
    )
  user = models.ForeignKey(  
    "CustomUser",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="+",   # <<< FIXED  
  ) 
  
    # ---- Company PROPERTIES----   
  RCompany = models.ForeignKey(  
    "RealEstateCompany",  
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="+",   # <<< FIXED
    )
 # ---- AMENITIES ----  
  amenities = models.ManyToManyField(Amenity, blank=True) 
  # Status
  status = models.CharField(
        max_length=20,
        choices=[
            ("Active", "Active"),
            ("Inactive", "Inactive"),
            ("Pending", "Pending"),
        ],
        default="Pending"
    ) 
  BUSINESS_TYPES = (
 ("restaurant", "Restaurant / Café"),
 ("shop", "Retail Shop"),
 ("manufacturing", "Manufacturing Unit"),
 ("it_company", "IT Company"),
 ("hotel", "Hotel / Lodge"),
 ("salon", "Salon / Spa"),
 ("gym", "Gym / Fitness"),
 ("other", "Other"),
)

  category = models.CharField(max_length=50, default="Business")    
  title = models.CharField(max_length=255)
  business_type = models.CharField(max_length=50, choices=BUSINESS_TYPES)
  established_year = models.IntegerField(null=True, blank=True)
  bedrooms = models.IntegerField(blank=True, null=True)
  bathrooms = models.IntegerField(blank=True, null=True) 

  asking_price = models.DecimalField(max_digits=12, decimal_places=2)
  price_negotiable = models.BooleanField(default=False)

  currency = models.CharField(max_length=10, default="INR")  
  monthly_revenue = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
  profit_margin = models.CharField(max_length=50, blank=True, null=True)
  number_of_employees = models.IntegerField(null=True, blank=True)


  total_area = models.DecimalField(max_digits=10, decimal_places=2, default=0)  
  ownership_type = models.CharField(max_length=100, null=True, blank=True)


  description = models.TextField()
  facilities_included = models.TextField(null=True, blank=True)  
  reason_for_sale = models.TextField(null=True, blank=True)


# --- Contact Information ---
  contact_person = models.CharField(max_length=200)  
  contact_phone = models.CharField(max_length=20)
  contact_email = models.EmailField()

  # ----- LOCATION -----
  country = models.CharField(max_length=100)
  state = models.CharField(max_length=100)
  city = models.CharField(max_length=100)  
  locality = models.CharField(max_length=150, blank=True, null=True)       
  address = models.TextField()
  landmark = models.CharField(max_length=150, blank=True, null=True)
  pincode = models.CharField(max_length=10, blank=True, null=True)
  latitude = models.FloatField(blank=True, null=True)
  longitude = models.FloatField(blank=True, null=True)
  
  
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


def __str__(self):  
  return self.title


class BusinessForSaleImage(models.Model):
    property = models.ForeignKey(
        BusinessForSale,
        on_delete=models.CASCADE,
        related_name="media"
    )

    # Normal Image
    image = models.ImageField(
        upload_to="holiday/images/",
        null=True,
        blank=True
    )
    exterior_image = models.ImageField(upload_to="property_images/exterior/", null=True, blank=True)
    living_room_image = models.ImageField(upload_to="property_images/living_room/", null=True, blank=True)
    bedroom_image = models.ImageField(upload_to="property_images/bedroom/", null=True, blank=True)
    bathroom_image = models.ImageField(upload_to="property_images/bathroom/", null=True, blank=True)
    kitchen_image = models.ImageField(upload_to="property_images/kitchen/", null=True, blank=True) 
    floor_plan_image = models.ImageField(upload_to="property_images/floor_plan/", null=True, blank=True)
    master_plan_image = models.ImageField(upload_to="property_images/master_plan/", null=True, blank=True)
    location_map_image = models.ImageField(upload_to="property_images/location_map/", null=True, blank=True)

    # 360° Image
    image_360 = models.ImageField(
        upload_to="holiday/images/360/",  
        null=True,  
        blank=True
    )

    # Video URL
    video_url = models.URLField(null=True, blank=True)

    # Video File Upload
    video_file = models.FileField(
        upload_to="holiday/videos/",
        null=True,
        blank=True
    )

    is_featured = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Media for {self.property.title}"              
