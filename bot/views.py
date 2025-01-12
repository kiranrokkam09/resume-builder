from django.shortcuts import render
from django.http import JsonResponse
import anthropic
from .models import Chat

# Create your views here.
client = anthropic.Anthropic(api_key = "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")

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
        history = Chat.objects.all().values()
        response = ask_ai(message,history)
        Chat.objects.create(message= message, response=response)
        return JsonResponse({'message':message , 'response':response})
    return render(request,"chatbot.html")