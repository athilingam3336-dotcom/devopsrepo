from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import os

# Database setup

DATABASE_URL = os.getenv(
"DATABASE_URL",
"postgresql://devuser:devpass@localhost:5432/devdb"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
autocommit=False,
autoflush=False,
bind=engine
)
Base = declarative_base()

class DataEntry(Base):
**tablename** = "data_entries"

```
id = Column(Integer, primary_key=True, index=True)
name = Column(String, nullable=False)
message = Column(String, nullable=False)
created_at = Column(DateTime, default=datetime.utcnow)
```

Base.metadata.create_all(bind=engine)

class DataIn(BaseModel):
name: str
message: str

class DataOut(BaseModel):
id: int
name: str
message: str
created_at: datetime

```
class Config:
    from_attributes = True
```

app = FastAPI(
title="DevOps Demo API",
version="1.0.0"
)

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_methods=["*"],
allow_headers=["*"],
)

def get_db():
db = SessionLocal()
try:
yield db
finally:
db.close()

@app.get("/")
def root():
return {
"message": "DevOps Demo API is running",
"version": "1.0.0"
}

@app.get("/health")
def health(db: Session = Depends(get_db)):
try:
db.execute(text("SELECT 1"))
db_status = "connected"
except Exception as e:
db_status = f"error: {str(e)}"

```
return {
    "status": "healthy",
    "database": db_status,
    "timestamp": datetime.utcnow().isoformat(),
}
```

@app.post("/data", response_model=DataOut, status_code=201)
def create_entry(
payload: DataIn,
db: Session = Depends(get_db)
):
entry = DataEntry(
name=payload.name,
message=payload.message
)

```
db.add(entry)
db.commit()
db.refresh(entry)

return entry
```

@app.get("/data", response_model=list[DataOut])
def list_entries(
db: Session = Depends(get_db)
):
return (
db.query(DataEntry)
.order_by(DataEntry.created_at.desc())
.all()
)
