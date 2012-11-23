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
# also note that appengine does not allow renaming of projects,
# and though it does allow deleting, the url jomyvideo.appspot.com
# can never be reused, so i opted to just still call this jomyvideo :)

import cgi
import Cookie
import os
import urllib2
import webapp2

from google.appengine.api import users

# home page has a CGI form to submit a web page to look at
class Request(webapp2.RequestHandler):
	def get(self):
	
		user = users.get_current_user()
		if user and str(user) in ['jomy.alappattu']:
			self.response.out.write("""
			  <html>
				<body>
				  <form action="/result" method="post">
					<input type="text" name="sitename" size=60><input type="submit" value="Submit URL">
				  </form>
				  <a href=\"%s\">Sign out</a>
				</body>
			  </html>""" % users.create_logout_url("/"))
		else:
			if user:
				self.response.out.write('Sorry, ' + str(user) + ' is not authorized to use this app.<br/>')
			else:
				self.response.out.write('Sorry, you need to be logged in to use this app.<br/>')
			self.response.out.write("""<a href=\"%s\">Go to login screen</a>.""" \
				% users.create_logout_url("/"))

# results page takes the submitted URL, reads it and displays content
class Results(webapp2.RequestHandler):
    def post(self):
		site = self.request.get('sitename')
		# discovered that the standard urllib2.urlopen() call
		# doesn't work on certain sites (e.g., wikipedia).
		# so have to create a different User-Agent
		req = urllib2.Request(site, headers={'User-Agent' : "Magic Browser"}) 
		site_source = urllib2.urlopen(req).read()			
		self.response.write(site_source)
	
app = webapp2.WSGIApplication([('/', Request),
							   ('/result', Results)])
