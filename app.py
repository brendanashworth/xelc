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
		chars = []
		while (count >= 0):
			if count > 25:
				chars.append(25)
			else:
				chars.append(count)

			count -= 25

		str = ''
		for char in chars:
			str += chr(97 + char)

		r.hset('links', str, request.form['url'])
		return str

@app.route('/<link>')
def get_link(link):
	url = r.hget('links', link)

	if url:
		return redirect(url)
	else:
		return abort(404)


app.run(host=app.config['APP_HOST'], port=app.config['APP_PORT'])