FROM python:3.9-slim

# script uses requests as library
RUN pip install requests

COPY entrypoint.sh /entrypoint.sh
COPY jenkins_build.py /jenkins_build.py

# makes logs appear during run
ENV PYTHONUNBUFFERED="true"

ENTRYPOINT ["/entrypoint.sh"]
