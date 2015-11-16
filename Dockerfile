# SeleniumBase Docker Image
FROM ubuntu:14.04

# Install Python and Basic Python Tools
RUN apt-get update && apt-get install -y python python-pip python-setuptools python-dev python-distribute

#========================
# Miscellaneous packages
# Includes minimal runtime used for executing selenium with firefox
#========================
ENV BUILD_DEPS '\
    build-essential \
    libmysqlclient-dev \
    libpython-dev \
    libyaml-dev \
    libxml2-dev \
    libxslt1-dev \
    libxslt-dev \
    zlib1g-dev \
  '

RUN apt-get update -qqy \
  && apt-get -qy --no-install-recommends install \
    locales \
    language-pack-en \
    sudo \
    unzip \
    wget \
    curl \
    vim \
    xvfb \
    libaio1 \
    libxml2 \
    libxslt1.1 \
    mysql-client \
    ${BUILD_DEPS} \
  && rm -rf /var/lib/apt/lists/* 

#==============================
# Locale and encoding settings
#==============================
ENV LANGUAGE en_US.UTF-8
ENV LANG ${LANGUAGE}
RUN locale-gen ${LANGUAGE} \
  && dpkg-reconfigure --frontend noninteractive locales 

#====================
# Firefox Latest ESR
#====================
RUN apt-get update -qqy \
  && apt-get -qy --no-install-recommends install \
     $(apt-cache depends firefox | grep Depends | sed "s/.*ends:\ //" | tr '\n' ' ') \
  && rm -rf /var/lib/apt/lists/* \
  && mkdir -p /tmp/ff \
  && wget -P /tmp/ff/ --no-check-certificate -r -l 1 -A bz2 -nH --cut-dirs=8 \
    https://ftp.mozilla.org/pub/mozilla.org/firefox/releases/latest-esr/linux-x86_64/en-US/ \
  && tar -xjf /tmp/ff/firefox-*esr.tar.bz2 -C /opt/ \
  && ln -s /opt/firefox/firefox /usr/bin/firefox \
  && rm -rf /tmp/ff/

#===================
# Timezone settings
#===================
# Full list at http://en.wikipedia.org/wiki/List_of_tz_database_time_zones
#  e.g. "US/Pacific" for Los Angeles, California, USA
ENV TZ "America/New_York"
# Apply TimeZone
RUN echo $TZ | tee /etc/timezone \
  && dpkg-reconfigure --frontend noninteractive tzdata

#========================================
# Add normal user with passwordless sudo
#========================================
RUN sudo useradd seluser --shell /bin/bash --create-home \
  && sudo usermod -a -G sudo seluser \
  && echo 'ALL ALL = (ALL) NOPASSWD: ALL' >> /etc/sudoers

#=====================
# Set up SeleniumBase
#=====================
COPY docker/docker_requirements.txt /SeleniumBase/
COPY docker/docker_setup.py /SeleniumBase/
COPY seleniumbase /SeleniumBase/seleniumbase/
COPY examples /SeleniumBase/examples/
RUN cd /SeleniumBase && ls && sudo pip install -r docker_requirements.txt
RUN cd /SeleniumBase && ls && sudo python docker_setup.py install

#=========================================
# Create entrypoint and grab example test
#=========================================
COPY docker/docker-entrypoint.sh /
COPY docker/docker_test.sh /
COPY docker/docker_config.cfg /SeleniumBase/examples/
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["/bin/bash"]
