# base
FROM python:3
WORKDIR /usr/src/app

# requirements
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://github.com/JoelInTheory/random_coding_thangs.git@k8_thangs
COPY . .

# RUN
CMD [ "gunicorn", "-b :5000", "yousirs:app" ]

# port
EXPOSE 5000
