from django.core.signing import Signer
import uuid  # Import the UUID library to generate unique table names
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import time
from datetime import datetime
import mysql.connector
import json
from .models import SigninUser
from django.contrib.auth import authenticate, login

from django.urls import reverse
from django.http import HttpRequest
from .models import Contact  # Rename the model class to Contact


def home(request):
    return render(request, 'home.html')


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
    
        if name and email and message:
            user = Contact(name=name, email=email, message=message)  # Create a Contact object
            user.save()
            return render(request, 'contact.html')

    return render(request, 'contact.html')


def chart(request):
    return render(request, 'chart.html')
from django.shortcuts import render
from .models import SigninUser  # Import your SigninUser model

def private_dashboard(request, table_name):
    remember_me_cookie = request.COOKIES.get('remember_me')
    if remember_me_cookie:
        username = remember_me_cookie.split(':')[0]
        user_value = SigninUser.objects.filter(username=username).first()
    else:
        user_value = None  

    return render(request, 'private_dashboard.html', {'user_value': user_value})


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        uploaded_image = request.FILES.get('image')  # Correctly get the uploaded image file

        if username and name and email and password and uploaded_image:
            user = SigninUser(username=username, name=name, email=email, password=password, image=uploaded_image)
            user.save()
            return render(request, 'signin.html')
    return render(request, 'signup.html')


# <<<<<<< start <<<<<<<<<<<<<< the all sigin user checking exsistig or user creation  >>>>>>>>>>>>>>>>>>>>>>>>>>

def get_last_sequence_number():
    try:
        with open("last_sequence_number.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def update_last_sequence_number(sequence_number):
    with open("last_sequence_number.txt", "w") as file:
        file.write(str(sequence_number))


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('rememberme')

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='newuser',
                password='newpassword',
                database='mydb1',
                port=3306,
            )
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            obj = {
                'Username': username,
                'CurrentTime': current_time,
                'Temperature': random.uniform(90.0, 120.0),
                'Heartbeat': random.randint(60, 100),
                'SpO2': random.randint(90, 100),
                'RBC': random.uniform(4.0, 6.5),
                'WBC': random.uniform(4.0, 11.0),
                'Platelets': random.uniform(150.0, 450.0),
                'BloodGlucose': random.uniform(70, 140),
                'HbConcentration': random.uniform(12.0, 16.0),
                'RespirationRate': random.randint(12, 20),
                'SleepMonitoring': random.choice(['Awake', 'Light Sleep', 'Deep Sleep']),
                'StepCount': random.randint(1000, 10000),
                'MovementData': random.choice(['Sedentary', 'Light Activity', 'Moderate Activity', 'High Activity'])
            }
            cursor = conn.cursor()

            last_sequence_number = get_last_sequence_number()
            sequence_number = last_sequence_number + 1
            unique_table_name = f"user_data_{sequence_number}"
            update_last_sequence_number(sequence_number)
            
            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {unique_table_name} (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                Username VARCHAR(255),
                CurrentTime DATETIME,
                Temperature FLOAT,
                Heartbeat INT,
                SpO2 INT,
                RBC FLOAT,
                WBC FLOAT,
                Platelets FLOAT,
                BloodGlucose FLOAT,
                HbConcentration FLOAT,
                RespirationRate INT,
                SleepMonitoring VARCHAR(255),
                StepCount INT,
                MovementData VARCHAR(255)
                    );
                """)
            insert_query = f"""
                INSERT INTO {unique_table_name} (
                    Username, CurrentTime, Temperature, Heartbeat, SpO2, RBC, WBC, Platelets,
                    BloodGlucose, HbConcentration, RespirationRate, SleepMonitoring, StepCount, MovementData
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            values = (
               obj['Username'],  current_time, obj['Temperature'], obj['Heartbeat'], obj['SpO2'], obj['RBC'], obj['WBC'], obj['Platelets'],
                obj['BloodGlucose'], obj['HbConcentration'], obj['RespirationRate'], obj['SleepMonitoring'],
                obj['StepCount'], obj['MovementData']
            )
            cursor.execute(insert_query, values)
            conn.commit()
            conn.close()
        
        except mysql.connector.Error as e:
            return JsonResponse({'error': str(e)})
        
        all_users = SigninUser.objects.all()
        user_found = False

        for user in all_users:
            if user.username == username:
                user_found = True
                if user.password == password:
                    if remember_me:
                        signer = Signer()
                        signed_username = signer.sign(username)
                        response = HttpResponseRedirect('private_dashboard')
                        url = reverse('private_dashboard',
                                      args=[unique_table_name])
                        response = HttpResponseRedirect(url)

                        # print(url, "++_________________________________________")

                        response.set_cookie('remember_me', signed_username)
                        response.set_cookie('table_name', url)

                        return response
                    else:
                        return render(request, 'private_dashboard.html')
                else:
                    error_message = "Incorrect password. Please try again."
                    return render(request, 'signin.html', {'error_message': error_message})

        if not user_found:
            error_message = "User not found. Please sign up."
            return render(request, 'signin.html', {'error_message': error_message})

    remember_me_cookie = request.COOKIES.get('remember_me')

    if remember_me_cookie:
        table_name_cookie = request.COOKIES.get('table_name')
        value = table_name_cookie.strip('/').split('/')[-1]

        try:
            redirect_url = f'/private_dashboard/{value}/'
            return HttpResponseRedirect(redirect_url)
        except:
            pass
    return render(request, 'signin.html')

# <<<<<< end <<<<<<<<<<<<<<< the all sigin user checking exsistig or user creation >>>>>>>>>>>>>>>>>>>>>>>>>>


def logout(request):
    if 'remember_me' in request.COOKIES:
        response = HttpResponseRedirect('/home')
        response.delete_cookie('remember_me')
        response.delete_cookie('table_name')
        return response
    else:
        return HttpResponseRedirect('/home')

def generate_auto_data(request):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='newuser',
            password='newpassword',
            database='mydb1',
            port=3306,
        )
        original_string = request.COOKIES.get('table_name', None)

        if original_string is not None:
            if original_string.endswith('/'):
                original_string = original_string[:-1]

            parts = original_string.split('&')
            if len(parts) > 1:
                unique_table_name = parts[1]

            select_query = f"""
            SELECT * FROM {unique_table_name}
            ORDER BY ID DESC
            LIMIT 7
            """
            cursor = conn.cursor(dictionary=True)
            cursor.execute(select_query)
            latest_data_list = cursor.fetchall()
            return JsonResponse({'latest_data_list': latest_data_list}, json_dumps_params={'indent': 4})
        else:
            return JsonResponse({'error': 'table_name cookie not found'}, status=400)
    except mysql.connector.Error as e:
        return JsonResponse({'error': str(e)})







