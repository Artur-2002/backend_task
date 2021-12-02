from django.db import models
import os
from django.dispatch import receiver

# Create your models here.

class Image(models.Model):
	url = models.URLField(max_length=400, null=True, verbose_name='Ссылка', blank=True)
	picture = models.ImageField(upload_to='', verbose_name='Фотография')
	parent_picture = models.PositiveIntegerField(verbose_name='Исходная фотография', null=True, blank=True)

	class Meta:
		verbose_name = 'Изображение'
		verbose_name_plural = 'Изображения'

	@property
	def name(self):
		return self.picture.name

	@property
	def width(self):
		return self.picture.width

	@property
	def height(self):
		return self.picture.height

	def __str__(self):
		return str(self.id)

# Удаление изображения с диска в случае удаления экземпляра класса из базы данных.
@receiver(models.signals.post_delete, sender=Image)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.picture:
        if os.path.isfile(instance.picture.path):
            os.remove(instance.picture.path)