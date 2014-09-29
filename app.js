// app
var Mustache = require('mustache'),
	fs = require('fs'),
	md5 = require('md5'),
	express = require('express'),
	app = express(),;

// redis
var redis = require('redis'),
	client = redis.createClient();

// Handle middleware
app.use(express.bodyParser());
app.use('/static', express.static('static'));

// Request main page
app.get('/', function(req, res) {
	// Get amount of links
	client.hlen('links', function(err, count) {
		if (err) {
			res.status(500).send('Uh oh! An error has occurred.').end();
			return;
		}

		// some base url value?
		var index = ':)';

		// Render response
		fs.readFile('./templates/index.html', function(err, data) {
			if (err) {
				res.status(500).send('Uh oh! An error has occurred.').end();
				return;
			}

			// Send to client
			res.status(200).send(Mustache.render(data, {count: count, baseUrl: index}));
		});
	});
});

// Submit a link
app.post('/', function(req, res) {
	var url = req.body.url,
		regex = /(https?://([-\w\.]+)+(:\d+)?(/([\w/_\.]*(\?\S+)?)?)?)/;

	// Ensure user supplied URL
	if (!url || !regex.match(url)) {
		res.status(500).send('Must supply valid URL.').end();
		return;
	}
	
	var link = md5.digest_s(url).substring(0, 6);

	client.hset('links', link, url, function() {
		res.status(200).send(link).end();
	});
});

// Visit a link
app.get('/:link', function(req, res) {
	var link = req.params.link,
		regex = /^[0-9a-zA-Z]{7}$/;

	// Ensure valid link
	if (!link || !regex.match(link)) {
		res.status(500).send('Must supply valid link.').end();
		return;
	}

	client.hget('links', link, function(err, url) {
		if (err) {
			res.status(404).send('Link not found.').end();
			return;
		}

		res.redirect(url);
	});
});