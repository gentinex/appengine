import cgi
import urllib2
import webapp2

from google.appengine.api import files # to use cloud storage api

# home page has a CGI form to submit a web page to look at
class Request(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("""
		  <html>
			<body>
			  <form action="/result" method="post">
				<input type="text" name="sitename" size=80><input type="submit" value="Submit URL">
			  </form>
			</body>
		  </html>""")

# results page takes the submitted URL, reads its first line and saves to
# google cloud storage
class Results(webapp2.RequestHandler):
    def post(self):
		site = self.request.get('sitename')
		first_line = urllib2.urlopen(site).readlines()[0]
		self.response.write('web site=' + site)
		
		filename = '/gs/jomyvideo/source.txt'
		writable_file_name = files.gs.create(filename, mime_type='application/octet-stream', acl='public-read')
		with files.open(writable_file_name, 'a') as f:
			f.write(first_line)
		files.finalize(writable_file_name)

app = webapp2.WSGIApplication([('/', Request),
							   ('/result', Results)],
                              debug=True)
