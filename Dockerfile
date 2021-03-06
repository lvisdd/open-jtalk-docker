FROM ubuntu:latest
MAINTAINER k_kanou

# Install build tools
RUN apt-get update && \
    apt-get install -y wget git build-essential unzip

WORKDIR /usr/local/src/

# Install Open JTalk
RUN wget http://downloads.sourceforge.net/hts-engine/hts_engine_API-1.10.tar.gz && \
    tar zxvf hts_engine_API-1.10.tar.gz && \
    cd hts_engine_API-1.10/ && \
    ./configure && \
    make && \
    make install

COPY manobi.patch manobi.patch

RUN wget http://downloads.sourceforge.net/open-jtalk/open_jtalk-1.09.tar.gz && \
    tar zxvf open_jtalk-1.09.tar.gz && \
    cd open_jtalk-1.09/ && \
    patch -p0 < /usr/local/src/manobi.patch && \
    ./configure --with-hts-engine-header-path=/usr/local/include --with-hts-engine-library-path=/usr/local/lib --with-charset=UTF-8 && \
    make && \
    make install

RUN wget http://downloads.sourceforge.net/open-jtalk/hts_voice_nitech_jp_atr503_m001-1.05.tar.gz && \
    tar zxvf hts_voice_nitech_jp_atr503_m001-1.05.tar.gz && \
    cp -r hts_voice_nitech_jp_atr503_m001-1.05 /usr/local/lib/hts_voice_nitech_jp_atr503_m001-1.05

RUN wget http://downloads.sourceforge.net/open-jtalk/open_jtalk_dic_utf_8-1.09.tar.gz && \
    tar zxvf open_jtalk_dic_utf_8-1.09.tar.gz && \
    cp -r open_jtalk_dic_utf_8-1.09 /usr/local/lib/open_jtalk_dic_utf_8-1.09

RUN wget https://sourceforge.net/projects/mmdagent/files/MMDAgent_Example/MMDAgent_Example-1.7/MMDAgent_Example-1.7.zip/download -O MMDAgent_Example-1.7.zip && \
    unzip MMDAgent_Example-1.7.zip MMDAgent_Example-1.7/Voice/* && \
    cp -r MMDAgent_Example-1.7/Voice/mei/ /usr/local/src

# Install python and pip
RUN apt-get install -y python3-pip

# Add our code
ADD ./webapp /opt/webapp/
WORKDIR /opt/webapp

# Install dependencies
ADD ./webapp/requirements.txt /tmp/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -qr /tmp/requirements.txt
# CMD [""]

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku			
CMD gunicorn --bind 0.0.0.0:$PORT wsgi
# CMD gunicorn index:app --bind 0.0.0.0:$PORT --log-file -
