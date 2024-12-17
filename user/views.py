from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import College
import os
import google.generativeai as genai
from django.conf import settings
import json
from .forms import ExpenseCalculatorForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now



# Create your views here[
# def home(request):
#     return render(request,'home.html')
def home(request):
    return render(request,'Landing/main.html')
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username,password = password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Credentials not matches....Try again....')
            return redirect('login')
    return render(request,'Auth/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email = email).exists():
                messages.info(request,'Email already exists.....Try to login')
            elif User.objects.filter(username = username).exists():
                messages.info(request,'Username already exits....Try to user anotherone')
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                return redirect('login')
            
        else:
            messages.info(request,"Password doesn't match.....")
            return redirect('register')
    return render(request,'Auth/register.html')
def college(request):
    query = request.GET.get('q', '')
    if query:
        colleges = College.objects.filter(name__icontains=query) | College.objects.filter(country__icontains=query)
    else:
        colleges = College.objects.all()
    return render(request,'College/college.html',{'colleges': colleges})
def chatBot(request):
    response_text = None
    if request.method == "POST":
        try: 
            data = json.loads(request.body)
            user_input = data.get("user_input", "")
            # user_input = request.POST.get("user_input")
            print(user_input)
            generation_config = {
                "temperature": 1,
                "top_p":0.95,
                "top_k":40,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }
            model = genai.GenerativeModel(
                model_name="gemini-2.0-flash-exp",
                generation_config=generation_config,
            )
            chat_session = model.start_chat(history=[])
            si = """
            You are an expert in asking mock question for different examination.

            Your only text response must be a HTML.
            donot involve '''html'''
            Example :

            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Document</title>
            </head>
            <body>
                
            </body>
            </html>
            """

            response = chat_session.send_message(si+'Can you ask me some mock question(MCQ and theory question mixed and alos provide the answer of the following) to prepare me for this exam/topic'+user_input)
    
            response_text = response.text
            print(response)
            return JsonResponse({"response_text": response_text}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return render(request,'Chatbot/chatBot.html') 

def expense(request):
    total_expenses = None
    country_data = None
    total_living_cost = 0

    if request.method == 'POST':
        form = ExpenseCalculatorForm(request.POST)
        if form.is_valid():
            country_name = form.cleaned_data['country']
            tuition_fees = form.cleaned_data['tuition_fees']

            
            with open(r'C:\Users\Sagnik\OneDrive\Desktop\PROJECTS\scholarship\static\country_expenses.JSON', 'r') as file:
                data = json.load(file)
                
                country_data = next((item for item in data['countries'] if item['country'] == country_name), None)
            
            if country_data:
                
                total_living_cost = sum(country_data['living_cost'].values())  
                travel_expense = country_data['travel_expense']
                total_expenses = total_living_cost*12*4 + travel_expense*2*4 + tuition_fees
    else:
        form = ExpenseCalculatorForm()

    return render(request, 'Expense/expense.html', {
        'form': form,
        'total_expenses': total_expenses,
        'country_data': country_data,
        'total_living_cost': total_living_cost,
    })
    


def aiInterview(request):
    return render(request,'Chatbot/chatBot.html')

# views.py
def studyplanner(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_input = data.get("user_input", {})

            
            topic = user_input.get("topic", "")
            time = user_input.get("time", "")
            print(topic, time)

            
            if not topic or not time:
                return JsonResponse({"error": "Both topic and time are required."}, status=400)

            
            generation_config = {
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }
            
            model = genai.GenerativeModel(
                model_name="gemini-2.0-flash-exp",
                generation_config=generation_config,
            )
            chat_session = model.start_chat(history=[])
            si = """
            You are an expert in planning rountine and roadmap.
            
            Your  response must be a HTML.
            Do not include '''html'''
            Example:
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Document</title>
            </head>
            <body>
                
            </body>
            </html>
            """

            
            response = chat_session.send_message(si + f"Can you provide me a roadmap to prepare for this topic '{topic}' in {time} days?")
            response_text = response.text  

            return JsonResponse({"response_text": response_text}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    
    return render(request, 'studyPlanner/studyplanner.html')


def visa(request):
    response_text = None
    if request.method == "POST":
        try: 
            data = json.loads(request.body)
            user_input = data.get("user_input", "")
            # user_input = request.POST.get("user_input")
            print(user_input)
            generation_config = {
                "temperature": 1,
                "top_p":0.95,
                "top_k":40,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }
            model = genai.GenerativeModel(
                model_name="gemini-2.0-flash-exp",
                generation_config=generation_config,
            )
            chat_session = model.start_chat(history=[])
            si = """
            You are an expert in guiding user for getting VISA.

            Your only text response must be a HTML.
            donot involve '''html'''
            Example :

            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Document</title>
            </head>
            <body>
                
            </body>
            </html>
            """

            response = chat_session.send_message(si+user_input)
    
            response_text = response.text
            print(response)
            return JsonResponse({"response_text": response_text}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return render(request,'visaGuidance/visa.html')
def scholarship(request):
    response_text = None
    if request.method == "POST":
        try: 
            data = json.loads(request.body)
            user_input = data.get("user_input", "")
            # user_input = request.POST.get("user_input")
            print(user_input)
            generation_config = {
                "temperature": 1,
                "top_p":0.95,
                "top_k":40,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }
            model = genai.GenerativeModel(
                model_name="gemini-2.0-flash-exp",
                generation_config=generation_config,
            )
            chat_session = model.start_chat(history=[])
            si = """
            You are an expert in guiding user for getting scholarship.

            Your only text response must be a HTML.
            donot involve '''html'''
            Example :

            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Document</title>
            </head>
            <body>
                
            </body>
            </html>
            """

            response = chat_session.send_message(si+"can you provide any available scholarship for this university"+user_input)
    
            response_text = response.text
            print(response)
            return JsonResponse({"response_text": response_text}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return render(request,'scholarship/scholarship.html')