from django.db import models

class BaseModel(models.Model):
    """
    Bu abstract model boshqa modellar uchun asos bo'lib xizmat qiladi.
    U har bir yozuvning yaratilgan va yangilangan vaqtini avtomatik ravishda saqlaydi.
    """

    # Yozuv qachon yaratilganligini saqlaydi
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    # Yozuv oxirgi marta qachon yangilanganligini saqlaydi
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")

    class Meta:
        abstract = True  # Bu modelni abstract qiladi, ya'ni ma'lumotlar bazasiga jadval yaratilmaydi
        ordering = ['-created_at']  # Yozuvlarni yaratilgan vaqt bo'yicha teskari tartibda saralash

# from django.db import models
#
# class BaseModel(models.Model):
#     """
#     Bu abstract model boshqa modellar uchun asos bo'lib xizmat qiladi.
#     U har bir yozuvning yaratilgan va yangilangan vaqtini avtomatik ravishda saqlaydi.
#     """
#
#     # Yozuv qachon yaratilganligini saqlaydi
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
#
#     # Yozuv oxirgi marta qachon yangilanganligini saqlaydi
#     updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")
#
#     class Meta:
#         abstract = True  # Bu modelni abstract qiladi, ya'ni ma'lumotlar bazasiga jadval yaratilmaydi
#         ordering = ['-created_at']  # Yozuvlarni yaratilgan vaqt bo'yicha teskari tartibda saralash
#
#     def __str__(self):
#         """
#         Modelning string ko'rinishi. Masalan, admin panelda yoki shell-da ko'rinadi.
#         """
#         return f"{self.__class__.__name__} (Yaratilgan: {self.created_at}, Yangilangan: {self.updated_at})"
#
#     def save(self, *args, **kwargs):
#         """
#         Yozuvni saqlashdan oldin qo'shimcha amallar bajarish uchun.
#         """
#         # Misol uchun, saqlashdan oldin ma'lumotlarni tekshirish yoki o'zgartirish
#         super().save(*args, **kwargs)  # Asosiy save metodini chaqiramiz
#
#     @classmethod
#     def get_recent_records(cls, days=30):
#         """
#         So'nggi berilgan kunlar davomida yaratilgan yozuvlarni qaytaradi.
#         """
#         from django.utils import timezone
#         return cls.objects.filter(created_at__gte=timezone.now() - timezone.timedelta(days=days))
#
#     @property
#     def is_recent(self):
#         """
#         Yozuv so'nggi 7 kun ichida yaratilgan bo'lsa, True qaytaradi.
#         """
#         from django.utils import timezone
#         return (timezone.now() - self.created_at).days <= 7