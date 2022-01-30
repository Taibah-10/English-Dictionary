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
    if not word:
        return render(request, "index.html")
    # dictionary = PyDictionary()
    # meaning = dictionary.meaning(word)
    # synonyms = dictionary.synonym(word)
    # antonyms = dictionary.antonym(word)
    res = requests.get('https://www.dictionary.com/browse/' + word)
    res1 = requests.get('https://www.thesaurus.com/browse/' + word)
    if not res and not res1:
        word = "Sorry, " + word + " is not found in our database."
        meaning = "None"
        antonym = "-"
        antonym = antonym[-1]
        synonym = "-"

    else:
        if res:
            soup=BeautifulSoup(res.text, "html.parser")
            meanings = soup.find('div', {'value': '1'})
            meaning = meanings.getText()
        else:
            word = "Sorry, " + word + " is not found in our database."
            meaning = "None"

        if res1:
            soup1=BeautifulSoup(res1.text, "html.parser")
            synonyms = soup1.find_all('a', {'class': "css-1kg1yv8 eh475bn0"})
            if(synonyms):
                synlist = []
                for syn in synonyms[:6]:
                    s = "".join(syn)
                    synlist.append(s)
                synonym = synlist
            else:
                synonyms = soup1.find_all('a', {'class': "css-1gyuw4i eh475bn0"}) 
                synlist = []
                for syn in synonyms[:6]:
                    s = "".join(syn)
                    synlist.append(s)
                synonym = synlist

            antonyms = soup1.find_all('a', {'class': "css-15bafsg eh475bn0"})
            if(antonyms):
                antlist = []
                for ant in antonyms[:6]:
                    a = "".join(ant)
                    antlist.append(a)
                antonym = antlist
            else:
                antonyms = soup1.find_all('a', {'class': "css-pc0050 eh475bn0"})
                antlist = []
                for ant in antonyms[:6]:
                    a = "".join(ant)
                    antlist.append(a)
                antonym = antlist

        else:
            word = "Sorry, the synonyms and antonyms of " + word + " is not found in our database."
            antonym = "".join("None")
            synonym = "".join("None")
        
    context={
        'word': word,
        'meaning': meaning,
        'synonyms': synonym,
        'antonyms': antonym
    }
    return render(request, 'search.html', context)
