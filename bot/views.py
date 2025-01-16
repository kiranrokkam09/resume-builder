from django.shortcuts import render
from django.http import JsonResponse
import anthropic
from .models import Chat
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
        one_hour_ago = timezone.now() - timedelta(hours=1)
        history = Chat.objects.filter(timestamp__gte=one_hour_ago).values()
        response = ask_ai(message,history)
        Chat.objects.create(message= message, response=response)
        return JsonResponse({'message':message , 'response':response})
    return render(request,"chatbot.html")