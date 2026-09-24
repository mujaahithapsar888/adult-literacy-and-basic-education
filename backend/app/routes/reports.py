from fastapi import APIRouter

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/")
def get_reports():
    return {"report_url": "http://localhost/reports/123.pdf"}
