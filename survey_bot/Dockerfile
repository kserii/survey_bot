FROM python3.9-bullseye
LABEL authors="Serezhkin Konstantin"

WORKDIR /app/survey_bot/

ENV PYTHONPATH=/app/survey_bot/

COPY ./requirements.txt /app/survey_bot/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app/survey_bot/

CMD ["uvicorn", "vk2tg.main:app", "--host", "0.0.0.0", "--port", "80"]
