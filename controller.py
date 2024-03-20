
import time
import hashlib

def generate_token(serial_number):
	timestamp = str(time.time())  # Current timestamp
	unique_string = f"{serial_number}{timestamp}"
	return hashlib.sha256(serial_number.encode()).hexdigest()
