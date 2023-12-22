# set up timezone since other packages (like firefox) need it
RUN apt-get -qq update && DEBIAN_FRONTEND=noninteractive apt-get -y --no-install-recommends install \
    tzdata \
  && rm -rf /var/lib/apt/lists/*

RUN apt-get -qq update && apt-get -y --no-install-recommends install \
    build-essential \
    cppcheck \
    doxygen \
    firefox \
    # need git in order to use vcstool
    git \
    gnupg \
    lsb-release \
    python3-dev \
    # used to install colcon, vcstool and psutil
    python3-pip \
    wget \
    # xdg-utils allows for users to open remotery (profiler in gz-common) in Docker
    xdg-utils \
  && rm -rf /var/lib/apt/lists/*

# set up repositories for Gazebo
# (add nightlies in case users want the newest Gazebo version)
RUN sh -c 'wget -qq https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg' \
  && sh -c 'echo "deb [arch=`dpkg --print-architecture` signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list' \
  && sh -c 'echo "deb [arch=`dpkg --print-architecture` signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-nightly `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-nightly.list'

# install colcon, vcstool and psutil (psutil is for sdformat memory leak tests)
RUN pip3 install setuptools wheel \
  && pip3 install colcon-common-extensions vcstool psutil

# install the specified Gazebo version
RUN apt-get -qq update && apt-get -y --no-install-recommends install \
    gz-@(gz_distro) \
  && rm -rf /var/lib/apt/lists/*

# install remaining build dependencies for the specified Gazebo version
# (in case users want to build Gazebo repositories from source)
RUN mkdir /temp_repos \
  && cd /temp_repos \
  && wget https://raw.githubusercontent.com/gazebo-tooling/gazebodistro/master/collection-@(gz_distro).yaml \
  && vcs import < collection-@(gz_distro).yaml \
  && apt-get -qq update && apt-get -y --no-install-recommends install \
    $(sort -u $(find . -iname 'packages-@(system_version).apt' -o -iname 'packages.apt') | grep -Ev 'libgz|libsdformat' | tr '\n' ' ') \
  && rm -rf /var/lib/apt/lists/* \
  && cd / \
  && rm -rf /temp_repos
