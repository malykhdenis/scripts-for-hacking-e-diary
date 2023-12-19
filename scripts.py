import random
from typing import Optional

from datacenter.models import (Schoolkid, Lesson, Mark, Chastisement,
                               Commendation)

COMMENDATION_CHOICES = [
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!',
]


def fix_marks(schoolkid_name: str) -> None:
    """Fix all bad marks for schoolkid."""
    wanted_mark = 5
    if not check_schoolkid(schoolkid_name):
        return
    Mark.objects.filter(
        schoolkid__full_name__contains=schoolkid_name,
        points__lt=4
    ).update(points=wanted_mark)


def remove_chastisements(schoolkid_name: str) -> None:
    """Delete all chastisiments for schoolkid."""
    if not check_schoolkid(schoolkid_name):
        return
    Chastisement.objects.filter(
        schoolkid__full_name__contains=schoolkid_name).delete()


def create_commendation(schoolkid_name: str, subject: str) -> None:
    """Create a commendation for schoolkid for defined subject."""
    schoolkid = check_schoolkid(schoolkid_name)
    if not schoolkid:
        return
    last_lesson = (
        Lesson.objects.filter(
            year_of_study=schoolkid.year_of_study,
            group_letter=schoolkid.group_letter,
            subject__title=subject
        ).order_by('date').last()
    )
    if not last_lesson:
        print('Не удалось найти урок.')
        return
    Commendation.objects.create(
        text=random.choice(COMMENDATION_CHOICES),
        created=last_lesson.date,
        schoolkid=schoolkid,
        subject=last_lesson.subject,
        teacher=last_lesson.teacher
    )


def check_schoolkid(schoolkid_name: str) -> Optional[Schoolkid]:
    """Checking existing of single schoolkid."""
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except Schoolkid.DoesNotExist:
        print('Ученик не найден.')
        return False
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено несколько учеников с таким именем.')
        return False
    else:
        return schoolkid
