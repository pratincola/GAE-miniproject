__author__ = 'prateek'
import sys

from google.appengine.ext import ndb
from models.modelUtil import ModelUtils
import logging


log = logging.getLogger(__name__)

class UserObject(ndb.Model):
    # user_id = ndb.StringProperty(required=True) #using id instead of user_id, helps with indexing...
    nickname = ndb.StringProperty()
    email = ndb.StringProperty()
    subscribe_list = ndb.StringProperty(repeated=True)

    ''' Input: Takes a user_id & stream_id stream
        It will subscribe the user to the stream by adding the stream id to user's subscribe list'''
    @classmethod
    def subscribe_stream(cls, user_id, stream_id):
        user_entity = cls.get_or_insert(user_id)
        stream_list = user_entity.subscribe_list
        stream_list.append(stream_id)
        user_entity.put()



    @classmethod # query doesnt work...
    def unsubscribe_stream(cls, user_id, stream_id):
        log.info(user_id)
        log.info(stream_id)
        user_entity = cls.query(cls.key==ndb.Key(cls, user_id)).get(projection=['subscribe_list'])
        log.info(user_entity.subscribe_list)
        for i,subscription in enumerate(user_entity.subscribe_list):
            log.info(i)
            log.info(subscription)
            if subscription == stream_id:
                log.info(stream_id)
                del cls.subscribe_list[i]
                cls.put()





class StreamObject(ModelUtils, ndb.Model):
    stream_owner = ndb.KeyProperty(kind=UserObject)
    stream_name = ndb.StringProperty(required=True)
    stream_tag = ndb.StringProperty(repeated=True)
    cover_url = ndb.StringProperty()
    stream_count = ndb.IntegerProperty(default=0)
    img_count = ndb.IntegerProperty(default=0)
    stream_create_time = ndb.DateTimeProperty(auto_now_add=True)
    stream_modified_Datetime = ndb.DateTimeProperty(auto_now_add=True) # need to update this value when the last image is inserted...
    stream_modified_day = ndb.ComputedProperty(lambda self: self.stream_modified_Datetime.strftime('%m/%d/%Y'))

    ''' Returns a list of stream for a given user'''
    @classmethod
    def my_stream(cls,accountUser_key, num):
        return cls.query(cls.stream_owner == accountUser_key)\
            .order(cls.stream_modified_Datetime)\
            .fetch()

    ''' Returns a list of stream a user is subscribed to'''
    @classmethod
    def my_subscription(cls, user_id, num):
        return cls.query(cls.stream_name.IN(UserObject
                                            .get_by_id(user_id)
                                            .subscribe_list)).fetch(num)
    ''' removes the stream with the given 'id' from the datastore'''
    @classmethod
    def remove_stream(cls, stream_id):
        return ndb.Key(cls, stream_id).delete()



class Images(ModelUtils, ndb.Model):
    stream_id = ndb.StringProperty()
    image_blob =  ndb.BlobKeyProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    ''' Returns a list of images for a given stream'''
    @classmethod
    def my_imgs(cls, stream_id, num, curs):
        return cls.query(cls.stream_id == stream_id)\
            .order(cls.date)\
            .fetch_page(num, start_cursor=curs)

