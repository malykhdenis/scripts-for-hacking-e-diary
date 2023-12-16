import random

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from datacenter.models import (Schoolkid, Lesson, Mark, Chastisement,
                               Commendation)


def fix_marks(schoolkid):
    """Fix all bad marks for schoolkid."""
    wanted_mark = 5
    bad_marks = Mark.objects.filter(schoolkid=schoolkid).filter(points__lt=4)
    for mark in bad_marks:
        mark.points = wanted_mark
        mark.save()


def remove_chastisements(schoolkid):
    """Delete all chastisiments for schoolkid."""
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid, subject):
    """Create a commendation for schoolkid for defined subject."""
    commendation_choices = [
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!',
    ]
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid)
    except ObjectDoesNotExist:
        print(f'{schoolkid} - нет такого ученика.')
    except MultipleObjectsReturned:
        print('Найдено несколько учеников с таким именем.')
    else:
        last_lesson = (
            Lesson.objects
            .filter(year_of_study=schoolkid.year_of_study)
            .filter(group_letter=schoolkid.group_letter)
            .filter(subject__title=subject)
            .order_by('date').last()
        )
        Commendation.objects.create(
            text=random.choice(commendation_choices),
            created=last_lesson.date,
            schoolkid=schoolkid,
            subject=last_lesson.subject,
            teacher=last_lesson.teacher
        )
