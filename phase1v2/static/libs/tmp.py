__author__ = 'prateek'

#!/usr/bin/env python


import webapp2
import json
import urllib
from google.appengine.api import urlfetch

###############################################################################

def html_generateContainerDiv(containerTitle,bgcolor):
    handlerContainer = '<div style="border-style:solid;border-width:1px;padding:0.5em 0 0.5em 0.5em;background-color:%s;">%s</div>' % (bgcolor, containerTitle )
    return handlerContainer

def html_generateContainerDivBlue(containerTitle):
    divColor = '#B0C4DE'
    return html_generateContainerDiv(containerTitle, divColor)

###############################################################################


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

###############################################################################
#< class_JsonTest>
# inspiration: http://stackoverflow.com/a/12664865
# doc: https://developers.google.com/appengine/docs/python/tools/webapp/responseclass#Response_out
# The contents of this object are sent as the body of the response when the request handler method returns.
#   http://stackoverflow.com/a/10871211
#   self.response.write and self.response.out.write are same thing
'''
Sample Usage:
  assumes that service accepts query params in to decide what to do
  from google.appengine.api import urlfetch
  # create query_params
  url = self.request.host_url
  result = urlfetch.fetch(url + urllib.urlencode(query_params),method=urlfetch.POST)
  if(result.status_code == 200):
    jsonStr += json.loads(result.content)
'''
class JsonTest(webapp2.RequestHandler):
  def post(self):
    jsonStr = self.get_json_str()
    self.response.write(jsonStr)
    #self.response.write('{"success": "some var", "payload": "some var"}')

  def get(self):
    response = '' # store request response
    user_name = self.request.get('userid','user_unspecified')
    query_params = urllib.urlencode({'userid': user_name})

    if(0):
      result = self.test_urlfetch()
      result = html_generateContainerDiv(result,'salmon') # websafe colours
      response += result

    url = self.request.host_url
    service_url = '/jsonreturntest'
    url += service_url
    #result = urlfetch.fetch(url + urllib.urlencode(query_params),method=urlfetch.POST)
    result = urlfetch.fetch(url,method=urlfetch.POST)
    #response += urlfetch.fetch(url,method=urlfetch.POST)
    if(result.status_code == 200):
      jsonStr = 'This code will make this page POST to itself and then read the output.<br/>\n'
      jsonStr += 'Python Code:<br/>\n' #'Example json return string that a service could use:<br/>\n'
      jsonStr += '<pre>'
      jsonStr += "jsonData = \"\"\n"
      jsonStr += "result = urlfetch.fetch('%s',method=urlfetch.POST)\n" % url
      jsonStr += "  if(result.status_code == 200):\n"
      jsonStr += "    jsonData = json.loads(result.content)\n"
      jsonStr += '</pre>'
      jsonStr += '<pre>'
      jsonStr = 'This is the output:<br/>\n'
      jsonStr += json.loads(result.content)
      jsonStr += '</pre>'
    else:
      jsonStr = 'request failed: ' + str(result.status_code)
    #< />
    jsonReturnText = 'This code will make this page POST to itself and then read the output.<br/>\n' + jsonStr
    response += html_generateContainerDivBlue(jsonReturnText)

    #greetText = 'This page generates the following json string when visited with POST:<br/>\n' + self.get_json_str()
    #response += html_generateContainerDivBlue(greetText) # websafe colours
    # wrap in grey div
    response = html_generateContainerDiv('<h1>Handler: JsonTest</h1>' + response,'#C0C0C0')
    response = '<html>\n  <body>\n' + response + '\n  </body>\n</html>'
    self.response.write(response)
  #< def_get_json_str>
  def get_json_str(self):
    return json.dumps('{"success": "some var", "payload": "some var"}')
  #</def_get_json_str>
  #< def test_urlfetch>
  def test_urlfetch(self):
    #TODO: as a testing exercise, rewrite to capture status messages and print summary
    #NOTE: this is how I learned that port 80 is the default port that non-specific query will use
    #      that is why this "coverage tests" all urls with "no port", 80, and 8080
    from google.appengine.api import urlfetch

    result = '<h1>TESTCODE OUTPUT</h1>'
    result += 'self.request.url is ' + self.request.url + '<br/>' + '\n'
    result += 'self.request.path is ' + self.request.path + '<br/>' + '\n'
    result += 'self.request.host_url is ' + self.request.host_url + '<br/>' + '\n'
    relpath = 'jsonreturntest'
    testUrls =  [
        self.request.host_url,
        self.request.host_url + '/' + relpath,
        '' + relpath,
        '/' + relpath,
        # find out why running on port :80 allowed '/<path>' to work
        'localhost/' + relpath,
        'localhost:80/' + relpath,
        'localhost:8080/' + relpath,
        'http://localhost/' + relpath,
        'http://localhost:80/' + relpath,
        'http://localhost:8080/' + relpath
        ]
    for url in testUrls:
      result += '>try:> urlfetch.fetch(\'%s\',method=urlfetch.POST)' % url

      result += '<br/>' + '\n'
      try:
        urlfetch.fetch(url,method=urlfetch.POST)
        result+='SUCCESS'
      except:
        result+='&nbsp;&nbsp;&nbsp;failure'
      result += '<br/>' + '\n'
    return result
    response += '\n'+result+'\n'
    #</send POST request>
    self.response.write(response)
  #<def test_urlfetch>
#</class_JsonTest>
###############################################################################

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/jsonreturntest',JsonTest),
], debug=True