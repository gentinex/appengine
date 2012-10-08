import urllib2
import webapp2

from google.appengine.api import files # to use cloud storage api

class MainPage(webapp2.RequestHandler):
  def get(self):
      self.response.headers['Content-Type'] = 'text/plain'
      first_line = urllib2.urlopen('http://www.scottaaronson.com').readlines()[1]
      self.response.write('Hello2, my World!\n')
      self.response.write(first_line)

      filename = '/gs/jomyvideo/my_file'
      writable_file_name = files.gs.create(filename, mime_type='application/octet-stream', acl='public-read')
      with files.open(writable_file_name, 'a') as f:
        f.write('Hello World!')
        f.write('This is my first Google Cloud Storage object!')
        f.write('How exciting!')
      files.finalize(writable_file_name)

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)
