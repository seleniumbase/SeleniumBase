# SeleniumBase Docker Image
FROM ubuntu:24.04
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8
ENV DEBIAN_FRONTEND=noninteractive

#======================
# Locale Configuration
#======================
RUN apt-get update
RUN apt-get install -y --no-install-recommends tzdata locales
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8
RUN echo "LC_ALL=en_US.UTF-8" >> /etc/environment
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
RUN echo "LANG=en_US.UTF-8" > /etc/locale.conf
RUN locale-gen en_US.UTF-8

#===========================
# Fingerprint Configuration
#===========================
RUN apt-get update
RUN apt install -y fonts-liberation fonts-noto-color-emoji libvulkan1 libnss3 libatk-bridge2.0-0 libcups2 libxcomposite1 libxrandr2 libgbm1 libpango-1.0-0 libcairo2
RUN apt install -y fonts-freefont-ttf fonts-dejavu-core fonts-ubuntu fonts-roboto fonts-droid-fallback

#======================
# Install Common Fonts
#======================
RUN apt-get update
RUN apt-get install -y \
    fonts-liberation2 \
    fonts-font-awesome \
    fonts-terminus \
    fonts-powerline \
    fonts-open-sans \
    fonts-mononoki \
    fonts-lato

#============================
# Install Linux Dependencies
#============================
RUN apt-get update
RUN apt-get install -y \
    dbus-x11 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libdbus-1-3 \
    libdrm2 \
    libgtk-3-0 \
    libnspr4 \
    libasound2t64 \
    libu2f-udev \
    libwayland-client0 \
    libx11-6 \
    libx11-xcb1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0

#==========================
# Install useful utilities
#==========================
RUN apt-get update
RUN apt-get install -y xdg-utils ca-certificates x11vnc

#=================================
# Install Bash Command Line Tools
#=================================
RUN apt-get update
RUN apt-get -qy --no-install-recommends install \
    curl \
    sudo \
    unzip \
    vim \
    wget \
    xvfb

#================
# Install Chrome
#================
RUN apt-get update
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
RUN rm ./google-chrome-stable_current_amd64.deb

#================
# Install Python
#================
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get update
RUN apt-get install -y python3.13 python3.13-venv python3.13-dev build-essential
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.13 1
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
RUN python3.13 -m ensurepip --upgrade
RUN python3.13 -m pip install --upgrade pip
RUN apt-get update
RUN apt-get install -y python3.13-tk python3.13-dev
RUN alias python=python3
RUN echo "alias python=python3" >> ~/.bashrc
RUN rm /usr/bin/python3
RUN ln -s python3.13 /usr/bin/python3

#===============
# Cleanup Lists
#===============
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

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
RUN pip install pyautogui
RUN pip install playwright
RUN seleniumbase get cft
RUN seleniumbase get chromium

#=======================
# Download chromedriver
#=======================
RUN seleniumbase get chromedriver --path

#==============
# Extra config
#==============
ENV DISPLAY=":99"
RUN Xvfb :99 -screen 1 1920x1080x16 -nolisten tcp &

#==========================================
# Create entrypoint and grab example tests
#==========================================
COPY integrations/docker/docker-entrypoint.sh /
COPY integrations/docker/run_docker_test_in_chrome.sh /
RUN chmod +x *.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["/bin/bash"]
