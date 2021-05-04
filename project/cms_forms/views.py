
from django.http import HttpResponse
from .models import Content, Comment
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.utils import timezone
from .forms import ContentForm, CommentForm

form = """
<form action="" method="POST">
    Value: <input type="text" name="value">
    <br/><input type="submit" name="action" value="Send Content">
</form>
"""

form2 = """
<form action="" method="POST">
    <br>Title: <input type="text" name="title">
    <br>Body: <input type="text" name="body">
     <br/><input type="submit" name="action" value="Send Comment">
</form>
"""


def logged_in(request):

    if request.user.is_authenticated:
        logged = "Logged in as " + request.user.username
    else:
        logged = "Not logged in. <a href='/login'>Login via login</a>"

    return HttpResponse(logged)


def logout_view(request):
    logout(request)
    return redirect("/cms_forms/")


def login_view(request):
    return redirect("/login")


@csrf_exempt
def index(request):
    form = ContentForm(request.POST)
    context = {"content": {}, "rootpage": True, "form": form}
    return render(request, 'cms_forms/content.html', context=context, status=200)


@csrf_exempt
def get_annotated(request, key):

    try:
        content = Content.objects.get(key=key)
        form = ContentForm(request.POST)
        context = {"content": content, "rootpage": False, "form": form}

    except Content.DoesNotExist:
        return render(request, 'cms_forms/new.html', context={}, status=404)

    return render(request, 'cms_forms/content.html', context=context, status=200)


@csrf_exempt
def edit(request, key):

    if request.method == "POST":
        action = request.POST['action']
        if action == "Send Content":
            value = request.POST['value']
            try:
                content = Content.objects.get(key=key)
                content.value = value

            except Content.DoesNotExist:
                content = Content(key=key, value=value)

            content.save()

    try:
        content = Content.objects.get(key=key)
        form = ContentForm(request.POST)
        context = {"content": content, "rootpage": False, "form": form}

    except Content.DoesNotExist:
        return render(request, 'cms_forms/new.html', context={}, status=404)

    return render(request, 'cms_forms/content.html', context=context, status=200)


@csrf_exempt
def get_content(request, key):

    if request.method == "PUT":
        value = request.body.decode('utf-8')

    if request.method == "POST":
        action = request.POST['action']

        if action == "Send Content":
            value = request.POST['value']
            try:
                content = Content.objects.get(key=key)
                content.value = value
                content.save()
            except Content.DoesNotExist:
                content = Content(key=key, value=value)
                content.save()

        elif action == "Send Comment":
            content = Content.objects.get(key=key)
            title = request.POST['title']
            body = request.POST['body']
            date = timezone.now()
            q = Comment(content=content, title=title, body=body, date=date)
            q.save()

    try:
        content = Content.objects.get(key=key)
        response = "Key '" + key + "' value is: " \
                   + content.value + "<br>"
        status = 200

        comments = content.comment_set.all()
        for comment in comments:
            response += "<p><b>Title</b>: " + comment.title + "<br><b>Body: </b>" + comment.body + "<br><b>Date: </b>" + str(comment.date)

        if request.user.is_authenticated:
            response += form + form2 + "Logged in as " + request.user.username
        else:
            response += "Not logged in. <a href='/login'>Login</a>"

    except Content.DoesNotExist:
        response = 'There is no content for key: ' + key + '<br>'
        if request.user.is_authenticated:
            response = form + "Logged in as " + request.user.username
        else:
            response = "<br>Not logged in. <a href='/login'>Login</a>"
        status = 404

    return HttpResponse(response, status=status)


def cms_new(request):

    if request.method == "POST":
        form = ContentForm(request.POST)
        if form.is_valid():
            content = form.save()
            return redirect('get_content', key=content.key)

    # crear content form y lo muestras si es un GET
    form = ContentForm(request.POST)
    return render(request, 'cms_forms/edit.html', {'form': form, 'is_content': True})


def comment_new(request, key):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            content = Content.objects.get(key=key)
            comment = Comment(content=content, title= request.POST['title'], body=request.POST['body'], date=timezone.now())
            comment.save()
            return redirect('get_content', key=content.key)

    form = CommentForm()
    return render(request, 'cms_forms/edit.html', {'form': form, 'is_content': False})
