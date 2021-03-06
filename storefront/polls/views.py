from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name= 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
    #Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
            ).order_by('-pub_date')[:5]




class DetailView(generic.DetailView):
    model = Question
    template_name= 'polls/detail.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question= get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
        print(selected_choice)
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect (reverse('polls:results', args = (question.id,)))
    except(KeyError, Choice.DoesNotExist):
        #Redisplay the question voting form
        return render(request, 'polls/result_not_found.html', {
            'question' : question,
            'error message':"You didn't select a choice."
    })
