
# from motor.motor_asyncio import AsyncIOMotorClient

# # MongoDB Atlas URI
# MONGO_DETAILS = "mongodb+srv://abhishek123:1234abcd@cluster0.h1gmepf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# client = AsyncIOMotorClient(MONGO_DETAILS)

# # Admin DB (Gov Certify)
# gov_certify_db = client.gov_certify
# gov_certify_birth_collection = gov_certify_db.get_collection("BirthCertificate")

# # Registrar DB
# gov_registrar_db = client.gov_registrar
# certificate_requests = gov_registrar_db.get_collection("CertificateRequests")
# registrars = gov_registrar_db.get_collection("RegistrarAccount")


from motor.motor_asyncio import AsyncIOMotorClient

import os
from dotenv import load_dotenv

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_DETAILS")

client = AsyncIOMotorClient(MONGO_DETAILS)

# Admin DB
gov_certify_db = client.gov_certify

# Registrar DB
gov_registrar_db = client.gov_registrar

# Admin Collections
birth_collection = gov_certify_db.get_collection("BirthCertificate")

# Registrar Collections
certificate_requests = gov_registrar_db.get_collection("CertificateRequests")
registrars = gov_registrar_db.get_collection("RegistrarAccount")





marriage_collection = gov_certify_db.get_collection("MarriageCertificate")
residential_collection = gov_certify_db.get_collection("ResidentialCertificate")
death_collection = gov_certify_db.get_collection("DeathCertificate")
