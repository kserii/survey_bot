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


class User(TypedDict):
    id: int
    is_admin: bool
    first_name: Optional[str]
    last_name: Optional[str]
    is_bot: Optional[bool]
    language_code: Optional[str]
    username: Optional[str]


class UserAnswers(TypedDict):
    """Ответы пользователя опроса"""
    survey_id: int
    user_id: int
    answers: List[Answer]
    user_info: Optional[List[User]]


class BotOptions(TypedDict):
    name: Literal["options"]
    active_survey: int  # Текущий опрос
