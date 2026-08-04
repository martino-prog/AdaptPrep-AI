import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, auth, adaptive

router = APIRouter(prefix="/api/questions", tags=["Questions"])

def format_question_dict(q: models.Question) -> dict:
    return {
        "id": q.id,
        "title": q.title,
        "description": q.description,
        "topic": q.topic,
        "difficulty": q.difficulty,
        "test_cases": json.loads(q.test_cases) if q.test_cases else [],
        "starter_code": json.loads(q.starter_code) if q.starter_code else {},
        "created_at": q.created_at
    }

@router.get("", response_model=List[schemas.QuestionResponse])
def get_questions(
    topic: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Question)
    if topic:
        query = query.filter(models.Question.topic == topic.lower())
    if difficulty:
        query = query.filter(models.Question.difficulty == difficulty.lower())
    questions = query.all()
    return [format_question_dict(q) for q in questions]

@router.get("/next-question")
def get_next_question(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    rec = adaptive.recommend_next_question(db, current_user.id)
    if not rec["question"]:
        raise HTTPException(status_code=404, detail="No suitable questions found")
    
    q_dict = format_question_dict(rec["question"])
    return {
        "question": q_dict,
        "target_topic": rec["target_topic"],
        "current_score": rec["current_score"],
        "recommended_difficulty": rec["recommended_difficulty"],
        "reason": rec["reason"]
    }

@router.get("/{question_id}", response_model=schemas.QuestionResponse)
def get_question_by_id(question_id: int, db: Session = Depends(get_db)):
    q = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return format_question_dict(q)
