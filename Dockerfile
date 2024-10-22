FROM python:3.12

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .
RUN find . -name "*.db" -delete
RUN find . -name "*.yaml" -delete

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# tell the port number the container should expose
EXPOSE 5000

# run the command
# CMD gunicorn -b 0.0.0.0:5000 app:app
CMD python3 app.py
