from datacenter.models import Mark, Schoolkid, Chastisement, Lesson, Commendation
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import random


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2,3])
    desired_evaluations = input('У вас ' + str(bad_marks.count()) + ' плохих оценок. На какую оценку вы хотели бы их исправить?\r\n')
    if desired_evaluations == '4' or desired_evaluations == '5':
        Mark.objects.filter(schoolkid=schoolkid, points__in=[2,3]).update(points=desired_evaluations)
        return 'Поздравляем, вы успешно исправили все плохие оценки. Учитесь хорошо!'
    else:
        print('Некорректное значение. Введите желаемую оценку: 4 или 5')

def remove_chastisements(schoolkid):
    all_chistisements = Chastisement.objects.filter(schoolkid=schoolkid)
    all_chistisements.delete()
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
        child = Schoolkid.objects.get(full_name__contains = full_name)
    except ObjectDoesNotExist:
        return 'Такого ученика нет в базе данных'
    except MultipleObjectsReturned:
        return 'Слишком много совпадений, уточните поиск'

    lessons = Lesson.objects.filter(year_of_study = child.year_of_study, group_letter = child.group_letter, subject__title__contains = subject_title).order_by('-date')
    Commendation.objects.create(text=random.choice(commendations), created = lessons.first().date, schoolkid = child, subject = lessons.first().subject, teacher = lessons.first().teacher)
    return 'похвала успешно добавлена'

