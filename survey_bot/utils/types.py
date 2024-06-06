from datetime import datetime
from typing import TypedDict, Optional, List, Literal


class Question(TypedDict):
    question_name: str  # Вопрос
    question_options: Optional[List[str]]  # Ответы. Если None, значит ответ произвольный.


class Survey(TypedDict):
    id: int
    questions: List[Question]  # Вопросы.
    created_at: datetime


class Answer(TypedDict):
    """Вопрос и ответ на него"""
    question: str
    answer: str


class UserAnswers(TypedDict):
    """Ответы пользователя опроса"""
    survey_id: int
    user_id: int
    answers: List[Answer]


class BotOptions(TypedDict):
    name: Literal["options"]
    active_survey: int  # Текущий опрос


class User(TypedDict):
    id: int
    first_name: str
    is_bot: bool
    language_code: str
    username: Optional[str]