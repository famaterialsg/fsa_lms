from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer,Subject, Category
from .forms import QuestionForm, AnswerForm
from module_group.models import ModuleGroup

from django.contrib.auth.decorators import login_required

@login_required
def question_list(request):
    questions = Question.objects.all()
    module_groups = ModuleGroup.objects.all()

  
    for question in questions:
        correct_answer = question.answers.filter(is_correct=True).first()
        
        question.correct_answer = correct_answer.text if correct_answer else 'No correct answer'

    return render(request, 'question_list.html', {
        'questions': questions,
        'module_groups': module_groups
    })
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    module_groups = ModuleGroup.objects.all()
    return render(request, 'question_detail.html', {'question': question,'module_groups': module_groups})

def question_add(request):
    module_groups = ModuleGroup.objects.all()
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save()
            answer_texts = request.POST.getlist('answer_text[]')
            is_corrects = request.POST.getlist('is_correct[]')
            if len(answer_texts) != len(is_corrects):
                return render(request, 'question_add.html', {
                    'question_form': question_form,
                    'error': 'Mismatch between answer texts and correctness flags'
                })
            for i in range(len(answer_texts)):
                Answer.objects.create(
                    question=question,
                    text=answer_texts[i],
                    is_correct=is_corrects[i].lower() == 'true'
                )
            return redirect('question:question_list')
    else:
        question_form = QuestionForm()
    return render(request, 'question_add.html', {'question_form': question_form,'module_groups': module_groups})

def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk)
    module_groups = ModuleGroup.objects.all()
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('question:question_list')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'question_form.html', {'form': form,'module_groups': module_groups})

def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        question.delete()
        return redirect('question:question_list')
    return render(request, 'question_confirm_delete.html', {'question': question})

def answer_add(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk)  
    module_groups = ModuleGroup.objects.all()
    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.question = question  #
            answer.save()
            return redirect('question:question_detail', pk=question_pk)  
    else:
        answer_form = AnswerForm()
    return render(request, 'answer_add.html', {'answer_form': answer_form, 'question': question,'module_groups': module_groups})

# View for Subject Detail
def subject_detail(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    return render(request, 'subject_detail.html', {'subject': subject})

# View for Category Detail
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'category_detail.html', {'category': category})