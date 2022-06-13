from fastapi import FastAPI, Depends, HTTPException
from database import SessionLocal, engine, Base
from pydantic import BaseModel 
from models import Mahasiswa
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

app = FastAPI()

Base.metadata.create_all(bind=engine)

class MahasiswaRequest(BaseModel):
    npm: str
    nama: str

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Read Service
@app.get("/read/{npm}")
def read_service(npm: str, db: Session = Depends(get_db)):
    db_mahasiswa = db.query(Mahasiswa).get(npm)
    if db_mahasiswa:
        return {"status": "OK", "npm": db_mahasiswa.npm, "nama": db_mahasiswa.nama }
    raise HTTPException(status_code=404, detail=f"Mahasiswa dengan npm {npm} tidak ditemukan")

# Update Service
@app.post("/update")
def update_book(mahasiswa: MahasiswaRequest, db: Session = Depends(get_db)):
    db_mahasiswa = db.query(Mahasiswa).get(mahasiswa.npm)
    if db_mahasiswa:
        db_mahasiswa.nama = mahasiswa.nama
        db.commit()
        db.refresh(db_mahasiswa)
        return {"status": "OK" }
    return HTTPException(status_code=404, detail=f"Mahasiswa dengan npm {mahasiswa.npm} tidak ditemukan")

@app.get("/read-all")
def get_books(db: Session = Depends(get_db)):
    return db.query(Mahasiswa).all()

@app.post("/create")
def create_book(mahasiswa: MahasiswaRequest, db: Session = Depends(get_db)):
    try:
        npm = mahasiswa.npm
        nama = mahasiswa.nama
        db_mahasiswa = Mahasiswa(npm=npm, nama=nama)
        db.add(db_mahasiswa)
        db.commit()
        db.refresh(db_mahasiswa)
        return db_mahasiswa
    except IntegrityError:
        return HTTPException(status_code=404, detail=f"Mahasiswa dengan npm {mahasiswa.npm} sudah ada")
