from celery.decorators import task
from celery.utils.log import get_task_logger, logger
import time

from .celery.send_new_feeds_mail import send_mail_to
sleeplogger = get_task_logger(__name__)


@task(name='send_notification_to_followers_task')
def send_notification_to_followers_task(duration, obj_id):
    from blog.models import Post
    obj = Post.objects.get(id=int(obj_id))
    subject = 'Celery'
    message = f'My task done successfully'
    is_task_completed = False
    error = ''
    receivers = []
    for follower in obj.blog.follower_set.all():
        receivers.append(follower.user.email)
    try:
        time.sleep(duration)
        is_task_completed = True
    except Exception as err:
        error = str(err)
        logger.error(error)
    if is_task_completed:
        send_mail_to(subject, message, receivers)
    else:
        send_mail_to(subject,error, receivers)
    return('send_notification_to_followers_task done')

