from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'physician',
            'first_name',
            'middle_name',
            'last_name',
            'mobile_number',
            'home_phone_number',
            'email',
            'address_line_1',
            'city',
            'state',
            'zip_code',
            'preferred_contact_method',
            'referring_provider',
            'date_of_birth',
            'sex',
            'insurance_company',
            'insurance_member_id',
            'effective_date_of_insurance',
            'secondary_insurance_company',
            'secondary_insurance_member_id',
            'web_upload_status',
            'medical_record_number',
            'eligibility_status',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={
                    'type': 'text', 
                    'class': 'form-control', 
                    'placeholder': 'yyyy-mm-dd'  # Add placeholder here
                }
            ),
            'effective_date_of_insurance': forms.DateInput(
                attrs={
                    'type': 'text', 
                    'class': 'form-control'
                }
            ),
        }
