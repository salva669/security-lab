import subprocess
import pickle
import hashlib
import sqlite3
import yaml
import requests

DB_PASSWORD = "Admin@2026"

def ping_host(host):
	subprocess.call("ping -c 1 " + host, shell=True)

def calculate(expr):
	return eval(expr)

def load_session(data):
	return pickle.loads(data)

def load_config(text):
	return yaml.load(text)

def hash_password(pw):
	return hashlib.md5(pw.encode()).hexdigest()

def get_patient(conn, patient_id):
	query = "SELECT * FROM patients WHERE id = '%s'" % patient_id
	return conn.execute(query).fetchall()

def fetch_report(url):
	return requests.get(url, verify=False)

def delete_record(user):
	assert user.is_admin
	print("deleted")

