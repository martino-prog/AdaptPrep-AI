from typing import List, Optional, Any, Dict
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# --- Auth Schemas ---
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username_or_email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# --- Question Schemas ---
class TestCase(BaseModel):
    input: str
    expected: str

class QuestionResponse(BaseModel):
    id: int
    title: str
    description: str
    topic: str
    difficulty: str
    test_cases: List[TestCase]
    starter_code: Dict[str, str]
    created_at: datetime

    class Config:
        from_attributes = True

# --- Submission & Execution Schemas ---
class SubmissionCreate(BaseModel):
    question_id: int
    language: str  # 'python' or 'cpp'
    code: str

class TestCaseResult(BaseModel):
    test_case: int
    passed: bool
    input: str
    expected: str
    actual: str
    execution_time_ms: float
    error: Optional[str] = None

class ExecutionResult(BaseModel):
    passed_all: bool
    passed_count: int
    total_tests: int
    avg_runtime_ms: float
    results: List[TestCaseResult]

# --- AI Feedback Schemas ---
class AIFeedbackSchema(BaseModel):
    bugs: List[str]
    time_complexity: str
    space_complexity: str
    optimization_tips: List[str]
    corrected_snippet: Optional[str] = ""

# --- Submission Response Schema ---
class SubmissionResponse(BaseModel):
    id: int
    question_id: int
    question_title: Optional[str] = None
    language: str
    code: str
    passed: bool
    passed_count: int
    total_tests: int
    runtime_ms: float
    ai_feedback: Optional[AIFeedbackSchema] = None
    created_at: datetime

    class Config:
        from_attributes = True

# --- Topic Score & Analytics Schemas ---
class TopicScoreResponse(BaseModel):
    topic: str
    score: float
    updated_at: datetime

    class Config:
        from_attributes = True

class DashboardData(BaseModel):
    user: UserResponse
    scores: List[TopicScoreResponse]
    recent_submissions: List[SubmissionResponse]
    stats: Dict[str, Any]
