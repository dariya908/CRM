from django.contrib.auth.models import User
from django.core.mail import EmailMessage


def mailing(username):
    """
    1. Отфильтровать пользователей по is_superuser
    2. Email адреса superusero'ов добавить в новый список
    3. Отправить сообщения на полученные email
    """
    users = User.objects.filter(is_superuser=True)
    email_list = []
    for user in users:
        email_list.append(user.email)
    subject = 'Greetings!'
    body = f'User with {username} registered in military database, please check him!'
    email = EmailMessage(subject=subject, body=body, to=email_list)
    email.send()


def validated_password(password):
    if len(password) >= 8 and not password.isdigit() and not password.isalpha():
        return True
    else:
        return False
