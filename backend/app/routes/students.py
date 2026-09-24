from fastapi import APIRouter

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/")
def get_students():
    return [{"id": 1, "name": "Student A"}]

@router.post("/")
def create_student():
    return {"status": "created"}

@router.put("/{student_id}")
def update_student(student_id: int):
    return {"status": "updated", "id": student_id}

@router.delete("/{student_id}")
def delete_student(student_id: int):
    return {"status": "deleted", "id": student_id}
