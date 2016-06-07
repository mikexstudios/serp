# Pull base image.
FROM ubuntu:14.04

RUN apt-get update && \
    apt-get install -y ca-certificates vim-tiny screen wget unzip

# Set up RabbitMQ broker (we can't setup vhost and user here since the
# settings don't presist).
RUN apt-get install -y rabbitmq-server

# Installs python 2.7.6 and packages necessary to install requirements.txt
# TEMPORARY FIX: libc version in cache is outdated so need to refresh
#                apt-get here
RUN apt-get update && apt-get install -y python python-dev python-pip git

# Set up our app files and install
RUN mkdir -p /usr/src/app
COPY . /usr/src/app
WORKDIR /usr/src/app
# Since pip -e are installed in /usr/src/app/src, it gets overwritten if we
# mount the current directory in /usr/src/app. Thus, we install src packages
# in another directory. See: http://stackoverflow.com/q/29905909/66771
RUN pip install -r requirements.txt --src /usr/local/src

# app
EXPOSE 80
VOLUME ["/usr/src/app"]
CMD /etc/init.d/rabbitmq-server start && \
    rabbitmqctl add_vhost serp && \
    rabbitmqctl set_permissions -p serp guest ".*" ".*" ".*" && \
    python manage.py syncdb --noinput && \
    python manage.py migrate && \
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python manage.py shell && \
    python manage.py celeryd & \
    python manage.py runserver 0.0.0.0:80
