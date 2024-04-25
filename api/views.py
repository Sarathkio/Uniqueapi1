
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Api_data
from django.core.validators import validate_email
from rest_framework.decorators import api_view




def register_fun(request):
    if request.method == 'POST':
        user_name = request.POST['name']
        user_age = request.POST['age']
        user_email = request.POST['txtMail']

        # Validating the valus
        if user_name == '':
            return render(request,'login.html',{'message': 'Use Proper username and password'})
        else:
            data = Api_data( name=user_name, age=user_age, email=user_email)
            # data.save()
            return redirect('reg')
    else:
        return render(request,'login.html',{'message1': 'Saved Successfully'})


def read_fun(request):
    if request.method == 'GET':
        # Fetch all data objects from the Data model
        data_objects = Api_data.objects.all().values()


        # Return a JsonResponse with the data_objects
        return JsonResponse(list(data_objects), safe=False)

@csrf_exempt
def merge_data(request):
    if request.method == 'POST':
        try:
            # Parse the JSON payload from the request body
            data_objects = json.loads(request.body)

            # Validate each data object in the JSON payload
            for obj in data_objects:
                if 'name' not in obj or 'age' not in obj or 'email' not in obj:
                    return JsonResponse({'message': 'Each data object must contain name, age, and email fields'},
                                        status=400)
                if not isinstance(obj['name'], str) or not isinstance(obj['age'], int) or not isinstance(obj['email'],
                                                                                                         str):
                    return JsonResponse({'message': 'Invalid data types for name, age, or email fields'}, status=400)
                if obj['age'] <= 0:
                    return JsonResponse({'message': 'Age must be a positive integer'}, status=400)
                try:
                    validate_email(obj['email'])
                except ValidationError:
                    return JsonResponse({'message': 'Invalid email address format'}, status=400)

            # Save the received data objects to the database
            for obj in data_objects:
                Api_data.objects.create(name=obj['name'], age=obj['age'], email=obj['email'])

            return JsonResponse({'message': 'Data objects successfully merged'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON payload'}, status=400)

    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)


# @api_view(['POST'])
# def update_post(request):
#     name = request.data.get('name')
#     email = request.data.get('email')
#     new_age = request.data.get('age')
#
#     if not name or not email or not new_age:
#         return Response({'error': 'Name, email, and new age are required'}, status=400)
#
#     try:
#         user = User.objects.get(name=name, email=email)
#     except User.DoesNotExist:
#         return Response({'error': 'User not found'}, status=404)
#
#     try:
#         user.age = int(new_age)
#         user.save()
#         return Response({'message': 'User age updated successfully'}, status=200)
#     except ValueError:
#         return Response({'error': 'Invalid age format'}, status=400)
