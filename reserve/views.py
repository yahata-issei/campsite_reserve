from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # トップページ（index.html）を表示する処理
    return render(request, 'reserve/index.html')

def clicked(request):
    # htmxのボタンが押された時、HTMLパーツだけを返す処理
    return HttpResponse("<p>DjangoからhtmxでHTMLパーツを取得しました！</p>")