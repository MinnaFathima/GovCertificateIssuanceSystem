
from fastapi import FastAPI, Depends, HTTPException, Header
# from database import certificate_requests, registrars, birth_collection
from database import (
    birth_collection,
    marriage_collection,
    residential_collection,
    death_collection,
    certificate_requests,
    registrars
)

from schemas import *
from auth import *
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from pdf_generator import generate_certificate_pdf
from fastapi.responses import FileResponse
import os
from datetime import datetime

app = FastAPI()

# Allow CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Utility function for MongoDB document conversion
def convert_mongo_document(doc):
    doc['_id'] = str(doc['_id'])
    if 'assignedRegistrarId' in doc and isinstance(doc['assignedRegistrarId'], ObjectId):
        doc['assignedRegistrarId'] = str(doc['assignedRegistrarId'])
    if 'userId' in doc and isinstance(doc['userId'], ObjectId):
        doc['userId'] = str(doc['userId'])
    return doc

### ======================================
### ADMIN FUNCTIONALITY
### ======================================
@app.post("/admin/forward-birth/{certificate_id}")
async def forward_birth_certificate(certificate_id: str):
    doc = await birth_collection.find_one({"_id": ObjectId(certificate_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Birth Certificate not found")

    registrar_doc = {
        "applicationNumber": doc.get("applicationNumber", ""),
        "certificateType": "BIRTH",
        "assignedRegistrarId": ObjectId("68570be6c2f36d714b73b939"),  # 👈 exact ObjectId assigned
        "status": "PENDING_REGISTRAR",
        "firstName": doc.get("firstName", ""),
        "lastName": doc.get("lastName", "")
    }

    await certificate_requests.insert_one(registrar_doc)

    # Optional: mark original document as forwarded
    # await birth_collection.update_one(
    #     {"_id": ObjectId(certificate_id)},
    #     {"$set": {"status": "FORWARDED"}}
    # )

    return {"message": "Successfully forwarded to registrar"}


###====================//////////////////////////====================================================
@app.post("/admin/forward-marriage/{certificate_id}")
async def forward_marriage_certificate(certificate_id: str):
    doc = await marriage_collection.find_one({"_id": ObjectId(certificate_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Marriage Certificate not found")

    registrar_doc = {
        "certificateType": "MARRIAGE",
        "originalCertificateId": str(doc["_id"]),
        "assignedRegistrarId":ObjectId("68581234c2f36d714b73b940"),
        "status": "PENDING_REGISTRAR",
        "applicationNumber": doc.get("applicationNumber", ""),
        "firstName": doc.get("husbandFirstName", ""),
        "middleName": doc.get("middleName", ""),
        "lastName": doc.get("husbandlastName", ""),
        "createdAt": doc.get("createdAt", datetime.now())
    }

    await certificate_requests.insert_one(registrar_doc)

    # await marriage_collection.update_one(
    #     {"_id": ObjectId(certificate_id)},
    #     {"$set": {"status": "FORWARDED"}}
    # )

    return {"message": "Successfully forwarded to registrar"}
###===============================////////////////////////////=========================================

@app.post("/admin/forward-residential/{certificate_id}")
async def forward_residential_certificate(certificate_id: str):
    doc = await residential_collection.find_one({"_id": ObjectId(certificate_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Residential Certificate not found")

    registrar_doc = {
        "certificateType": "RESIDENTIAL",
        "originalCertificateId": str(doc["_id"]),
        "assignedRegistrarId": ObjectId("68581234c2f36d714b73b941"),
        "status": "PENDING_REGISTRAR",
        "applicationNumber": doc.get("applicationNumber", ""),
        "firstName": doc.get("firstName", ""),
        "middleName": doc.get("middleName", ""),
        "lastName": doc.get("lastName", ""),
        "createdAt": doc.get("createdAt", datetime.now())
    }

    await certificate_requests.insert_one(registrar_doc)

    # await residential_collection.update_one(
    #     {"_id": ObjectId(certificate_id)},
    #     {"$set": {"status": "FORWARDED"}}
    # )

    return {"message": "Successfully forwarded to registrar"}
###============================================///////////////////////////////////==================================

@app.post("/admin/forward-death/{certificate_id}")
async def forward_death_certificate(certificate_id: str):
    doc = await death_collection.find_one({"_id": ObjectId(certificate_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Death Certificate not found")

    registrar_doc = {
        "certificateType": "DEATH",
        "originalCertificateId": str(doc["_id"]),
        "assignedRegistrarId": ObjectId("68581234c2f36d714b73b942"),
        "status": "PENDING_REGISTRAR",
        "applicationNumber": doc.get("applicationNumber", ""),
        "firstName": doc.get("firstName", ""),
        "middleName": doc.get("middleName", ""),
        "lastName": doc.get("lastName", ""),
        "createdAt": doc.get("createdAt", datetime.now())
    }

    await certificate_requests.insert_one(registrar_doc)

    # await death_collection.update_one(
    #     {"_id": ObjectId(certificate_id)},
    #     {"$set": {"status": "FORWARDED"}}
    # )

    return {"message": "Successfully forwarded to registrar"}




### ======================================
### REGISTRAR FUNCTIONALITY
### ======================================

@app.post("/registrar/login")
async def registrar_login(payload: RegistrarLoginSchema):
    registrar = await registrars.find_one({"username": payload.username})
    if not registrar or not verify_password(payload.password, registrar["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({
        "registrar_id": str(registrar["_id"]),
        "certificateType": registrar["certificateType"]
    })
    return {"access_token": token}


async def get_current_registrar(Authorization: str = Header()):
    token = Authorization.split(" ")[1]
    payload = decode_token(token)
    return payload


@app.get("/registrar/requests")
async def get_registrar_requests(registrar=Depends(get_current_registrar)):
    cert_type = registrar["certificateType"]
    assigned_id = ObjectId(registrar["registrar_id"])

    cursor = certificate_requests.find({
        "certificateType": cert_type,
        "assignedRegistrarId": assigned_id,
        # "status": "PENDING_REGISTRAR"
    })

    results_raw = await cursor.to_list(100)
    results = [convert_mongo_document(doc) for doc in results_raw]
    return results


@app.post("/registrar/request/{request_id}/status")
async def update_request_status(request_id: str, payload: CertificateStatusUpdate, registrar=Depends(get_current_registrar)):
    await certificate_requests.update_one(
        {"_id": ObjectId(request_id)},
        {"$set": {"status": payload.status}}
    )
    return {"success": True}


@app.post("/registrar/request/{request_id}/generate-pdf")
async def generate_pdf(request_id: str, registrar=Depends(get_current_registrar)):
    record = await certificate_requests.find_one({"_id": ObjectId(request_id)})
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    data = {
        "applicationNumber": record.get("applicationNumber", ""),
        "firstName": record.get("firstName", ""),
        "middleName": record.get("middleName", ""),
        "lastName": record.get("lastName", ""),
        "certificateType": record.get("certificateType", ""),
        "status": record.get("status", ""),
        "issuedDate": datetime.now().strftime("%d-%m-%Y")
    }

    output_dir = "generated"
    os.makedirs(output_dir, exist_ok=True)
    output_path = f"{output_dir}/certificate_{request_id}.pdf"

    generate_certificate_pdf("birth", data, output_path)

    return FileResponse(output_path, filename="certificate.pdf", media_type="application/pdf")
