from django.shortcuts import render

# Create your views here.
def index(requset):
    titles = ['echobot/myFunction.py', 'echobot/views.py']
    texts = [open('echobot/myFunction.py').read(), open('echobot/views.py').read()]
    contents = zip(titles, texts)
    # with open('echobot/views.py') as f:
    #     context = {
    #         'text': f.read(),
    #     }
    context = {
        'titles': titles,
        'texts': texts,
        'contents': contents
    }
    return render(requset, 'displaycode/index.html', context=context)