from flask import Flask, request, render_template, redirect, abort

app = Flask(__name__);
app.config.update(
	DEBUG=True,
	SECRET_KEY='changeme',
	REDIS_HOST='localhost',
	REDIS_PORT=6379,
	REDIS_DB=0,

	APP_HOST='0.0.0.0',
	APP_PORT=5000,

	URL_BASE = 'http://192.168.1.149:5000/' # Must end with a slash
);

import redis
r = redis.StrictRedis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], db=app.config['REDIS_DB'])

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
def index(path):
	count = r.hlen('links')
	if request.method == 'GET':
		return render_template('index.html', count=count, url_base=app.config['URL_BASE'])
	else:
		# UEL regexp from django
		import re
		regex = re.compile(
			r'^(?:http)s?://' # http:// or https://
			r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
			r'localhost|' # localhost...
			r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
			r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
			r'(?::\d+)?' # optional port
			r'(?:/?|[/?]\S+)$', re.IGNORECASE)

		if not regex.search(request.form['url']):
			return 'Invalid URL! Be sure to prepend with http:// or https://', 400

		chars = []

		import math
		def shorten(input):
			pointer = math.floor(input / 26)
			if pointer > 26:
				pointer = shorten(pointer)
			else:
				remainder = input % 26
				chars.append(pointer)
				chars.append(remainder)

			return count

		shorten(count)

		str = ''
		for char in chars:
			str += chr(97 + char)

		r.hset('links', str, request.form['url'])
		return str, 200

@app.route('/<link>')
def get_link(link):
	url = r.hget('links', link)

	if url:
		return redirect(url)
	else:
		return abort(404)

from gevent.wsgi import WSGIServer
http_server = WSGIServer(('', app.config['APP_PORT']), app)
http_server.serve_forever()