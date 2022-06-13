from sqlalchemy import Column, String

from database import Base

class Mahasiswa(Base):
    __tablename__ = "mahasiswa"

    npm = Column(String, primary_key=True)
    nama = Column(String, nullable=False)