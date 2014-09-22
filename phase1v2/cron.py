__author__ = 'prateek'

#!/usr/bin/env python
#
import webapp2

from controllers import *
from config import app_config
from google.appengine.api import mail
from cronUtil import CronUtils
from datetime import datetime, timedelta

log = logging.getLogger(__name__)


class FiveMinCronHandler(webapp2.RequestHandler):
    def get(self):
        log.info("inside get cron handler ")

        # Update streams with trending value
        stream_objects = StreamObject.get_click_times()
        log.info(stream_objects)
        for stream in stream_objects:
            log.info(stream.click_times)
            if stream.click_times:
                stream.trending_stream_count = len(stream.click_times)
                stream.put()

        log.info(" e-mail logic")
        five_min_users = UserObject.get_users_for_rate(5)
        log.info(five_min_users)
        if five_min_users:
            CronUtils().send_email(five_min_users)


class OneHourCronHandler(webapp2.RequestHandler):
    def get(self):
        now = datetime.now()
        onehourago = now - timedelta(seconds=3600)

        log.info(now)
        log.info(onehourago)

        pquery = StreamObject.query(StreamObject.click_times < onehourago).fetch()
        log.info(pquery)
        # Remove all items from the list that are older than 1 hour
        for stream in pquery:
            log.info(stream.click_times)
            for i, t in enumerate(stream.click_times):
                log.info(t)
                log.info(stream.click_times[i])
                if t < onehourago:
                    stream.click_times.remove(stream.click_times[i])
            stream.put()

        log.info(" e-mail logic")
        one_hour_users = UserObject.get_users_for_rate(60)
        log.info(one_hour_users)
        if one_hour_users:
            CronUtils().send_email(one_hour_users)


class OneDayCronHandler(webapp2.RequestHandler):
    def get(self):

        log.info(" e-mail logic")
        one_hour_users = UserObject.get_users_for_rate(1440)
        log.info(one_hour_users)
        if one_hour_users:
            CronUtils().send_email(one_hour_users)


route_list = [(r'^/tasks/trending', FiveMinCronHandler),
              (r'^/tasks/onehour', OneHourCronHandler),
              (r'^/tasks/oneday', OneDayCronHandler)]

app = webapp2.WSGIApplication(route_list,
                              config=app_config,
                              debug=app_config.get('debug', True))
