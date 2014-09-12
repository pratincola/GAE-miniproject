__author__ = 'prateek'

import logging

log = logging.getLogger(__name__)

from base_handler import BaseHandler

class DefaultHandler(BaseHandler):
    def get(self):
        config = self.app.config
        super(DefaultHandler, self).render_response()


class ManagementHandler(BaseHandler):
    pass

class CreateStreamHandler(BaseHandler):
    pass

class ViewSingleStreamHandler(BaseHandler):
    pass

class ViewAllStreamsHandler(BaseHandler):
    pass

class SearchStreamsHandler(BaseHandler):
    pass

class TrendingStreamsHandler(BaseHandler):
    pass

class SocialMedia(BaseHandler):
     def get(self):
        config = self.app.config
        super(SocialMedia, self).render_response()

class ErrorHandler(BaseHandler):
    pass