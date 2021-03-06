from google.appengine.api.images import get_serving_url

__author__ = 'prateek'

import logging
import urllib
import json
from google.appengine.api import users
from base_handler import BaseHandler
from google.appengine.api import urlfetch
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images
from models import *


log = logging.getLogger(__name__)


class DefaultHandler(BaseHandler):
    def get(self):
        config = self.app.config
        super(DefaultHandler, self).render_response({})


class ManagementHandler(BaseHandler):
    def get(self):
        account_user = self.request.get('accountUser')
        if not account_user:
            user = users.get_current_user()
            account_user = user.user_id()
        log.info(account_user)
        ''' Streams I own: '''
        streams = [d.to_dict() for d in StreamObject.my_stream(ndb.Key("UserObject", account_user), 2)]

        ''' Streams I'm subscribed too'''
        # log.info(streams)
        user_entity = UserObject.get_by_id(account_user)
        # log.info(user_entity)
        # log.info(userEntity.subscribe_list)
        # subscribed_streams = [d.to_dict() for d in StreamObject.my_subscription(user_entity.subscribe_list, 2)]
        subscribed_streams = [d.to_dict() for d in StreamObject.my_subscription(account_user, 2)]
        self.render_response({'streams': streams, 'subscribedStreams': subscribed_streams}, 'manage.html')


    def post(self):
        account_user = self.request.get('accountUser')
        if not account_user:
            user = users.get_current_user()
            account_user = user.user_id()
        log.info(account_user)

        delete_stream = self.request.get_all('delete')
        if delete_stream:
            for items in delete_stream:
                log.info(items)
                StreamObject.remove_stream(items)

        # Doesn't work at the moment...
        # unsubs_stream = self.request.get_all('unsubscribe')
        # log.info(unsubs_stream)
        # if unsubs_stream:
        #     for items in unsubs_stream:
        #         log.info(items)
        #         UserObject.unsubscribe_stream(account_user, items)






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
        subscribersList = ['5629499534213120','pratincola','patrick@gmail.com','as@as.com']
        optionalMessage = "poop"
        streamTags = ['#lucknow','#india','#stuff']  # TODO: remove hashes when adding hashtags...
        coverURL = "http://www.w3schools.com/images/w3schools_green.jpg"
        user = users.get_current_user()
        log.info(user.user_id())
        # add a check to see if the user is logged-in ...else force login
        if True: #TODO: Need to add a method which parses the input & does not basic validation...
            u = UserObject(id=user.user_id(), nickname=user.nickname(), email=user.email(), subscribe_list=subscribersList)
            log.info(u)
            u_key = u.put() #perhaps user get_or_put function here...
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


class ViewSingleStreamHandler(blobstore_handlers.BlobstoreUploadHandler,
                              blobstore_handlers.BlobstoreDownloadHandler,
                              BaseHandler):
    ''' /ViewStream?stream={{stream['key']}}&cursor='''
    def get(self):

        upload_url = blobstore.create_upload_url('/ViewStream')
        log.info(upload_url)
        view_stream = self.request.get('stream')
        log.info(view_stream)
        ''' Add clicks... '''
        StreamObject.update_click_times(view_stream)

        curs = Cursor(urlsafe=self.request.get('cursor'))  # range
        log.info(curs)

        images, next_curs, more = Images.my_imgs(view_stream, 3, curs)
        # images = Images.my_imgs(view_stream, 3, curs)
        if not next_curs:
            next_curs_pos = ''
        else:
            next_curs_pos = next_curs.urlsafe()

        log.info(next_curs)
        log.info(more)
        log.info(images)

        # streams = [d.to_dict() for d in Images.my_imgs(ndb.Key("StreamObject", view_stream), 3, curs)]

        # blob_info = [blobstore.BlobInfo.get(img.image_blob) for img in images]
        blob_info = [get_serving_url(img.image_blob) for img in images]
        log.info(blob_info)
        # self.send_blob(blob_info)

        self.render_response({'images': blob_info,
                              'more': more,
                              'next_curs': next_curs_pos,
                              'uploadUrl': upload_url,
                              'stream_id': view_stream}, "view_single_stream.html")


    def post(self):
        error = ''
        stream_id = self.request.get('streamId')
        user_id = users.get_current_user().user_id()
        file_upload = self.get_uploads('fileField')
        subscribe_stream = self.request.get('subscribeStream')

        log.info(stream_id)
        log.info(user_id)
        log.info(file_upload)
        log.info(subscribe_stream)
        log.info(":(")

        if file_upload:
            blob_info = file_upload[0]
            log.info(blob_info)
            try:
                ''' Upload image...'''
                s = Images(stream_id=stream_id,
                           image_blob=blob_info.key())
                log.info(s)
                s.put()
                StreamObject.update_image_count(stream_id)
            except:
                error += " Problems uplaoding the picture"

        elif subscribe_stream and user_id:
            UserObject.subscribe_stream(user_id, stream_id)
        else:
            error += " You are not logged-in, please log-in and then subscribe"

        self.redirect('/ViewStream?stream=%s&cursor=' % stream_id)


class ViewAllStreamsHandler(BaseHandler):
    def get(self):

        stream_info = [d.to_dict() for d in StreamObject.get_covers_to_display()]
        log.info(stream_info)
        self.render_response({'stream': stream_info}, "view_all.html")

    ''' No implementation required as there is no action on this page. '''
    def post(self):
        pass


class SearchStreamsHandler(BaseHandler):
    def get(self):
        self.render_response({}, "search.html")

    def post(self):
        result = ''
        searh_term = self.request.get('localSearch')
        log.info(searh_term)
        if searh_term:
            result = [d.to_dict() for d in StreamObject.search_hash(searh_term, 5)]
            log.info(result)

        self.render_response({'search': searh_term,
                              'searchResult': result}, "search.html")


class TrendingStreamsHandler(BaseHandler):
    def get(self):
        error = self.request.get('error')
        result = [d.to_dict() for d in StreamObject.trending_streams(3)]
        self.render_response({'searchResult': result,
                              'error': error}, "trending.html")

    def post(self):
        error = ''
        update_rate = self.request.get('rate')
        log.info(update_rate)
        user = users.get_current_user()
        if user:
            u_id = user.user_id()
            UserObject.update_rate(u_id, update_rate)
            error += "Preference updated"
        else:
            error += "Please log-in before updating preference"

        self.redirect('/TrendingStreams?error=%s' % error)


class SocialMedia(BaseHandler):
    def get(self):
        config = self.app.config
        super(SocialMedia, self).render_response()


class ErrorHandler(BaseHandler):
    pass