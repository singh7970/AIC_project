from django.shortcuts import render,redirect,HttpResponse
from .forms import PatientForm
# Create your views here.
import datetime


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Patient
from .serializers import PatientSerializer

from django.shortcuts import render
# from .tasks import get_makemytrip_title
from .tasks import selenium_task



@api_view(['GET', 'POST'])
def patient_list(request):
    if request.method == 'GET':
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





def index(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()  # Save the form data and get the saved instance
            # Trigger the Celery task after the form submission
            selenium_task.delay(patient.id)  # Pass the ID of the saved patient
            return HttpResponse("Form submitted! The title will be printed in the worker terminal.")
        else:
            return HttpResponse("Form is not valid. Please try again.")
    else:
        # Render the form page for GET requests
        form = PatientForm()  # Make sure the form is passed for GET requests
        return render(request, 'index.html', {'form': form})


LOG_FILE = "/home/priyanshu/Documents/AIC/app/selenium_task.log"

def log_message(message):
    try:
        with open(LOG_FILE, "a") as log_file:
            log_file.write(f"{datetime.now()} - {message}\n")
    except Exception as e:
        print(f"Logging failed: {e}")
