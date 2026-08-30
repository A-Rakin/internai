"""
============================================================
Chatbot Views - AI-Powered Assistant Endpoints
============================================================
Handles AJAX chat interactions with Groq Cloud AI.
============================================================
"""

import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings

from chatbot.models import ChatSession, ChatMessage


def _get_system_prompt(user):
    """Generate a role-aware system prompt for the AI assistant."""
    role = user.role
    role_context = {
        'student': (
            "The user is a Student on the InternAI platform. "
            "Help them with internship applications, resume tips, cover letter writing, "
            "interview preparation, weekly report writing, and career guidance. "
            "Be encouraging and supportive."
        ),
        'company': (
            "The user is a Company HR Recruiter on the InternAI platform. "
            "Help them with writing internship descriptions, evaluating candidates, "
            "scheduling interviews, understanding AI match scores, and recruitment best practices."
        ),
        'supervisor': (
            "The user is an Academic Supervisor on the InternAI platform. "
            "Help them with evaluating student reports, writing feedback, "
            "grading criteria, and academic supervision best practices."
        ),
        'admin': (
            "The user is a Platform Administrator on InternAI. "
            "Help them with platform management, user moderation, analytics interpretation, "
            "and system administration tasks."
        ),
    }

    return (
        "You are InternAI Assistant, a helpful AI powered by advanced language models. "
        "You assist users of the InternAI Internship Management Platform. "
        f"{role_context.get(role, '')} "
        "Keep responses concise, professional, and helpful. "
        "Use markdown formatting when helpful. "
        "If asked about something outside the platform, politely redirect to internship-related topics."
    )


@login_required
def chat_page(request):
    """Main chat page view."""
    sessions = ChatSession.objects.filter(user=request.user)[:20]
    return render(request, 'chatbot/chat.html', {'sessions': sessions})


@login_required
@require_POST
def send_message(request):
    """AJAX endpoint to send a message and get AI response."""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id')

        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)

        # Get or create session
        if session_id:
            session = get_object_or_404(ChatSession, pk=session_id, user=request.user)
        else:
            # Create new session with first message as title
            title = user_message[:50] + ('...' if len(user_message) > 50 else '')
            session = ChatSession.objects.create(user=request.user, title=title)

        # Save user message
        ChatMessage.objects.create(session=session, role='user', content=user_message)

        # Build conversation history for context
        history = list(session.messages.order_by('created_at').values('role', 'content'))
        # Limit to last 10 messages for token management
        history = history[-10:]

        # Get AI response
        ai_response = _get_ai_response(request.user, history)

        # Save AI response
        ChatMessage.objects.create(session=session, role='assistant', content=ai_response)
        session.save()  # Update timestamp

        return JsonResponse({
            'response': ai_response,
            'session_id': session.pk,
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def get_session(request, pk):
    """Load messages for a specific chat session."""
    session = get_object_or_404(ChatSession, pk=pk, user=request.user)
    messages = list(session.messages.order_by('created_at').values('role', 'content', 'created_at'))

    # Format dates
    for msg in messages:
        msg['created_at'] = msg['created_at'].strftime('%b %d, %I:%M %p')

    return JsonResponse({
        'session_id': session.pk,
        'title': session.title,
        'messages': messages,
    })


@login_required
@require_POST
def new_session(request):
    """Create a new chat session."""
    session = ChatSession.objects.create(user=request.user, title='New Chat')
    return JsonResponse({'session_id': session.pk})


def _get_ai_response(user, history):
    """Get AI response from Groq Cloud API or fallback."""
    groq_api_key = getattr(settings, 'GROQ_API_KEY', '')

    if groq_api_key and not groq_api_key.startswith('gsk_your_groq'):
        try:
            from groq import Groq
            client = Groq(api_key=groq_api_key)

            messages = [
                {"role": "system", "content": _get_system_prompt(user)}
            ]
            for msg in history:
                messages.append({
                    "role": msg['role'] if msg['role'] in ['user', 'assistant'] else 'user',
                    "content": msg['content']
                })

            response = client.chat.completions.create(
                messages=messages,
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=1024,
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Groq Chatbot Error: {e}")

    # Fallback response
    return _local_fallback(history[-1]['content'] if history else '')


def _local_fallback(message):
    """Simple keyword-based fallback when API is unavailable."""
    message_lower = message.lower()

    if any(w in message_lower for w in ['resume', 'cv']):
        return (
            "📄 **Resume Tips:**\n\n"
            "1. **Keep it concise** — 1-2 pages maximum\n"
            "2. **Tailor it** to each internship's required skills\n"
            "3. **Use action verbs** — Built, Developed, Designed, Led\n"
            "4. **Include projects** — GitHub repos, portfolio links\n"
            "5. **Quantify achievements** — 'Increased efficiency by 30%'\n\n"
            "Upload your resume on InternAI and our AI will automatically match you with suitable internships!"
        )
    elif any(w in message_lower for w in ['interview', 'prepare']):
        return (
            "🎯 **Interview Preparation Tips:**\n\n"
            "1. **Research the company** thoroughly before the interview\n"
            "2. **Practice STAR method** — Situation, Task, Action, Result\n"
            "3. **Prepare questions** to ask the interviewer\n"
            "4. **Review technical concepts** related to the role\n"
            "5. **Test your setup** if it's an online interview\n\n"
            "Check your upcoming interviews in the Interviews tab on your dashboard!"
        )
    elif any(w in message_lower for w in ['cover letter', 'application']):
        return (
            "✍️ **Cover Letter Guide:**\n\n"
            "1. **Opening** — Express enthusiasm for the specific role\n"
            "2. **Body** — Connect your skills to the job requirements\n"
            "3. **Examples** — Share relevant project or coursework experience\n"
            "4. **Closing** — Express eagerness for the opportunity\n\n"
            "Tip: Use our AI Cover Letter Generator when applying to have one auto-generated for you!"
        )
    elif any(w in message_lower for w in ['report', 'weekly']):
        return (
            "📋 **Weekly Report Tips:**\n\n"
            "1. **Be specific** about tasks completed\n"
            "2. **Mention tools/technologies** used\n"
            "3. **Document challenges** and how you overcame them\n"
            "4. **Set clear goals** for next week\n"
            "5. **Track hours** accurately\n\n"
            "Submit your weekly reports from the Reports section in your dashboard."
        )
    elif any(w in message_lower for w in ['hello', 'hi', 'hey', 'help']):
        return (
            "👋 **Hello!** I'm the InternAI Assistant. I can help you with:\n\n"
            "- 📄 Resume and CV tips\n"
            "- ✍️ Cover letter writing\n"
            "- 🎯 Interview preparation\n"
            "- 📋 Weekly report guidance\n"
            "- 💼 Internship search strategies\n"
            "- 📊 Understanding your AI match scores\n\n"
            "Just ask me anything related to internships and your career!"
        )
    else:
        return (
            "Thank you for your message! I'm the InternAI Assistant and I'm here to help with:\n\n"
            "- Resume optimization\n"
            "- Interview preparation\n"
            "- Cover letter writing\n"
            "- Weekly report guidance\n"
            "- Career advice\n\n"
            "Could you please ask a more specific question so I can assist you better?"
        )
