__author__ = 'prateek'

import webapp2
import logging
import json
import jinja2
from google.appengine.api import users
log = logging.getLogger(__name__)


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('views'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class BaseHandler(webapp2.RedirectHandler):


    def __init__(self, request, response):
        self.initialize(request, response)

    def render_response(self, template_values, template='base.html'):

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            log.info(user.user_id())
                # ('Welcome, %s! (<a href="%s">sign out</a>)' %
                #         (user.nickname(), users.create_logout_url('/')))
        else:
            # greeting = ('<a href="%s">Sign in</a>.' %
            #             users.create_login_url('/'))
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            log.info("not logged in ")

        template_values['title'] = 'Connex.us'
        template_values['year'] = '2014'
        template_values['url'] = url
        template_values['url_linktext'] = url_linktext

        use_template = JINJA_ENVIRONMENT.get_template(template)
        self.response.write(use_template.render(template_values))

    def render_json(self, obj):
        jsonify = json.dump(obj)
        self.response.headers.content_type = 'application/json'
        self.response.write(jsonify)