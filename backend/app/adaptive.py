from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from .models import Question, TopicScore, Submission

TOPICS = ["arrays", "strings", "dp", "graphs", "trees"]
ALPHA = 0.3  # Exponential Moving Average smoothing factor

def update_user_topic_score(db: Session, user_id: int, topic: str, passed_all: bool, passed_count: int, total_tests: int, avg_runtime_ms: float) -> float:
    """
    Updates user's topic mastery score using Exponential Moving Average (EMA).
    Formula: new_score = old_score + alpha * (result - old_score)
    """
    # Calculate performance result
    if passed_all:
        if avg_runtime_ms <= 200.0:
            result = 1.0  # Perfect pass & optimal runtime
        else:
            result = 0.8  # Pass but slightly slow
    elif total_tests > 0 and (passed_count / total_tests) >= 0.5:
        result = 0.4      # Partial pass
    else:
        result = 0.0      # Failure or runtime/compile error

    # Fetch or create topic score
    score_record = db.query(TopicScore).filter(
        TopicScore.user_id == user_id,
        TopicScore.topic == topic.lower()
    ).first()

    if not score_record:
        old_score = 0.5  # Neutral starting score
        score_record = TopicScore(
            user_id=user_id,
            topic=topic.lower(),
            score=old_score
        )
        db.add(score_record)
    else:
        old_score = score_record.score

    # Compute updated EMA score
    new_score = old_score + ALPHA * (result - old_score)
    # Clamp score between 0.0 and 1.0
    new_score = max(0.0, min(1.0, round(new_score, 4)))

    score_record.score = new_score
    db.commit()
    db.refresh(score_record)

    return new_score


def recommend_next_question(db: Session, user_id: int) -> Dict[str, Any]:
    """
    Recommends the next question for the user by:
    1. Finding user's lowest-scoring topic across ["arrays", "strings", "dp", "graphs", "trees"].
    2. Matching target difficulty: < 0.4 => 'easy', 0.4-0.7 => 'medium', > 0.7 => 'hard'.
    3. Selecting an uncompleted (or suitable) question matching topic & difficulty.
    """
    # Ensure all topics have an entry for this user
    existing_scores = db.query(TopicScore).filter(TopicScore.user_id == user_id).all()
    score_map = {s.topic: s.score for s in existing_scores}

    for topic in TOPICS:
        if topic not in score_map:
            new_ts = TopicScore(user_id=user_id, topic=topic, score=0.5)
            db.add(new_ts)
            score_map[topic] = 0.5
    db.commit()

    # Find lowest scoring topic
    lowest_topic = min(score_map, key=score_map.get)
    lowest_score = score_map[lowest_topic]

    # Map score to target difficulty
    if lowest_score < 0.4:
        target_difficulty = "easy"
    elif lowest_score < 0.7:
        target_difficulty = "medium"
    else:
        target_difficulty = "hard"

    # Get IDs of questions already solved by the user with full pass
    solved_q_ids = db.query(Submission.question_id).filter(
        Submission.user_id == user_id,
        Submission.passed == True
    ).distinct().all()
    solved_q_ids = [q[0] for q in solved_q_ids]

    # 1. Try finding an unsolved question in lowest_topic matching target_difficulty
    q = db.query(Question).filter(
        Question.topic == lowest_topic,
        Question.difficulty == target_difficulty,
        Question.id.not_in(solved_q_ids) if solved_q_ids else True
    ).first()

    # 2. If not found, try any unsolved question in lowest_topic
    if not q:
        q = db.query(Question).filter(
            Question.topic == lowest_topic,
            Question.id.not_in(solved_q_ids) if solved_q_ids else True
        ).first()

    # 3. If not found, try any question in lowest_topic matching target_difficulty (allow repeat practice)
    if not q:
        q = db.query(Question).filter(
            Question.topic == lowest_topic,
            Question.difficulty == target_difficulty
        ).first()

    # 4. Fallback to any question in lowest_topic
    if not q:
        q = db.query(Question).filter(
            Question.topic == lowest_topic
        ).first()

    # 5. Ultimate fallback: pick any question in database
    if not q:
        q = db.query(Question).first()

    recommendation_reason = (
        f"Your lowest mastery score is in '{lowest_topic.capitalize()}' ({round(lowest_score * 100)}%). "
        f"We recommended a {target_difficulty.capitalize()} level question to strengthen your skills."
    )

    return {
        "question": q,
        "target_topic": lowest_topic,
        "current_score": lowest_score,
        "recommended_difficulty": target_difficulty,
        "reason": recommendation_reason
    }
