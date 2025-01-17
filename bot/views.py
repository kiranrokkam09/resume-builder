from django.shortcuts import render
from django.http import JsonResponse
import anthropic
from .models import Chat, Session
from dotenv import load_dotenv
import os
from django.utils import timezone
from datetime import timedelta



load_dotenv()


apikey = os.getenv('API_KEY')

# Create your views here.
client = anthropic.Anthropic(api_key = apikey)

def ask_ai(message,history):
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0.7,
        system=(
            "You are an expert Resume Creator. Guide the user step by step to build a professional resume. "
            "Ask one question at a time, starting with basic contact details, followed by professional summary, "
            "skills, work experience, education, certifications, and additional information. "
            "Ensure each question is clear and concise. Provide a friendly and engaging tone."
            "Only after all sections are completed, output the final resume in html format."
        ),
        messages=[
            {"role": "user", "content": f"{history}"},
            {"role": "user", "content": f"The user answered: {message}. What should we ask next to complete the resume?"}
        ]
    )
    return message.content[0].text

def chat(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        session_id = request.POST.get('session_id')
        session_instance = Session.objects.filter(id = session_id).first()
        history = Chat.objects.filter(session = session_id).values()
        response = ask_ai(message,history)
        Chat.objects.create(session = session_instance, message= message, response=response)
        return JsonResponse({'message':message , 'response':response})
    new_session = Session.objects.create(name = "New Chat")
    return render(request,"chatbot.html",context={'session_id':new_session.id, 'session_name':new_session.name})

def session(request):
    if request.method == 'POST':
        new_session = Session.objects.create(name = "New Chat")
        return JsonResponse({'session_id':new_session.id, 'session_name':new_session.name})
    if request.method == 'PATCH':
        session = Session.objects.filter(id = request.PATCH.get('id')).first()
        session.updated_at = timezone.now()
        return JsonResponse({'status':'Successfully updated'})
    if request.method == 'GET':
        # Return all sessions ordered by updated_at
        sessions = list(Session.objects.all().values('id', 'name', 'created_at', 'updated_at'))
        return JsonResponse({'sessions': sessions}, status=200)

    return JsonResponse({'error': 'Method not allowed.'}, status=405)
    