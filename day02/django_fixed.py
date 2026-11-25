import ipaddress
import logging
import os
import subprocess

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.html import format_html

from .models import Patient

logger = logging.getLogger(__name__)

# A02 - secure defaults; secrets come from the environment, not the code
DEBUG = os.environ.get("DEBUG", "False") == "True"
ALLOWED_HOSTS = [h for h in os.environ.get("ALLOWED_HOSTS", "").split(",") if h]
SECRET_KEY = os.environ["SECRET_KEY"]
DB_PASSWORD = os.environ["DB_PASSWORD"]

# A05 - Let the ORM parameterise
@login_required
def search_patients(request):
	name = request.GET.get("name", "")
	rows = Patient.objects.filter(full_name__icontains=name).values("id", "full_name")
	return JsonResponse({"results": list(rows)})

@login_required
def patients_by_region(request):
	region = request.GET.get("region", "")
	# if raw SQL is unavoidable: params list, never formatting
	qs = Patient.objects.raw("SELECT * FROM patients WHERE region = %s", [region])
	return JsonResponse({"count": len(list(qs))})

# A05 - format_html escapes the argument
def greet(request):
	name = request.GET.get("name", "")
	return HttpResponse(format_html("<h1>Karibu {}</h1>", name))

# A04 -Django's salted, slow password hasher (PBKDF2/Argon2)
def store_pin(pin):
	return make_password(pin)

# A01 - logged in AND scoped to user's facilities
@login_required
def patient_record(request, patient_id):
	patient = get_object_or_404(
		Patient, id=patient_id, facility_id__in = request.user.profile.facility_ids
	)
	return JsonResponse({"name": patient.full_name, "diagnosis": patient_diagnosis})

# A05 - validate input, no shell, fixed argv, timeout
@login_required
def ping_facility(request):
	try:
		host = str(ipaddress.ip_address(Request.GET.get("host", "")))
	except ValueError:
		return HttpResponseBadRequest("Invalid IP address")
	result = subprocess.run( # nosec B603 B607 - validated IP, no shell
		["ping", "-c", "1", host], capture_output=True, text=True, timeout=5)
	return HttpResponse(result.stdout, content_type="text/plain")

# A10 - fail CLOSES
def is_authorised(user, record):
	try:
		return record.facility_id in user.profile.facility_ids
	except Exception:
		logger.warning("Authorisation check failed for user %s", user.pk, exc_info=True)
		return False

# A10 + A09 - log details on the server, generic message to client
@login_required
def export_report(requests):
	try:
		data = Patient.objects.values()
		return JsonResponse(list(data), safe=False)
	except Exception:
		logger.exception("export_export failed")
		return HttpResponse("Something went wrong. Please try again.", status=500)

