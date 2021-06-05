# SeleniumBase Docker Image
FROM ubuntu:18.04

#=======================================
# Install Python and Basic Python Tools
#=======================================
RUN apt-get -o Acquire::Check-Valid-Until=false -o Acquire::Check-Date=false update
RUN apt-get install -y python3 python3-pip python3-setuptools python3-dev python-distribute
RUN alias python=python3
RUN echo "alias python=python3" >> ~/.bashrc

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

#=======================
# Update Python Version
#=======================
RUN apt-get update -y
RUN apt-get -qy --no-install-recommends install python3.8
RUN rm /usr/bin/python3
RUN ln -s python3.8 /usr/bin/python3

#=============================================
# Allow Special Characters in Python Programs
#=============================================
RUN export PYTHONIOENCODING=utf8
RUN echo "export PYTHONIOENCODING=utf8" >> ~/.bashrc

#=====================
# Set up SeleniumBase
#=====================
COPY sbase /SeleniumBase/sbase/
COPY seleniumbase /SeleniumBase/seleniumbase/
COPY examples /SeleniumBase/examples/
COPY integrations /SeleniumBase/integrations/
COPY requirements.txt /SeleniumBase/requirements.txt
COPY setup.py /SeleniumBase/setup.py
RUN find . -name '*.pyc' -delete
RUN find . -name __pycache__ -delete
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install --upgrade setuptools-scm
RUN cd /SeleniumBase && ls && pip3 install -r requirements.txt --upgrade
RUN cd /SeleniumBase && python3 setup.py develop
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
