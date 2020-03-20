from django.shortcuts import render,redirect
from bs4 import BeautifulSoup
import requests
import collections
import pandas as pd
from atgapp.models import urls,words_count

# Create your views here.

def home(request):
    return redirect(frequency)


def frequency(request):
    return render(request, "frequency.html")

def results(request):
    if request.method == 'POST':
        url = request.POST['url']
        if urls.objects.filter(url=url).exists():
            p = "This Data is from databse"
            data = words_count.objects.filter(fromurl=url)
            words = []
            for d in data:
                words.append(str(d.words+"  : "+str(d.count)+" times"))
            return render(request,"result.html",{"words": words,"p":p})
        else:
            res = requests.get(url)
            html_page = res.content
            soup = BeautifulSoup(html_page, 'html.parser')
            text = soup.find_all(text=True)
            output = ''
            blacklist = [
                '[document]','an','div','class','style','meta','header','noscript','header','html','meta','head', 'input','script','the','of','and','to','a','in','for','is','on','that','by','this','with','i','you','it','not','or','be','are','from','at','as',]
            for t in text:
                if t.parent.name not in blacklist:
                    output += '{} '.format(t)

            wordcount = {}
            for word in output.lower().split():
                word = word.replace(".","")
                word = word.replace(",","")
                word = word.replace(":","")
                word = word.replace("\"","")
                word = word.replace("!","")
                word = word.replace("â€œ","")
                word = word.replace("â€˜","")
                word = word.replace("*","")
                if word not in blacklist:
                    if word not in wordcount:
                        wordcount[word] = 1
                    else:
                        wordcount[word] += 1
            word_counter = collections.Counter(wordcount)
            words = []
            for word, count in word_counter.most_common(10):
                words.append(str(word+"  : "+str(count)+" times"))
                set_words = words_count(fromurl = url,words = word,count = count
                )
                set_words.save()
            set_urls = urls(url=url)
            set_urls.save()
            p = "This is a Preprocessed Data"
            return render(request,"result.html",{"words": words,"p":p})