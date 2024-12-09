from django.db import models

class Patient(models.Model):   
    CONTACT_METHOD_CHOICES = [
        ('Email', 'Email'),
        ('Phone', 'Phone'),
        ('Mail', 'Mail'),
    ]
    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('Need to Upload', 'Need to Upload'),
        ('Uploaded', 'Uploaded'),
    ]

    physician = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    home_phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    address_line_1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    preferred_contact_method = models.CharField(max_length=20, choices=CONTACT_METHOD_CHOICES)
    referring_provider = models.CharField(max_length=100)
    date_of_birth = models.DateField()      
    sex = models.CharField(max_length=20, choices=SEX_CHOICES)
    insurance_company = models.CharField(max_length=200)
    insurance_member_id = models.CharField(max_length=200)
    effective_date_of_insurance = models.DateField(blank=True)
    secondary_insurance_company = models.CharField(max_length=200, blank=True)
    secondary_insurance_member_id = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    web_upload_status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Need to Upload')
    medical_record_number = models.CharField(max_length=20, blank=True)
    eligibility_status = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"