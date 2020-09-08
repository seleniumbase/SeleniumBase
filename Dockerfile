# SeleniumBase Docker Image
FROM ubuntu:18.04

#=======================================
# Install Python and Basic Python Tools
#=======================================
RUN apt-get update && apt-get install -y python python-pip python-setuptools python-dev python-distribute
# Above command on Windows
#RUN apt-get -o Acquire::Check-Valid-Until=false -o Acquire::Check-Date=false update
#RUN apt-get install -y python python-pip python-setuptools python-dev python-distribute

#=================================
# Install Bash Command Line Tools
#=================================
RUN apt-get -qy --no-install-recommends install \
    sudo \
    unzip \
    wget \
    curl \
    libxi6 \
    libgconf-2-4 \
    vim \
    xvfb \
  && rm -rf /var/lib/apt/lists/*

#================
# Install Chrome
#================
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get -yqq update && \
    apt-get -yqq install google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

#==================
# Configure Chrome
#==================
RUN dpkg-divert --add --rename --divert /opt/google/chrome/google-chrome.real /opt/google/chrome/google-chrome && \
    echo "#!/bin/bash\nexec /opt/google/chrome/google-chrome.real --disable-setuid-sandbox --no-sandbox \"\$@\"" > /opt/google/chrome/google-chrome && \
    chmod 755 /opt/google/chrome/google-chrome

#=================
# Install Firefox
#=================
RUN apt-get -qy --no-install-recommends install \
     $(apt-cache depends firefox | grep Depends | sed "s/.*ends:\ //" | tr '\n' ' ') \
  && rm -rf /var/lib/apt/lists/* \
  && cd /tmp \
  && wget --no-check-certificate -O firefox-esr.tar.bz2 \
    'https://download.mozilla.org/?product=firefox-esr-latest&os=linux64&lang=en-US' \
  && tar -xjf firefox-esr.tar.bz2 -C /opt/ \
  && ln -s /opt/firefox/firefox /usr/bin/firefox \
  && rm -f /tmp/firefox-esr.tar.bz2

#===========================
# Configure Virtual Display
#===========================
RUN set -e
RUN echo "Starting X virtual framebuffer (Xvfb) in background..."
RUN Xvfb -ac :99 -screen 0 1280x1024x16 > /dev/null 2>&1 &
RUN export DISPLAY=:99
RUN exec "$@"

#=====================
# Set up SeleniumBase
#=====================
COPY seleniumbase /SeleniumBase/seleniumbase/
COPY examples /SeleniumBase/examples/
COPY integrations /SeleniumBase/integrations/
COPY requirements.txt /SeleniumBase/requirements.txt
COPY setup.py /SeleniumBase/setup.py
RUN find -name '*.pyc' -delete
RUN find -name __pycache__ -delete
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install --upgrade setuptools-scm
RUN cd /SeleniumBase && ls && pip install -r requirements.txt --upgrade
RUN cd /SeleniumBase && python setup.py develop
RUN seleniumbase install chromedriver
RUN seleniumbase install geckodriver

#==========================================
# Create entrypoint and grab example tests
#==========================================
COPY integrations/docker/docker-entrypoint.sh /
COPY integrations/docker/run_docker_test_in_firefox.sh /
COPY integrations/docker/run_docker_test_in_chrome.sh /
RUN chmod +x *.sh
COPY integrations/docker/docker_config.cfg /SeleniumBase/examples/
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["/bin/bash"]
