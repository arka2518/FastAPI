from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open("patients.json", "r") as file:
        data = json.load(file)
        return data

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "A fully functionaly API built to manage patient records"}

@app.get("/view")
def view_patients():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def get_patient(patient_id: str = Path(..., description="The ID of the patient in the DB", example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="Sort on the basis of weight, height or bmi"), order: str = Query("asc", description="Sort in asc or desc order")):
    valid_fields = ["weight", "height", "bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field, select from {valid_fields}")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order, select between asc and desc")

    data = load_data()
    sort_order = True if order == "desc" else False
    sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse = sort_order)
    return sorted_data

@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    data[patient.id] = patient.model_dump(exclude=["id"])
    
    save_data(data)
    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})

@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    existing_patient_data = data[patient_id]
    updated_patient_data = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_data.items():
        existing_patient_data[key] = value

    existing_patient_data["id"] = patient_id
    patient_pydantic = Patient(**existing_patient_data)
    
    existing_patient_data = patient_pydantic.model_dump(exclude="id")
    data[patient_id] = existing_patient_data

    save_data(data)
    return JSONResponse(status_code=200, content={"message": "Patient data updated successfully"})
