FROM python:3.7-alpine
WORKDIR /bot

# install system dependencies
RUN apk add --no-cache gcc musl-dev linux-headers mariadb-dev python3-dev

# copy requirements.txt & install them
COPY PrincessPaperplane/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# start bot
CMD ["python", "PrincessPaperplane/paperbot.py", "-test"]