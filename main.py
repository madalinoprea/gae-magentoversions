from google.appengine.ext import webapp
from google.appengine.api import memcache

import glob
import os

APP_DIR = os.path.dirname(__file__)
DOWNLOAD_DIR = '%s/magento' % APP_DIR

class IndexHandler(webapp.RequestHandler):
    def parse_files(self):
        client = memcache.Client()
        files = client.get('files')

        if files:
            return files

        files = []

        for filepath in glob.glob('%s/*' % DOWNLOAD_DIR):
            files.append(os.path.basename(filepath))

        client.set('files', files, 12*3600)

        return files

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        files = self.parse_files()
        content = "<h1>Available Magento Versions</h1>"
        content += "<ul>"
        for f in files:
            content += "<li><a href=\"/%s\">%s</a></li>" % (f, f)
        content += "</ul>"
        self.response.out.write(content)


app = webapp.WSGIApplication([
    ('/index.html', IndexHandler),
])



