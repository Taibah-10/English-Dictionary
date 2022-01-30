from multiprocessing import context
from django.shortcuts import render
from PyDictionary import PyDictionary
import requests
from bs4 import BeautifulSoup

# Create your views here.
def index(request):
    return render(request, 'index.html')

def search(request):
    word=request.GET.get('word')
    # dictionary = PyDictionary()
    # meaning = dictionary.meaning(word)
    # synonyms = dictionary.synonym(word)
    # antonyms = dictionary.antonym(word)
    res = requests.get('https://www.dictionary.com/browse/' + word)
    res1 = requests.get('https://www.thesaurus.com/browse/' + word)
    if res:
        soup=BeautifulSoup(res.text, "html.parser")
        meanings = soup.find('div', {'value': '1'})
        meaning = meanings.getText()
    else:
        word = "Sorry, " + word + " is not found in our database."
        meaning = ""

    if res1:
        soup1=BeautifulSoup(res1.text, "html.parser")
        synonyms = soup1.find_all('a', {'class': "css-1kg1yv8 eh475bn0"})
        if(synonyms):
            synonym = []
            for syn in synonyms[:6]:
                s = "".join(syn)
                synonym.append(s)
        else:
            synonyms = soup1.find_all('a', {'class': "css-1gyuw4i eh475bn0"}) 
            synonym = []
            for syn in synonyms[:6]:
                s = "".join(syn)
                synonym.append(s)

        antonyms = soup1.find_all('a', {'class': "css-15bafsg eh475bn0"})
        if(antonyms):
            antonym = []
            for ant in antonyms[:6]:
                a = "".join(ant)
                antonym.append(a)
        else:
            antonyms = soup1.find_all('a', {'class': "css-pc0050 eh475bn0"})
            antonym = []
            for ant in antonyms[:6]:
                a = "".join(ant)
                antonym.append(a)

    else:
        word = "Sorry, the synonyms and antonyms of " + word + " is not found in our database."
        antonym = ""
        synonym = ""
    
    context={
        'word': word,
        'meaning': meaning,
        'synonyms': synonym,
        'antonyms': antonym
    }
    return render(request, 'search.html', context)