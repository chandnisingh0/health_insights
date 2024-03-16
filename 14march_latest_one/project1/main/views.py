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

from .models import NutritionModel
from .models import MealInstructionModel


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



def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        veg_nonveg = request.POST.get('veg_nonveg')
        state = request.POST.get('state')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        uploaded_image = request.FILES.get('image')

        # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(password)


        # if username and name and email and password and uploaded_image:
        if username and name and email and password:
            try:
                conn = mysql.connector.connect(
                    host='localhost',
                    user='newuser',
                    password='newpassword',
                    database='mydb1',
                    port=3306,
                )
                cursor = conn.cursor()

                # Create a table for the new user during signup
                unique_table_name = f"user_data_{username.lower()}"
                create_table_query = f"""
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
                """
                cursor.execute(create_table_query)

                # Save user details in the SigninUser model
                user = SigninUser(
                        username=username,
                        name=name,
                        email=email,
                        password=password,
                        gender=gender,
                        age=age,
                        height=height,
                        weight=weight,
                        veg_nonveg=veg_nonveg,
                        state=state,
                        phone=phone,
                        dob=dob,
                        uploaded_image=uploaded_image
                    )

                user.save()

                conn.commit()
                conn.close()

                return render(request, 'signin.html')

            except mysql.connector.Error as e:
                return JsonResponse({'error': str(e)})

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

        all_users = SigninUser.objects.all()
        user_found = False

        for user in all_users:
            if user.username == username:
                user_found = True
                if user.password == password:
                    if remember_me:
                        signer = Signer()
                        signed_username = signer.sign(username)
                        response = HttpResponseRedirect('profile')
                        url = reverse('profile', args=[f"user_data_{username.lower()}"])
                        response = HttpResponseRedirect(url)

                        response.set_cookie('remember_me', signed_username)
                        response.set_cookie('table_name', url)

                        return response
                    else:
                        return render(request, 'profile.html')
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
            redirect_url = f'/profile/{value}/'
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

def print_insight(request):
    return render(request, 'print_insight.html')

# -----------------------dashboard---------------------
def chart(request, table_name):
    remember_me_cookie = request.COOKIES.get('remember_me')
    if remember_me_cookie:
        username = remember_me_cookie.split(':')[0]
        user_value = SigninUser.objects.filter(username=username).first()
    else:
        user_value = None  

    return render(request, 'dashboard/chart.html', {'user_value': user_value})



def profile(request, table_name):
    remember_me_cookie = request.COOKIES.get('remember_me')
    if remember_me_cookie:
        username = remember_me_cookie.split(':')[0]
        user_value = SigninUser.objects.filter(username=username).first()
    else:
        user_value = None  

    return render(request, 'dashboard/profile.html', {'user_value': user_value})


def nutrient_calculator(request, table_name):
    remember_me_cookie = request.COOKIES.get('remember_me')
    if remember_me_cookie:
        username = remember_me_cookie.split(':')[0]
        user_value = SigninUser.objects.filter(username=username).first()
    else:
        user_value = None  
    return render(request, 'dashboard/NutrientCalculator.html', {'user_value': user_value})

def fitness_health(request, table_name):
    remember_me_cookie = request.COOKIES.get('remember_me')
    if remember_me_cookie:
        username = remember_me_cookie.split(':')[0]
        user_value = SigninUser.objects.filter(username=username).first()
    else:
        user_value = None  
    return render(request, 'dashboard/Fitness_health.html', {'user_value': user_value})

def recent_start(request, table_name):
    remember_me_cookie = request.COOKIES.get('remember_me')
    if remember_me_cookie:
        username = remember_me_cookie.split(':')[0]
        user_value = SigninUser.objects.filter(username=username).first()
    else:
        user_value = None  
    return render(request, 'dashboard/recent_start.html', {'user_value': user_value})

def settings(request, table_name):
    remember_me_cookie = request.COOKIES.get('remember_me')
    if remember_me_cookie:
        username = remember_me_cookie.split(':')[0]
        user_value = SigninUser.objects.filter(username=username).first()
    else:
        user_value = None  
    return render(request, 'dashboard/settings.html', {'user_value': user_value})

def check_benefits(request, table_name):
    remember_me_cookie = request.COOKIES.get('remember_me')
    if remember_me_cookie:
        username = remember_me_cookie.split(':')[0]
        user_value = SigninUser.objects.filter(username=username).first()
    else:
        user_value = None  
    return render(request, 'dashboard/check_benefits.html', {'user_value': user_value})

def reports(request, table_name):
    remember_me_cookie = request.COOKIES.get('remember_me')
    if remember_me_cookie:
        username = remember_me_cookie.split(':')[0]
        user_value = SigninUser.objects.filter(username=username).first()
    else:
        user_value = None  
    return render(request, 'dashboard/reports.html', {'user_value': user_value})

# recent_start
# settings
# course> check_benefits> benefits about health > video type
# file > reports

def simple_nutrition(request, table_name):
    remember_me_cookie = request.COOKIES.get('remember_me')
    if remember_me_cookie:
        username = remember_me_cookie.split(':')[0]
        user_value = SigninUser.objects.filter(username=username).first()
        # Assuming age is a field in your SigninUser model
        age = user_value.age
        
        # Check if age is a numeric value
        try:
            age_numeric = int(age)
            
            # Query the model using the numeric value
            nutritional_data = NutritionModel.objects.filter(age_group__icontains=age_numeric).first()
        except ValueError:
            nutritional_data = None
    else:
        user_value = None  
        nutritional_data = None

    return render(request, 'dashboard/simple_nutrition.html', {'user_value': user_value, 'nutritional_data': nutritional_data})


def required_meal(request, table_name):
    remember_me_cookie = request.COOKIES.get('remember_me')
    if remember_me_cookie:
        username = remember_me_cookie.split(':')[0]
        user_value = SigninUser.objects.filter(username=username).first()

        if user_value:
            age = user_value.age

            try:
                age_numeric = int(age)

                # Query the model using the numeric value
                required_meal = MealInstructionModel.objects.filter(required_meal_age__icontains=age_numeric).first()
            except ValueError:
                required_meal = None
        else:
            required_meal = None
    else:
        user_value = None
        required_meal = None

    return render(request, 'dashboard/required_meal.html', {'user_value': user_value, 'required_meal': required_meal})