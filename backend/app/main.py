from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import Base, engine, get_db

# Create tables on startup if they do not exist.
# (For real production we would use migrations e.g. Alembic — noted for later.)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Portfolio Backend", version="1.0.0")

# Allow the frontend (served from a different origin) to call this API.
# In production we tighten allow_origins to the real domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    """Liveness/readiness probe target for Kubernetes."""
    return {"status": "ok"}


@app.post("/api/contact", response_model=schemas.ContactResponse, status_code=201)
def create_contact(payload: schemas.ContactCreate, db: Session = Depends(get_db)):
    """Save a contact-form submission to Postgres."""
    msg = models.ContactMessage(
        name=payload.name,
        email=payload.email,
        message=payload.message,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


@app.post("/api/visits", response_model=schemas.VisitResponse)
def increment_visits(db: Session = Depends(get_db)):
    """Increment and return the visit counter."""
    counter = db.execute(select(models.VisitCounter).limit(1)).scalar_one_or_none()
    if counter is None:
        counter = models.VisitCounter(count=0)
        db.add(counter)
    counter.count += 1
    db.commit()
    db.refresh(counter)
    return {"count": counter.count}


@app.get("/api/visits", response_model=schemas.VisitResponse)
def get_visits(db: Session = Depends(get_db)):
    """Return the current visit count without incrementing."""
    counter = db.execute(select(models.VisitCounter).limit(1)).scalar_one_or_none()
    return {"count": counter.count if counter else 0}
