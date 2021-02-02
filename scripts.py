import random

from datacenter.models import Mark
from datacenter.models import Schoolkid
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Commendation
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def fix_marks(schoolkid, desired_evaluations):
    try:
        Mark.objects.filter(schoolkid=schoolkid,
                            points__in=[2, 3]).get()
    except ObjectDoesNotExist:
        return 'Поздравляем! У вас нет ни одной плохой оценки!'
    except MultipleObjectsReturned:
        Mark.objects.filter(schoolkid=schoolkid,
                            points__in=[2, 3])

    if desired_evaluations == 4 or desired_evaluations == 5:
        Mark.objects.filter(
            schoolkid=schoolkid,
            points__in=[2, 3]).update(points=desired_evaluations)

        return 'Поздравляем, вы успешно исправили все плохие оценки.\
                Учитесь хорошо!'
    else:
        return 'Введено неверное значение, попробуйте ввести 4 или 5'


def remove_chastisements(schoolkid):
    try:
        chistisements = Chastisement.objects.filter(schoolkid=schoolkid).get()
        chistisements.delete()
    except ObjectDoesNotExist:
        return 'Замечания не найдены. Вы молодец!'
    except MultipleObjectsReturned:
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
        return 'Такого ученика нет в базе данных. \
                Попробуйте ввести запрос по-другому'
    except MultipleObjectsReturned:
        return 'Слишком много совпадений, уточните поиск'

    try:
        lesson = Lesson.objects.get(
            year_of_study=child.year_of_study,
            group_letter=child.group_letter,
            subject__title__contains=subject_title)
    except Lesson.DoesNotExist:
        return 'Такого предмета не существует. Попробуйте ввести по-другому'
    except MultipleObjectsReturned:
        lesson = Lesson.objects.filter(
            year_of_study=child.year_of_study,
            group_letter=child.group_letter,
            subject__title__contains=subject_title).order_by('-date').first()

    Commendation.objects.create(
        text=random.choice(commendations),
        created=lesson.date,
        schoolkid=child,
        subject=lesson.subject,
        teacher=lesson.teacher)
    return 'похвала успешно добавлена'
