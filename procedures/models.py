from datetime import date

from django.db import models

from users.models import User


class Procedure(models.Model):
    """Процедура"""
    xml_type = models.CharField("Корневой каталог", max_length=100, null=True)
    purchaseNumber = models.CharField("Лот", max_length=20, default='')
    docPublishDate = models.DateField("Дата публикации", default=date.today, )
    purchaseObjectInfo = models.CharField("Информация", max_length=100, default='')
    regNum = models.CharField("Код организации", max_length=12, default='')
    fullName = models.CharField("Наименование организации", max_length=250, default='')
    maxPrice = models.PositiveIntegerField("Бюджет", default=0, help_text="указывать сумму в рублях")
    curator = models.ForeignKey(
        User, verbose_name="Куратор", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        db_table = "t_procedures"
        verbose_name = "Лот"
        verbose_name_plural = "Лоты"
