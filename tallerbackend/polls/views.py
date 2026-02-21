import json
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from .models import Answer
from  django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    latest_answer_list = Answer.objects.order_by("-pub_date")[:5]
    context = {"latest_answer_list": latest_answer_list}
    return render(request, "polls/index.html", context)

@csrf_exempt
def answers_collection(request):
    if request.method == "GET":
        answers = Answer.objects.order_by("-id")[:5]
        data = [
            {
                "id": a.id,
                "answer_text": a.answer_text,
                "pub_date": timezone.localtime(a.pub_date).strftime("%Y-%m-%d %H:%M:%S"),
            }
            for a in answers
        ]
        return JsonResponse(data, safe=False)

    if request.method == "POST":
        try:
            body = json.loads(request.body or "{}")
            answer_text = (body.get("answer_text") or "").strip()
            if not answer_text:
                return JsonResponse({"error": "El campo 'answer_text' es requerido"}, status=400)

            answer = Answer.objects.create(answer_text=answer_text)

            return JsonResponse(
                {
                    "id": answer.id,
                    "answer_text": answer.answer_text,
                    "pub_date": timezone.localtime(answer.pub_date).isoformat(),
                },
                status=201,
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)


