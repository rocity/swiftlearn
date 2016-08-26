Development				Production
Application
WSGI							uWSGI (gunicorn, tornado, fastcgi)
Webserver
SimpleHTTPServer	NGINX (Apache, IIS)


1. System Requirements
	apt-get install git

2. Python Backports
	add-apt-repository ppa:fkrull/deadsnakes
	apt-get update
	apt-get install python3.5

3. Create Virtualenv
	apt-get install python-virtualenv
	virtualenv --python=`which python3.5` env
	source env/bin/activate

4. Install Requriements
	4.a. Prerequiset
		# Pillow
		apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

		# Python Headers
		apt-get install python3.5-dev

		# Postgres Lib
		apt-get install libpq-dev

	4.b.
		pip install -r requirements.txt --verbose

5. Webserver
	5.a. apt-get install nginx

	5.b. NGINX Config
	# /etc/nginx/sites-enabled/swiftlearn.nginxconf
	```
	upstream swiftlearn_app {
		server 127.0.0.1:3031;
	}
	server {
			server_name 128.199.158.203;
				location / {
					include uwsgi_params;
					uwsgi_pass swiftlearn_app;
			}
		location /static {
			alias /root/swiftlearn/static;
		}
	}
	```

6. Application Handler
	6.a. pip install uwsgi

	6.b.
	# /etc/init/swiftlearn.conf
	```
	description "Swiftlearn Application"

	start on runlevel [2345]
	stop on runlevel [!2345]

	setuid root
	setgid root

	exec /root/env/bin/uwsgi --chdir=/root/swiftlearn --home=/root/env --module=swiftlearn.wsgi:application --socket=0.0.0.0:3031
	```

7. Database Server
	7.a. apt-get install postgresql
	7.b.
	sudo -u postgres psql postgres
	\password # change password

	7.c.
	sudo -u postgres createdb swiftlearn
	7.d.
	nano local_settings.py
	```
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.postgresql',
	        'NAME': 'swiftlearn',
	        'USER': '',
	        'PASSWORD': '',
	        'HOST': 'localhost',
	        'PORT': '5432',
	    }
	}
	```
