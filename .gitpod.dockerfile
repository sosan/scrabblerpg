FROM buildpack-deps:disco

### base ###
RUN yes | unminimize \
    && apt-get install -yq \
        asciidoctor \
        bash-completion \
        build-essential \
        htop \
        jq \
        less \
        locales \
        man-db \
        nano \
        software-properties-common \
        sudo \
        vim \
        multitail \
        lsof \
    && locale-gen en_US.UTF-8 \
    && mkdir /var/lib/apt/dazzle-marks \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/*

ENV LANG=en_US.UTF-8

### Gitpod user ###
# '-l': see https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
RUN useradd -l -u 33333 -G sudo -md /home/gitpod -s /bin/bash -p gitpod gitpod \
    # passwordless sudo for users in the 'sudo' group
    && sed -i.bkp -e 's/%sudo\s\+ALL=(ALL\(:ALL\)\?)\s\+ALL/%sudo ALL=NOPASSWD:ALL/g' /etc/sudoers
ENV HOME=/home/gitpod
WORKDIR $HOME
# custom Bash prompt
RUN { echo && echo "PS1='\[\e]0;\u \w\a\]\[\033[01;32m\]\u\[\033[00m\] \[\033[01;34m\]\w\[\033[00m\] \\\$ '" ; } >> .bashrc

### Gitpod user (2) ###
USER gitpod
# use sudo so that user does not get sudo usage info on (the first) login
RUN sudo echo "Running 'sudo' for Gitpod: success"
# create .bashrc.d folder and source it in the bashrc
RUN mkdir /home/gitpod/.bashrc.d && \
    (echo; echo "for i in \$(ls \$HOME/.bashrc.d/*); do source \$i; done"; echo) >> /home/gitpod/.bashrc
	

### Python ###
LABEL dazzle/layer=lang-python
LABEL dazzle/test=tests/lang-python.yaml
USER gitpod
ENV PATH=$HOME/.pyenv/bin:$HOME/.pyenv/shims:$PATH
RUN curl -fsSL https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash \
    && { echo; \
        echo 'eval "$(pyenv init -)"'; \
        echo 'eval "$(pyenv virtualenv-init -)"'; } >> /home/gitpod/.bashrc.d/60-python \
    && pyenv install 2.7.16 \
    && pyenv install 3.7.4 \
    && pyenv global 2.7.16 3.7.4 \
    && pip2 install --upgrade pip \
    && pip2 install virtualenv pipenv pylint rope flake8 autopep8 pep8 pylama pydocstyle bandit notebook python-language-server[all]==0.25.0 \
    && pip3 install --upgrade pip \
    && pip3 install virtualenv pipenv pylint rope flake8 autopep8 pep8 pylama pydocstyle bandit notebook flask pymysql Flask-Bootstrap wtforms python-language-server[all]==0.25.0 \
    && rm -rf /tmp/*
# Gitpod will automatically add user site under `/workspace` to persist your packages.
# ENV PYTHONUSERBASE=/workspace/.pip-modules \
#    PIP_USER=yes

FROM gitpod/workspace-mysql


