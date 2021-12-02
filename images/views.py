from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Image
from .serializers import ImageSerializer
from django.http import HttpResponse
from urllib.parse import urlparse
import os
import requests
from django.core.files import File
from PIL import Image as ImagePIL


class ImageView(APIView):
    def get(self, request, pk=None):
    	if pk:
    		# Вывод конкретного изображение по ключу.
    		image = Image.objects.get(id=pk)
    		serializer = ImageSerializer(image, context={"request": request})
    		return Response({'image': serializer.data})
    	else:
    		# Вывод списка всех изображений.
	        images = Image.objects.all()
	        serializer = ImageSerializer(images, many=True, context={"request": request})
	        return Response({'images': serializer.data})

    def post(self, request):
    	# Загрузка изображения с компьютера пользователя.
    	if request.data.get('file'):
	    	image = Image.objects.create(picture=request.data.get('file'))
	    	serializer = ImageSerializer(image, context={"request": request})
	    	return Response({'image': serializer.data})

	    # Загрузка изображения по ссылке.
    	elif request.data.get('url'):
    		r = requests.get(request.data.get('url'))
    		filename = os.path.basename(urlparse(request.data.get('url')).path)
    		with open(filename, 'wb') as picture:
    			picture.write(r.content)

    		picture_file = open(filename, 'rb')
    		picture = File(picture_file)
    		image = Image.objects.create(picture=picture, url=request.data.get('url'))
    		picture.close()
    		os.remove(filename)

	    	serializer = ImageSerializer(image, context={"request": request})
	    	return Response({'image': serializer.data})


    	else:
    		return HttpResponse('Вы не загрузили файл или ссылку на файл', status=400)

    def delete(self, request, pk):
    	image = Image.objects.get(id=pk)
    	image.delete()

    	return HttpResponse('Изображение удалено', status=200)


class ImageResizeView(APIView):
	# Создание нового изображение с измененными размерами.
	def post(self, request, pk):
		height = request.data.get('height')
		width = request.data.get('width')

		if not height or not width:
			return HttpResponse('Некорректный запрос', status=400)


		parent_image = Image.objects.get(id=pk)
		original_picture = ImagePIL.open(parent_image.picture.url[1:])
		resized_picture = original_picture.resize((int(width), int(height)))
		basename = parent_image.picture.name.split('.')[0]
		extension = parent_image.picture.name.split('.')[1]
		resized_picture_name = f'{basename}_{width}_{height}.{extension}'
		resized_picture.save(resized_picture_name)
		picture_file = open(resized_picture_name, 'rb')
		picture = File(picture_file)
		image = Image.objects.create(picture=picture, parent_picture=parent_image.id)
		picture_file.close()
		os.remove(resized_picture_name)
		serializer = ImageSerializer(image, context={"request": request})
		return Response({'image': serializer.data})












