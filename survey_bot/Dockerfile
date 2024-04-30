FROM jeandormehl/python3.9-bullseye
LABEL authors="Serezhkin Konstantin"

WORKDIR /app/

ENV PYTHONPATH=/app/survey_bot/

COPY ./requirements.txt /app/survey_bot/requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./survey_bot/requirements.txt

COPY . /app/survey_bot/
