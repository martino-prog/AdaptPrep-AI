import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    scores = relationship("TopicScore", back_populates="user", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="user", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    topic = Column(String(50), index=True, nullable=False)  # arrays, strings, dp, graphs, trees
    difficulty = Column(String(20), index=True, nullable=False)  # easy, medium, hard
    test_cases = Column(Text, nullable=False)  # JSON list of {"input": "...", "expected": "..."}
    starter_code = Column(Text, nullable=True)  # JSON dict {"python": "...", "cpp": "..."}
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    submissions = relationship("Submission", back_populates="question", cascade="all, delete-orphan")

class TopicScore(Base):
    __tablename__ = "topic_scores"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic = Column(String(50), nullable=False)
    score = Column(Float, default=0.5, nullable=False)  # 0.0 (weak) to 1.0 (master)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="scores")

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    language = Column(String(20), nullable=False)  # python or cpp
    code = Column(Text, nullable=False)
    passed = Column(Boolean, nullable=False, default=False)
    passed_count = Column(Integer, default=0)
    total_tests = Column(Integer, default=0)
    runtime_ms = Column(Float, default=0.0)
    ai_feedback = Column(Text, nullable=True)  # JSON string of structured AI feedback
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="submissions")
    question = relationship("Question", back_populates="submissions")
