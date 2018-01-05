# nginx configs

I started migrating all my sites from Apache (mod_wsgi, mod_fcgid, mod_rewrite, etc.) over to nginx. For the interim phase I forwarded domains from nginx to Apache while slowly converting domains over.

The eventual goal is to get all sites running on Python/Flask/gunicorn and use supervisor ([details on that here](https://github.com/kirsle/rophako/wiki/Server-Configuration#nginx-configurations)) but in the mean time I had to set up PHP/CGI support in nginx.

These are some of those configs:

## mod_rewrite site with an index.cgi

Apache config using mod_rewrite:

```apache
<IfModule mod_rewrite.c>
	RewriteEngine on
	RewriteBase /
	RewriteCond %{REQUEST_FILENAME} !-f
	RewriteCond %{REQUEST_FILENAME} !-d
	RewriteRule . /index.cgi [L]
</IfModule>
```

Ported over to nginx:

```nginx
server {
	server_name noah.is;
	listen 80;

	root /home/www/sites/noah.is;
	index index.cgi index.html index.htm;

	location / {
		try_files $uri $uri/ /index.cgi;
	}

	# legacy CGI scripts
	# <https://wiki.debian.org/nginx/FastCGI>
	location ~ \.cgi$ {
		try_files $uri $uri/ /index.cgi;
		gzip off;
		fastcgi_pass unix:/var/run/fcgiwrap.socket;
		include fastcgi_params;
		fastcgi_param SERVER_NAME $host;
	}
}
```

## Legacy PHP and CGI Script Support

Kirsle.net used some PHP scripts ([Piwik Analytics](http://piwik.org/)) in the `/piwik` folder and some legacy CGI scripts (ttf2eot converter, etc.) in `/wizards` and these had to continue working while the rest of the site moved to gunicorn/supervisor/nginx.

Irrelevant aliases were removed from this snippet along with SSL settings (not very interesting).

```nginx
server {
	server_name www.kirsle.net kirsle.net;
	listen 443 ssl;

	# (ssl configs removed)

	index index.cgi index.html index.htm;

	root /home/www/git/rophako;

	location /static {
		alias /home/www/public_html/static;
	}
	location /piwik {
		alias /home/www/public_html/piwik;
		index index.php;
	}
	location /wizards {
		alias /home/www/public_html/wizards;
	}

	# uwsgi
	location / {
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $remote_addr;
		proxy_pass http://127.0.0.1:9000;
	}

	# run php scripts
	location ~ \.php$ {
		include fastcgi_params;
		fastcgi_split_path_info ^(.+\.php)(/.+)$;
		fastcgi_pass unix:/var/run/php5-fpm.sock;
		fastcgi_index index.php;
		fastcgi_param SCRIPT_FILENAME /home/www/public_html$fastcgi_script_name;
	}

	# legacy CGI scripts
	# https://wiki.debian.org/nginx/FastCGI
	location ~ \.cgi$ {
		try_files $uri $uri/ /index.cgi;
		gzip off;
		root /home/www/public_html;
		fastcgi_pass unix:/var/run/fcgiwrap.socket;
		include fastcgi_params;
		fastcgi_param SERVER_NAME $host;
	}
}
```