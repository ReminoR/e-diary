import random

from datacenter.models import (
    Mark,
    Schoolkid,
    Chastisement,
    Lesson,
    Commendation)
from django.core.exceptions import MultipleObjectsReturned


def fix_marks(schoolkid, point):
    if point not in [4, 5]:
        return 'Введено неверное значение, попробуйте ввести 4 или 5'

    if Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).exists():
        Mark.objects.filter(schoolkid=schoolkid,
                            points__in=[2, 3]).update(points=point)
        return ('Поздравляем, вы успешно исправили все плохие оценки.'
                'Учитесь хорошо!')
    else:
        return 'Поздравляем! У вас нет ни одной плохой оценки!'


def remove_chastisements(schoolkid):
    chistisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chistisements.delete()
    return 'Все замечания успешно удалены'


def create_commendation(full_name, subject_title):
    commendations = [
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!',
        'Великолепно!',
        'Прекрасно!',
        'Ты меня очень обрадовал!',
        'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!',
        'Ты, как всегда, точен!',
        'Очень хороший ответ!',
        'Талантливо!',
        'Ты сегодня прыгнул выше головы!',
        'Я поражен!',
        'Уже существенно лучше!',
        'Потрясающе!',
        'Замечательно!',
        'Прекрасное начало!',
        'Так держать!',
        'Ты на верном пути!',
        'Здорово!',
        'Это как раз то, что нужно!',
        'Я тобой горжусь!',
        'С каждым разом у тебя получается всё лучше!',
        'Мы с тобой не зря поработали!',
        'Я вижу, как ты стараешься!',
        'Ты растешь над собой!',
        'Ты многое сделал, я это вижу!',
        'Теперь у тебя точно все получится!',
    ]

    try:
        child = Schoolkid.objects.get(full_name__contains=full_name)
    except Schoolkid.DoesNotExist:
        return ('Такого ученика нет в базе данных.'
                'Попробуйте ввести запрос по-другому')
    except MultipleObjectsReturned:
        return 'Слишком много совпадений, уточните поиск'

    try:
        lesson = Lesson.objects.filter(
            year_of_study=child.year_of_study,
            group_letter=child.group_letter,
            subject__title__contains=subject_title).order_by('-date').first()
    except Lesson.DoesNotExist:
        return 'Такого предмета не существует. Попробуйте ввести по-другому'

    Commendation.objects.create(
        text=random.choice(commendations),
        created=lesson.date,
        schoolkid=child,
        subject=lesson.subject,
        teacher=lesson.teacher)
    return 'похвала успешно добавлена'
