import json
from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

TOPICS = ["arrays", "strings", "dp", "graphs", "trees"]

@router.get("/scores", response_model=List[schemas.TopicScoreResponse])
def get_user_scores(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    scores = db.query(models.TopicScore).filter(models.TopicScore.user_id == current_user.id).all()
    score_map = {s.topic: s for s in scores}

    # Ensure all topics are present
    results = []
    for topic in TOPICS:
        if topic in score_map:
            results.append(score_map[topic])
        else:
            new_ts = models.TopicScore(user_id=current_user.id, topic=topic, score=0.5)
            db.add(new_ts)
            db.commit()
            db.refresh(new_ts)
            results.append(new_ts)
    return results

@router.get("/dashboard")
def get_dashboard_data(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Topic Scores
    scores = get_user_scores(current_user=current_user, db=db)
    
    # 2. Recent Submissions
    submissions = db.query(models.Submission).filter(
        models.Submission.user_id == current_user.id
    ).order_by(models.Submission.created_at.desc()).limit(10).all()

    formatted_submissions = []
    for s in submissions:
        feedback_obj = json.loads(s.ai_feedback) if s.ai_feedback else None
        formatted_submissions.append({
            "id": s.id,
            "question_id": s.question_id,
            "question_title": s.question.title if s.question else f"Question #{s.question_id}",
            "language": s.language,
            "code": s.code,
            "passed": s.passed,
            "passed_count": s.passed_count,
            "total_tests": s.total_tests,
            "runtime_ms": s.runtime_ms,
            "ai_feedback": feedback_obj,
            "created_at": s.created_at
        })

    # 3. Aggregated Stats
    total_submissions = db.query(models.Submission).filter(models.Submission.user_id == current_user.id).count()
    passed_submissions = db.query(models.Submission).filter(
        models.Submission.user_id == current_user.id,
        models.Submission.passed == True
    ).count()

    solved_question_ids = db.query(models.Submission.question_id).filter(
        models.Submission.user_id == current_user.id,
        models.Submission.passed == True
    ).distinct().count()

    total_questions = db.query(models.Question).count()
    
    avg_score = sum([s.score for s in scores]) / len(scores) if scores else 0.5

    stats = {
        "total_submissions": total_submissions,
        "passed_submissions": passed_submissions,
        "solved_questions_count": solved_question_ids,
        "total_questions_count": total_questions,
        "overall_mastery": round(avg_score * 100, 1),
        "pass_rate": round((passed_submissions / total_submissions * 100), 1) if total_submissions > 0 else 0.0
    }

    return {
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "created_at": current_user.created_at
        },
        "scores": [{"topic": s.topic, "score": s.score, "updated_at": s.updated_at} for s in scores],
        "recent_submissions": formatted_submissions,
        "stats": stats
    }
