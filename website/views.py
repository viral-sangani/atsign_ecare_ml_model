import json
import uuid
from datetime import datetime, timedelta

from constants import Constants
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import medicines, report_data


# Create your views here.
def reportPage(request, id):

    if id == None or id == "":
        return render(request, "404.html")

    jsonDec = json.decoder.JSONDecoder()
    reportObj = report_data.objects.get(uuid=id)

    medicinesListObj = medicines.objects.filter(report__uuid=id)
    future = reportObj.createdAt + timedelta(minutes=15)
    if timezone.now() > future:
        return render(request, "expire.html")
    testsList = []
    medicinesList = []

    if reportObj.tests != "":
        testsList = jsonDec.decode(reportObj.tests)
    for item in medicinesListObj:
        medicinesList.append(
            {
                "name": item.name,
                "time": item.time,
                "interval": item.interval,
            }
        )
    context = {
        "hospital_name": reportObj.hospital_name,
        "doctor_name": reportObj.doctor_name,
        "doctor_degree": reportObj.doctor_degree,
        "doctor_address": reportObj.doctor_address,
        "doctor_number": reportObj.doctor_number,
        "doctor_email": reportObj.doctor_email,
        "patient_name": reportObj.patient_name,
        "patient_age": reportObj.patient_age,
        "patient_gender": reportObj.patient_gender,
        "date": reportObj.date,
        "content": reportObj.content.splitlines(),
        "tests": testsList,
        "medicines": medicinesList,
    }

    return render(request, "reports.html", context)


@api_view(["POST"])
def generatePage(request):
    if request.method == "POST":
        try:
            uuidStr = str(uuid.uuid4())
            hospital_name = request.data["doctor"]["hospital_name"]
            doctor_name = request.data["doctor"]["doctor_name"]
            doctor_degree = request.data["doctor"]["doctor_degree"]
            doctor_address = request.data["doctor"]["doctor_address"]
            doctor_number = request.data["doctor"]["doctor_number"]
            doctor_email = request.data["doctor"]["doctor_email"]
            patient_name = request.data["patient"]["patient_name"]
            patient_age = request.data["patient"]["patient_age"]
            patient_gender = request.data["patient"]["patient_gender"]
            date = request.data["date"]
            content = request.data["content"]
            tests = json.dumps(request.data["tests"])
            obj = report_data.objects.create(
                uuid=uuidStr,
                hospital_name=hospital_name,
                doctor_name=doctor_name,
                doctor_degree=doctor_degree,
                doctor_address=doctor_address,
                doctor_number=doctor_number,
                doctor_email=doctor_email,
                patient_name=patient_name,
                patient_age=patient_age,
                patient_gender=patient_gender,
                date=date,
                content=content,
                tests=tests,
            )
            for item in request.data["medicines"]:
                medicines.objects.create(
                    report=obj,
                    name=item["name"],
                    time=item["time"],
                    interval=item["interval"],
                )
            return Response(
                {"url": Constants.URL + "reports/" + uuidStr}, status=status.HTTP_200_OK
            )
        except:
            return Response(
                {"error": "missing fields"}, status=status.HTTP_400_BAD_REQUEST
            )
