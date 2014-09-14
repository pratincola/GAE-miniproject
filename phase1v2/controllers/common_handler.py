__author__ = 'prateek'

import logging
from google.appengine.api import users
from base_handler import BaseHandler
from models import *


log = logging.getLogger(__name__)

class DefaultHandler(BaseHandler):
    def get(self):
        config = self.app.config
        super(DefaultHandler, self).render_response({})



class ManagementHandler(BaseHandler):
    def get(self):
        user = self.request.get('accountUser')
        # log.info(user)
        # userEntity = UserObject.get_by_id(user)
        # log.info(userEntity)
        # log.info(userEntity.key)
        # user_key = ndb.Key("UserObject", user)
        # log.info(user_key)
        ''' Streams I own: '''
        streams = [ d.to_dict() for d in StreamObject.query(StreamObject.stream_owner==ndb.Key("UserObject", user)).fetch(2)]
        log.info(streams)
        self.render_response({'streams':streams}, 'manage.html')



    def post(self):
        self.render_response('manage.html')





class CreateStreamHandler(BaseHandler):
    def get(self):
        self.render_response({}, 'create.html')

    def post(self):
        # streamName = self.request.get('streamName')
        # subscribersList = (self.request.get('subscribersList')).split(',')
        # optionalMessage = self.request.get('optionalMessage')
        # streamTags = (self.request.get('streamTags')).split(',')
        # coverURL = self.request.get('coverURL')
        # user = users.get_current_user()
        streamName = "pratincola"
        subscribersList = ['pratik@gmail.com','patrick@gmail.com','as@as.com']
        optionalMessage = "poop"
        streamTags = ['#lucknow','#india','#stuff']
        coverURL = "http://facebook.com/?page=timemachine"
        user = users.get_current_user()

        if True: #TODO: Need to add a method which parses the input & does not basic validation...
            u = UserObject(id=user.user_id(), nickname=user.nickname(), email=user.email(), subscribe_list=subscribersList)
            log.info(u)
            u_key = u.put()
            log.info(u_key)
            s = StreamObject(stream_owner=u_key,
                             stream_name=streamName,
                             stream_tag=streamTags,
                             cover_url=coverURL
                             )
            s.put()
            log.info(s)
            log.info(user)
            self.redirect("/ManagementPage?accountUser=%s" %user.user_id())

        else: #TODO: Need to add error message to the page stating that user didn't enter all the fields...
            self.response.write('create.html')




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