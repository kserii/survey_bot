FROM 1222333444/node20
LABEL authors="Serezhkin Konstantin"

WORKDIR /app/survey_web/

COPY package.json package-lock.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "app.js"]

