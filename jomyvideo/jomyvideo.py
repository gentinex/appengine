# google app engine app to take an input URL,
# then display its contents on a separate page
# idea is that if one's internet connection blocks a site,
# this should be able to retrieve the site via google's
# computing resources and then display them to the user.

# of course it's likely that embedded objects from the
# same location as the blocked site (e.g., pics, video)
# will not display on the output. so better for wikipedia
# than tumblr say
# TODO: is it possible to use some scraper, say
# BeautifulSoup or scrapy or wget, to download such objects
# and display the page?

# originally, this was meant to be an app to download
# youtube videos. however, i ran into various issues:
# (1) the state-of-the-art python program for this -
#     youtube-dl - uses certain python modules (e.g.,
#     ctypes, socket) that are not supported in appengine
# (2) even if one were to package this up as an executable,
#     appengine does not allow executables to be run
# (3) i looked into various alternatives to youtube-dl,
#     but they only work with older versions of youtube,
#     or are based on Python3, so incompatible with appengine
# so i'm going to look into building the youtube app with django.
# also note that appengine does not allow deleting or renaming
# of projects, which is why this is still called jomyvideo :)

import cgi
import hashlib
import urllib2
import webapp2

# home page has a CGI form to submit a web page to look at
class Request(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("""
		  <html>
			<body>
			  <form action="/result" method="post">
				URL <input type="text" name="sitename" size=60><br/>
				Password <input type="password" name="password" size=60><input type="submit" value="Submit">
			  </form>
			</body>
		  </html>""")

# results page takes the submitted URL, reads it and displays content
class Results(webapp2.RequestHandler):
    def post(self):
		# in retrospect, could probably have restricted via
		# user authentication (plus checking that the authenticated
		# user was on a whitelist) rather than using password encryption..
		password = self.request.get('password')
		password_hex = hashlib.sha512(password).hexdigest()
		if password_hex == 'a954d57d365dae1e25c5c8a2a46e266acf5f32dcfedd2c232fa5aea46c0ec28de494a59c147f34752c931e43e0c29feb90e3ee80db76b58a5a1449dc0a33bc60':
			site = self.request.get('sitename')
			# discovered that the standard urllib2.urlopen() call
			# doesn't work on certain sites (e.g., wikipedia).
			# so have to create a different User-Agent
			req = urllib2.Request(site, headers={'User-Agent' : "Magic Browser"}) 
			site_source = urllib2.urlopen(req).read()			
			self.response.write(site_source)
		else:
			self.response.write('Invalid password.')
		
app = webapp2.WSGIApplication([('/', Request),
							   ('/result', Results)],
                              debug=True)
