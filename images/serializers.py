from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Image
		picture = serializers.SerializerMethodField()
		fields = [
		'id',
		'name',
		'url',
		'picture',
		'width',
		'height',
		'parent_picture',
		]

		# Вывод абсолютного пути изображения в response.
		def get_picture(self, obj):
			request = self.context.get('request')
			return request.build_absolute_uri(obj.picture.url)