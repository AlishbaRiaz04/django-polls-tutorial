from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Choice
from django.views import generic
from django.utils import timezone
from django.db.models import F
from django.views.decorators.http import require_POST

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now(),
            choice__isnull=False,
        ).order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model=Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        )
@require_POST
def vote(request, question_id):
    question=get_object_or_404(
        Question,
        pk=question_id,
        pub_date__lte=timezone.now(),
    )

    try:
        selected_choice=question.choice_set.get(
            pk=request.POST["choice"]
        )
    except (KeyError, ValueError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    Choice.objects.filter(pk=selected_choice.pk).update(
        votes=F("votes")+1
    )

    return redirect("polls:results", pk=question.id)

class ResultsView(generic.DetailView):
    model= Question
    template_name = "polls/results.html"

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        )



