# SeleniumBase Docker Image
FROM ubuntu:22.04

#============================
# Install Linux Dependencies
#============================
RUN apt-get update && apt-get install -y \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    libu2f-udev \
    libvulkan1 \
    xdg-utils

#=================================
# Install Bash Command Line Tools
#=================================
RUN apt-get -qy --no-install-recommends install \
    curl \
    sudo \
    unzip \
    vim \
    wget \
    xvfb \
  && rm -rf /var/lib/apt/lists/*

#================
# Install Chrome
#================
RUN curl -LO  https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
RUN rm google-chrome-stable_current_amd64.deb

#================
# Install Python
#================
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python3-setuptools python3-dev
RUN alias python=python3
RUN echo "alias python=python3" >> ~/.bashrc
RUN apt-get -qy --no-install-recommends install python3.10
RUN rm /usr/bin/python3
RUN ln -s python3.10 /usr/bin/python3

#=============================================
# Allow Special Characters in Python Programs
#=============================================
RUN export PYTHONIOENCODING=utf8
RUN echo "export PYTHONIOENCODING=utf8" >> ~/.bashrc

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
COPY sbase /SeleniumBase/sbase/
COPY seleniumbase /SeleniumBase/seleniumbase/
COPY examples /SeleniumBase/examples/
COPY integrations /SeleniumBase/integrations/
COPY requirements.txt /SeleniumBase/requirements.txt
COPY setup.py /SeleniumBase/setup.py
COPY MANIFEST.in /SeleniumBase/MANIFEST.in
COPY pytest.ini /SeleniumBase/pytest.ini
COPY setup.cfg /SeleniumBase/setup.cfg
COPY virtualenv_install.sh /SeleniumBase/virtualenv_install.sh
RUN find . -name '*.pyc' -delete
RUN pip install --upgrade pip setuptools wheel
RUN cd /SeleniumBase && ls && pip install -r requirements.txt --upgrade
RUN cd /SeleniumBase && pip install .

#=======================
# Download chromedriver
#=======================
RUN seleniumbase get chromedriver --path

#==========================================
# Create entrypoint and grab example tests
#==========================================
COPY integrations/docker/docker-entrypoint.sh /
COPY integrations/docker/run_docker_test_in_chrome.sh /
RUN chmod +x *.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["/bin/bash"]