@csrf_exempt
def generate_and_insert_data(request):
    username = ""
    if request.method == 'POST' or request.method == 'GET':
        username = request.POST.get('username')
        try:
            remember_me_cookie = request.COOKIES.get('remember_me')

            if not remember_me_cookie:
                return JsonResponse({'error': 'User not authenticated'}, status=401)

            signer = Signer()
            username = signer.unsign(remember_me_cookie)

            conn = mysql.connector.connect(
                host='localhost',
                user='newuser',
                password='newpassword',
                database='mydb1',  # Use the common database
                port=3306,
            )

            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            obj = {
                'Username': username,
                'CurrentTime': current_time,
                'Temperature': random.uniform(90.0, 120.0),
                'Heartbeat': random.randint(60, 100),
                'SpO2': random.randint(90, 100),
                'RBC': random.uniform(4.0, 6.5),
                'WBC': random.uniform(4.0, 11.0),
                'Platelets': random.uniform(150.0, 450.0),
                'BloodGlucose': random.uniform(70, 140),
                'HbConcentration': random.uniform(12.0, 16.0),
                'RespirationRate': random.randint(12, 20),
                'SleepMonitoring': random.choice(['Awake', 'Light Sleep', 'Deep Sleep']),
                'StepCount': random.randint(1000, 10000),
                'MovementData': random.choice(['Sedentary', 'Light Activity', 'Moderate Activity', 'High Activity'])
            }
            original_string = request.COOKIES.get('table_name', None)

            if original_string.endswith('/'):
                original_string = original_string[:-1]

            parts = original_string.split('&')
            if len(parts) > 1:
                unique_table_name = parts[1]

            if not unique_table_name:
                return JsonResponse({'error': 'User not authenticated'}, status=401)

            insert_query = f"""
                INSERT INTO {unique_table_name} (
                    Username, CurrentTime, Temperature, Heartbeat, SpO2, RBC, WBC, Platelets,
                    BloodGlucose, HbConcentration, RespirationRate, SleepMonitoring, StepCount, MovementData
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """

            values = (
                obj['Username'], current_time, obj['Temperature'], obj['Heartbeat'], obj['SpO2'], obj['RBC'], obj['WBC'], obj['Platelets'],
                obj['BloodGlucose'], obj['HbConcentration'], obj['RespirationRate'], obj['SleepMonitoring'],
                obj['StepCount'], obj['MovementData']
            )

            cursor = conn.cursor()
            cursor.execute(insert_query, values)
            conn.commit()
            response_data = {
                'message': 'Data generated and inserted successfully',
                'generated_data': obj
            }
            return JsonResponse(response_data, json_dumps_params={'indent': 4})

        except mysql.connector.Error as e:
            return JsonResponse({'error': str(e)})

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)





def print(request):
    return render(request, 'print_insight.html')





# import json
# import requests
# from django.shortcuts import render
# from django.http import HttpResponseServerError

# def print(request):
#     # Make a GET request to the API URL
#     api_url = "http://127.0.0.1:8000/generate_auto_data/"
#     response = requests.get(api_url)

#     if response.status_code == 200:

#         try:
#             data = json.loads(response.text)
#             latest_data_list = data.get("latest_data_list", [])
#         except json.JSONDecodeError as e:
#             return HttpResponseServerError("Error decoding JSON data: " + str(e))
#     else:
#         latest_data_list = []

#     return render(request, "print_insight.html", {"latest_data_list": latest_data_list})