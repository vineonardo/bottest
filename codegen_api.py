from fastapi import APIRouter

router = APIRouter()

@router.post("/generate_code")
async def generate_code():
    return {"status": "Codegen Active"}
