FROM tensorflow/tensorflow

ADD setup.py .

RUN python setup.py

ADD . .

RUN pip install --ignore-installed Flask pillow

CMD [ "python", "-m", "flask", "-A", "main", "run", "-h", "0.0.0.0" ]