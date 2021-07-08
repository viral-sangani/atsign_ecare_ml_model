from django.db import models

# Create your models here.


class report_data(models.Model):
    uuid = models.CharField(max_length=100, null=False, blank=False)
    hospital_name = models.CharField(max_length=100, null=False, blank=False)
    doctor_name = models.CharField(max_length=100, null=False, blank=False)
    doctor_degree = models.CharField(max_length=100, null=False, blank=False)
    doctor_address = models.CharField(max_length=200, null=False, blank=False)
    doctor_number = models.CharField(max_length=20, null=False, blank=False)
    doctor_email = models.CharField(max_length=30, null=False, blank=False)
    patient_name = models.CharField(max_length=60, null=False, blank=False)
    patient_age = models.CharField(max_length=5, null=False, blank=False)
    patient_gender = models.CharField(max_length=10, null=False, blank=False)
    date = models.CharField(max_length=20, null=False, blank=False)
    content = models.TextField(blank=True, default="NA")
    tests = models.TextField(blank=True, default="")
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "report_data"

    def __str__(self):
        return self.patient_name


class medicines(models.Model):
    report = models.ForeignKey(report_data, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False)
    time = models.CharField(max_length=100, null=False, blank=False)
    interval = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.report.patient_name
