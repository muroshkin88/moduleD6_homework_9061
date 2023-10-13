import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from ...models import Category, Post, SubscribedUsersCategory
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def my_job():
    if SubscribedUsersCategory.objects.all().exists():
        subscribers = SubscribedUsersCategory.objects.all()
        for subscriber in subscribers:
            user = subscriber.subscribed_users
            print(user)
            subject = f'Здравствуйте, {user}! Еженедельная рассылка новостей по категории "{subscriber.category}"'

            postList = Post.objects.filter(dateCreat__gte =(datetime.today() - timedelta(days=7)), category=subscriber.category.pk)
            for post in postList:
                print(post.title,post.author, post.dateCreat, subscriber.category)

            html_content = render_to_string('distribution.html', {'postlist': postList, })
            msg = EmailMultiAlternatives(
                subject=subject,
                body='',
                from_email= settings.DEFAULT_FROM_EMAIL ,
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/30"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")