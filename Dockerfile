FROM ubuntu:22.04

# set timezone
ENV TZ=Asia/Kolkata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get -q update
RUN apt-get -qy install tmux nginx curl gunicorn3 git
RUN apt-get install software-properties-common -y
# install python 3.9
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update && apt install -y python3-pip python3.9 python3.9-dev libpq-dev
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 10
RUN apt-get install -y python3.9-distutils
RUN pip3 install --upgrade setuptools && pip3 install --upgrade pip && pip3 install --upgrade distlib

RUN mkdir home/code
RUN mkdir home/data
WORKDIR /home/code

ENV LANG C.UTF-8
ENV LANGUAGE en_US:en
ENV LC_LANG en_US.UTF-8
ENV LC_ALL C.UTF-8
ENV ACCEPT_EULA Y

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


RUN pip3 install uvicorn==0.13.3
RUN pip3 install fastapi==0.63.0
RUN pip3 install https://github.com/aboSamoor/pycld2/zipball/e3ac86ed4d4902e912691c1531d0c5645382a726
RUN apt-get -y install libicu-dev
RUN apt-get -y install pkg-config
RUN pip3 install "uvicorn[standard]" gunicorn
RUN pip3 install PyICU polyglot
RUN pip3 install nltk emoji xformers optimum[onnxruntime]
RUN pip3 install  pyspellchecker
RUN python3 -m spacy download en_core_web_sm
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader wordnet
RUN python3 -m nltk.downloader averaged_perceptron_tagger
RUN cp -r /root/nltk_data /usr/local/share/nltk_data


COPY . .
RUN chmod +x /home/code/auto_run.sh

ENTRYPOINT ["/home/code/auto_run.sh"]
