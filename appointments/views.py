from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers
from .models import Appointment


def notify_managers_appointment(sender, instance, created, **kwargs):
    # в зависимости от того, есть ли такой объект уже в базе данных или нет, тема письма будет разная
    if created:
        subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'
    else:
        subject = f'Appointment changed for {instance.client_name} {instance.date.strftime("%d %m %Y")}'

    mail_managers(
        subject=subject,
        message=instance.message,
    )

# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=Appointment)
def notify_managers_appointment(sender, instance, created, **kwargs):
    if created:
        subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'
    else:
        subject = f'Appointment changed for {instance.client_name} {instance.date.strftime("%d %m %Y")}'

    mail_managers(
        subject=subject,
        message=instance.message,
    )
# 1 вариант

from django.shortcuts import render, reverse, redirect

from django.views import View

from django.core.mail import send_mail, EmailMultiAlternatives, mail_admins
# импортируем класс для создание объекта письма с html
# импортируем функцию для массовой отправки писем админам
from datetime import datetime
from django.template.loader import render_to_string
# импортируем функцию, которая срендерит наш html в текст
from .models import Appointment


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # отправляем письмо
        send_mail(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
            # имя клиента и дата записи будут в теме для удобства
            message=appointment.message,  # сообщение с кратким описанием проблемы
            from_email='Konstantin-sama@yandex.ru',
            # здесь указываете почту, с которой будете отправлять (об этом попозже)
            recipient_list=['kalinkinkonstantin00@gmail.com']
            # здесь список получателей. Например, секретарь, сам врач и т. д.
        )
        # получаем наш html
        html_content = render_to_string(
            'appointment_created.html',
            {
                'appointment': appointment,
            }
        )

        # в конструкторе уже знакомые нам параметры, да? Называются правда немного по-другому, но суть та же.
        msg = EmailMultiAlternatives(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
            body=appointment.message,  # это то же, что и message
            from_email='Konstantin-sama@yandex.ru',
            to=['kalinkinkonstantin00@gmail.com'],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()  # отсылаем

        # отправляем письмо всем админам по аналогии с send_mail, только здесь получателя указывать не надо
        mail_admins(
            subject=f'{appointment.client_name} {appointment.date.strftime("%d %m %Y")}',
            message=appointment.message,
        )

        return redirect('appointments:make_appointment')




# вариант 2

from datetime import datetime

from django.shortcuts import render, redirect
from django.views import View

from news.models import Category, Post
from .models import Appointment


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # отправляем письмо
        send_mail(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
            # имя клиента и дата записи будут в теме для удобства
            message=appointment.message,  # сообщение с кратким описанием проблемы
            from_email='yerzhan.kaiyrbek@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
            recipient_list=['kairbek_erzhan@mail.ru',]  # здесь список получателей. Например, секретарь, сам врач и т. д.
        )

        return redirect('appointments:make_appointment')


class AppointView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'test_test.html')

    def post(self, request):
        pole_test = request.POST['test']
        if pole_test:
            pole_test = pole_test
        else:
            pole_test = 1

        pole_test2 = request.POST['test2']
        if pole_test2:
            pole_test2 = pole_test2


        pole_spisok1 = Category.objects.get(pk=pole_test)

        pole_spisok2 = Category.objects.get(pk=pole_test).subscribers.all()

        for category in Category.objects.all():

            news_from_each_category = []

            for news in Post.objects.filter(category_id=category.id,
                                            dateCreation__week=datetime.now().isocalendar()[1] - 1).values('pk',
                                                                                                           'title',
                                                                                                           'dateCreation'):
                new = (f'{news.get("title")}, {news.get("dateCreation")}, http://127.0.0.1:8000/news/{news.get("pk")}')
                news_from_each_category.append(new)
            print("Письма отправлены подписчикам категории:", category.id, category.name)
            for qaz in news_from_each_category:
                print(qaz)

            qwe = category.subscribers.all()
            for wsx in qwe:
                print('Новости отправлены на', wsx.email)

        return render(request, 'test_test.html', {
            'pole_test_html': pole_test,
            'pole_test_html2': pole_test2,
            "pole_spisok_html1": pole_spisok1,
            "pole_spisok_html2": pole_spisok2,
        })


