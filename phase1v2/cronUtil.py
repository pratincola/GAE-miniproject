__author__ = 'prateek'

import logging
from models import UserObject, StreamObject
from google.appengine.api import mail


log = logging.getLogger(__name__)


class CronUtils(object):
    def send_email(self, userList):
        log.info("inside get cron handler's emailer")
        result = [d.to_dict() for d in StreamObject.trending_streams(3)]
        log.info(result)
        if len(result) == 3:
            for user in userList:
                log.info(user)
                log.info(user.nickname)
                log.info(user.email)
                log.info(result)
                mail.send_mail(sender="Connex.us <burman.prateek@gmail.com>",
                               to="%s <%s>" % (user.nickname, user.email),
                               subject="Trending Report",
                               body=""" %s, %s, %s """ % (result[0]['stream_name'],
                                                          result[1]['stream_name'],
                                                          result[2]['stream_name']))
        if len(result) == 2:
            for user in userList:
                log.info(user)
                log.info(user.nickname)
                log.info(user.email)
                log.info(result)
                mail.send_mail(sender="Connex.us <burman.prateek@gmail.com>",
                               to="%s <%s>" % (user.nickname, user.email),
                               subject="Trending Report",
                               body=""" %s, %s """ % (result[0]['stream_name'],
                                                      result[1]['stream_name']))
        if len(result) == 1:
            for user in userList:
                log.info(user)
                log.info(user.nickname)
                log.info(user.email)
                log.info(result)
                mail.send_mail(sender="Connex.us <burman.prateek@gmail.com>",
                               to="%s <%s>" % (user.nickname, user.email),
                               subject="Trending Report",
                               body=""" %s """ % (result[0]['stream_name']))