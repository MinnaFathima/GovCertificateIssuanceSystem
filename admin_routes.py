# admin_routes.py

from fastapi import APIRouter
from database import birth_collection, registrar_requests_collection
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/admin/forward-birth/{certificate_id}")
async def forward_birth_certificate(certificate_id: str):
    original_doc = await birth_collection.find_one({"_id": ObjectId(certificate_id)})
    if not original_doc:
        return {"error": "Document not found"}

    registrar_doc = {
        "certificateType": "APB",
        "originalCertificateId": str(original_doc["_id"]),
        "registrarId": "Registrar1",  # you can make this dynamic later
        "forwardedByAdminAt": datetime.utcnow(),
        "status": "PENDING",
        "certificateData": original_doc
    }

    await registrar_requests_collection.insert_one(registrar_doc)

    await birth_collection.update_one(
        {"_id": ObjectId(certificate_id)},
        {"$set": {"status": "FORWARDED"}}
    )

    return {"message": "Successfully forwarded"}
