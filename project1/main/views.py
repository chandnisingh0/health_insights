from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import time
from datetime import datetime
import mysql.connector
import json

# Create your views here.

def homepage(request):
    return render(request,'home.html')

def chart(request):
    return render(request,'chart.html') 

from django.shortcuts import render

from django.http import JsonResponse

def generate_auto_data(request):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='newuser',
            password='newpassword',
            database='mydb',
            port=3306,
        )
        
        select_query = """
        SELECT * FROM health_data
        ORDER BY ID DESC
        LIMIT 10
        """
        cursor = conn.cursor(dictionary=True)
        cursor.execute(select_query)
        latest_data_list = cursor.fetchall()
        # print(latest_data_list)
        # return JsonResponse({'latest_data_list': latest_data_list})
        return JsonResponse({'latest_data_list': latest_data_list}, json_dumps_params={'indent': 4})  # Return the generated data
    except mysql.connector.Error as e:
        return JsonResponse({'error': str(e)})

@csrf_exempt
def generate_and_insert_data(request):
    if request.method == 'POST' or request.method == 'GET':
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='newuser',
                password='newpassword',
                database='mydb',
                port=3306,
            )
            
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            obj = {
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

            current_time = obj['CurrentTime']
            temperature = obj['Temperature']
            heartbeat = obj['Heartbeat']
            spo2 = obj['SpO2']
            rbc = obj['RBC']
            wbc = obj['WBC']
            platelets = obj['Platelets']
            blood_glucose = obj['BloodGlucose']
            hb_concentration = obj['HbConcentration']
            respiration_rate = obj['RespirationRate']
            sleep_monitoring = obj['SleepMonitoring']
            step_count = obj['StepCount']
            movement_data = obj['MovementData']

            insert_query = """
            INSERT INTO health_data (
                CurrentTime, Temperature, Heartbeat, SpO2, RBC, WBC, Platelets,
                BloodGlucose, HbConcentration, RespirationRate, SleepMonitoring, StepCount, MovementData
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """

            values = (
                current_time, temperature, heartbeat, spo2, rbc, wbc, platelets,
                blood_glucose, hb_concentration, respiration_rate, sleep_monitoring, step_count, movement_data
            )

            cursor = conn.cursor()
            cursor.execute(insert_query, values)
            latest_inserted_value = cursor.fetchall()
            conn.commit()
            response_data = {
                            'message': 'Data generated and inserted successfully',
                            'generated_data': obj
                        }
            return JsonResponse(response_data, json_dumps_params={'indent': 4})  # Return the generated data

        except mysql.connector.Error as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
