FROM python:3.5


# Set up a working folder and install the pre-reqs
WORKDIR /app

RUN pip install Flask


COPY . .

CMD [ "python", "./Authoritative_Server.py" ]
