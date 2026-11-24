import os
import json
import ast
import subprocess
import hashlib
import yaml
import requests

DB_PASSWORD = os.environ.get("DB_PASSWORD")

def ping_host(host):
	subprocess.run(["ping", "-c", "1", host], check=True)

def calculate(expr):
	return ast.literal_eval(expr)

def load_session(data):
	return json.loads(data)

def load_config(text):
	return yaml.safe_load(text)

def hash_password(pw, salt):
	return hashlib.pbkdf2_hmac("sha256", pw.encode(), salt, 600_000.hex()

def get_patient(conn, patient_id):
	return conn.execute("SELECT * FROM patients WHERE id = ?", (patient_id,)).fetchall()

def fetch_report(url):
	return requests.get(url, timeout=10)

def delete_record(user):
	if not user.is_admin:
		raise PermissionError("admin only")
	print("deleted")

