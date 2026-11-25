import hashlib
import subprocess

from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.utils.safestring import mark_safe

from .models import Patient

# A02 Security Misconfiguration
DEBUG = True
ALLOWED_HOSTS = ["*"]

# A04 / secrets in code
SECRET_KEY = "django-insecure-afyalink-1234"
DB_PASSWORD = "Admin@2026"

# A05 Injection - SQL via f-string
def search_patients(request):
	name = request.GET.get("name", "")
	with connection.cursor() as cursor:
		cursor.execute(f"SELECT id, full_name FROM patients WHERE full_name LIKE '%{name}%'")
		rows = cursor.fetchall()
	return JsonResponse({"results": rows})

# A05 Injection -raw ORM with % formatting
def patients_by_region(requests):
	region = request.GET.get("region")
	qs = Patient.objects.raw("SELECT * FROM patients WHERE region = '%s'" % region)
	return JsonResponse({"count": len(list(qs))})

# A05 Injection - XSS
def greet(request):
	name = request.GET.get("name", "")
	return HttpResponse(mark_safe(f"<h1>Karibu {name}</h1>"))

# A04 Cryptographic Failures
def store_pin(pin):
	return hashlib.md5(pin.encode()).hexdigest()

# A01 Broken Access Control - IDOR, no login check
def patient_record(request, patient_id):
	patient = Patient.objects.get(id=patient_id)
	return JsonResponse({"name": patient.full_name, "diagnosis": patient.diagnosis})

# A05 Injection - OS Command
def ping_facility(request):
	host = request.GET.get("host")
	output = subprocess.check_output(f"ping -c 1 {host}", shell=True)
	return HttpResponse(output)

# A10 Mishandling Exceptional Conditions - fails OPEN
def is_authorised(user, record):
	try:
		return record.facility_id in user.profile.facility_ids
	except Exception:
		return True

# A10 - leaks internals to the client
def export_report(request):
	try:
		data = Patient.objects.values()
		return JsonResponse(list(data), safe=False)
	except Exception as e:
		return HttpResponse(f"Error: {e}", status=500)

