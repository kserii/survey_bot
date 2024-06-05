from datetime import datetime
from typing import TypedDict, Optional, List, Literal


class Question(TypedDict):
    name: str  # Вопрос
    answers: Optional[List[str]]  # Ответы. Если None, значит ответ произвольный.


class Survey(TypedDict):
    id: int
    questions: List[Question]  # Вопросы.
    created_at: datetime


class BotOptions(TypedDict):
    name: Literal["options"]
    active_survey: int  # Текущий опрос


class User(TypedDict):
    id: int
    first_name: str
    is_bot: bool
    language_code: str
    username: Optional[str]
