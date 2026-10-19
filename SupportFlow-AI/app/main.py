from fastapi import FastAPI
from app.database import Base, engine
from app import models  # noqa: F401 - registers SQLAlchemy models
from app.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SupportFlow AI",
    description=(
        "Explainable support ticket classification and response drafting. "
        "Drafts require human approval before being marked READY."
    ),
    version="1.0.0",
)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}


app.include_router(router)
