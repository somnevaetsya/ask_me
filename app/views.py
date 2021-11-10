from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import Http404
from app.models import Answer, LikeToAns, LikeToQue, Tag, Question, Profile
from django.template.defaulttags import register


# Create your views here.


@register.filter
def get_item(dictionary, key):
    return dictionary[0][key]


def pagination(request, listing, n):
    paginator = Paginator(listing, n)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return content


def index(request):
    questions = [{'title': Question.objects.new_que()[i].title,
                  'text': Question.objects.new_que()[i].text_que,
                  'answer': Answer.objects.count_answ(Question.objects.new_que()[i].id),
                  'like_to_que': LikeToQue.objects.count_like_que(Question.objects.new_que()[i].id),
                  'tag': Question.objects.get_tag(Question.objects.new_que()[i].id, 0),
                  'id':Question.objects.new_que()[i].id}
                 # 'url': Question.objects.get(id=i).get_absolute_url()}
                 for i in range(0, Question.objects.count())
                 ]
    content = pagination(request, questions, 10)
    return render(request, "index.html", context={'post': content})


def hot(request):
    questions = [{'title': Question.objects.hot_que(i).title,
                  'text': Question.objects.hot_que(i).text_que,
                  'tag': Question.objects.get_tag(Question.objects.hot_que(i).id, 0),
                  'answer': Answer.objects.count_answ(Question.objects.hot_que(i).id),
                  'like_to_que': LikeToQue.objects.count_like_que(Question.objects.hot_que(i).id),
                  'tag': Question.objects.get_tag(Question.objects.hot_que(i).id, 0),
                  'id':Question.objects.hot_que(i).id}
                 # 'url': Question.objects.get(id=i).get_absolute_url()}
                 for i in range(0, Question.objects.count())
                 ]
    content = pagination(request, questions, 10)
    return render(request, "hot.html", context={'post': content})


# questions = [
#     {
#         "title": f"Title {i}",
#         "id": i,
#         "text": f"This is text for {i} question.",
#     } for i in range(20)
# ]

def tag(request, ind_que):
    cur_tag = Question.objects.get_tag(ind_que, 0)
    ques = Question.objects.get_que_tag(cur_tag)
    if ques.exists():
        questions = [{'title': Question.objects.get_que_tag(cur_tag)[i].title,
                      'text': Question.objects.get_que_tag(cur_tag)[i].text_que,
                      'answer': Answer.objects.count_answ(Question.objects.get_que_tag(cur_tag)[i].id),
                      'tag': Question.objects.get_tag(Question.objects.get_que_tag(cur_tag)[i].id, 0),
                      'like_to_que': LikeToQue.objects.count_like_que(Question.objects.get_que_tag(cur_tag)[i].id),
                      'id':ind_que}
                     # 'url': Question.objects.get(id=i).get_absolute_url()}
                     for i in range(Tag.objects.count_tags(cur_tag))
                     ]
        content = pagination(request, questions, 5)
        return render(request, "tags.html", {'post': content})
    else:
        raise Http404("Tag does not exist")


def question(request, ind_que):
    answers = [{'title': Question.objects.get(id=ind_que).title,
                'text': Question.objects.get(id=ind_que).text_que,
                'text_ans': Answer.objects.get_answer(ind_que, i - 1),
                'tag': Question.objects.get_tag(ind_que, 0),
                'like_to_que': LikeToQue.objects.count_like_que(ind_que),
                'like_to_ans': LikeToAns.objects.count_like_ans(i),
                'id': ind_que}
               # 'url': Question.objects.get(id=i).get_absolute_url()}
               for i in range(1, Answer.objects.count_answ(ind_que) + 1)
               ]

    content = pagination(request, answers, 5)
    return render(request, "question.html", {'post': content})


def login(request):
    return render(request, "login.html", {})


def signup(request):
    return render(request, "sign_up.html", {})


def ask(request):
    return render(request, "ask.html", {})


def settings(request):
    return render(request, "settings.html", {})
