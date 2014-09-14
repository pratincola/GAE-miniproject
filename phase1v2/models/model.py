__author__ = 'prateek'
import sys

from google.appengine.ext import ndb


class UserObject(ndb.Model):
    # user_id = ndb.StringProperty(required=True) #using id instead of user_id, helps with indexing...
    nickname = ndb.StringProperty()
    email = ndb.StringProperty()
    subscribe_list = ndb.StringProperty(repeated=True)


class StreamObject(ndb.Model):
    stream_owner = ndb.KeyProperty(kind=UserObject)
    stream_name = ndb.StringProperty(required=True)
    stream_tag = ndb.StringProperty(repeated=True)
    cover_url = ndb.StringProperty()
    stream_count = ndb.IntegerProperty(default=0)
    img_count = ndb.IntegerProperty(default=0)
    stream_create_time = ndb.DateTimeProperty(auto_now_add=True)
    stream_modified_time = ndb.DateTimeProperty(auto_now=True) # need to update this value when the last image is inserted...


class Images(ndb.Model):
    stream_id = ndb.KeyProperty(kind=StreamObject)
    image_blob = ndb.BlobProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

