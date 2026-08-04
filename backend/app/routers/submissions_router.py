import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, auth, sandbox, adaptive, ai_review

router = APIRouter(prefix="/api/submissions", tags=["Submissions"])

@router.post("/submit")
def submit_solution(
    sub_in: schemas.SubmissionCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    question = db.query(models.Question).filter(models.Question.id == sub_in.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    test_cases = json.loads(question.test_cases) if question.test_cases else []
    
    # 1. Execute Submission in Sandbox
    exec_result = sandbox.execute_submission(
        language=sub_in.language,
        code=sub_in.code,
        test_cases=test_cases
    )

    passed_all = exec_result["passed_all"]
    passed_count = exec_result["passed_count"]
    total_tests = exec_result["total_tests"]
    avg_runtime_ms = exec_result["avg_runtime_ms"]

    # 2. Update Adaptive Topic Score via EMA
    updated_score = adaptive.update_user_topic_score(
        db=db,
        user_id=current_user.id,
        topic=question.topic,
        passed_all=passed_all,
        passed_count=passed_count,
        total_tests=total_tests,
        avg_runtime_ms=avg_runtime_ms
    )

    # Compile errors for AI prompt context if any
    errors_list = [r["error"] for r in exec_result["results"] if r.get("error")]
    error_summary = "; ".join(errors_list[:2]) if errors_list else ""

    # 3. LangChain AI Code Review
    ai_feedback = ai_review.analyze_code_with_langchain(
        title=question.title,
        description=question.description,
        language=sub_in.language,
        code=sub_in.code,
        passed_all=passed_all,
        passed_count=passed_count,
        total_tests=total_tests,
        runtime_ms=avg_runtime_ms,
        errors=error_summary
    )

    # 4. Record Submission in DB
    submission_record = models.Submission(
        user_id=current_user.id,
        question_id=question.id,
        language=sub_in.language,
        code=sub_in.code,
        passed=passed_all,
        passed_count=passed_count,
        total_tests=total_tests,
        runtime_ms=avg_runtime_ms,
        ai_feedback=json.dumps(ai_feedback)
    )
    db.add(submission_record)
    db.commit()
    db.refresh(submission_record)

    return {
        "submission_id": submission_record.id,
        "question_id": question.id,
        "question_title": question.title,
        "language": sub_in.language,
        "execution": exec_result,
        "updated_topic_score": {
            "topic": question.topic,
            "new_score": updated_score
        },
        "ai_feedback": ai_feedback,
        "created_at": submission_record.created_at
    }

@router.get("/history", response_model=List[schemas.SubmissionResponse])
def get_submission_history(
    limit: int = 20,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    submissions = db.query(models.Submission).filter(
        models.Submission.user_id == current_user.id
    ).order_by(models.Submission.created_at.desc()).limit(limit).all()

    formatted = []
    for s in submissions:
        feedback_obj = json.loads(s.ai_feedback) if s.ai_feedback else None
        formatted.append({
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
    return formatted
