from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import PostCategory, SubscribedUsersCategory, Category, Post
from django.contrib.auth.models import User
from django.template.loader import render_to_string



@receiver(post_save, sender=Post)
def notify_managers_appointment(sender, instance, created, **kwargs):

    pst=Post.objects.get(pk = instance.pk)
    print(pst.categoryType, pst.title)
    for category in pst.category.all():
        print (category)
        if created:
            html_content = render_to_string('new_post.html', {'post': instance, })
            for rec in category.subscribed_users.all():
                subject = f'Здравствуй, {rec} ! В категории "{category}" создана новая новость!'
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body='',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to= [rec.email] ,
                    )
    
                msg.attach_alternative(html_content, "text/html")
                msg.send()  


@receiver(m2m_changed, sender=Post.category.through)
def notify_managers_appoint(instance, action, pk_set, *args, **kwargs):
    if action == 'post_add':

        html_content = render_to_string('new_post.html', {'post': instance, })
        sec = instance.title
        we = instance.pk
        for pk1 in pk_set:
            
            category = Category.objects.get(pk=pk1)
            for rec in category.subscribed_users.all():
                subject = f'Здравствуй,{rec} ! В категории "{category}" создана новая новость!'
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body='',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to= [rec.email] ,
                    )
    
                msg.attach_alternative(html_content, "text/html")
                msg.send() 
