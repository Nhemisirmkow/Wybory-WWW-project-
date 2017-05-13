from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST

# Create your views here.

from zadanie2.filter import TestFilter
from zadanie2.forms import GminaQuestionForm, UserCreationForm
from zadanie2.models import Województwo, Okręg, Gmina, Test
from zadanie2.viewHelper import daj_tabele_wyników_kandydatów, zmień_głosy


def test_list(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        # do_something_with(form.cleaned_data)
        return redirect("zadanie2/kraj")

    return render_to_response("test2.html", {'form': form}, locals())
    # return render(request, 'test2.html', locals())


def index(request):
    return HttpResponse()


def kraj(request):
    # Hack here
    nazwa = "DOLNOŚLĄSKIE"
    kraj = Województwo.objects.get(nazwa=nazwa)
    liczba_województw = 0
    for w in Województwo.objects.all():
        if w.nazwa == nazwa:
            continue
        liczba_województw += 1
        kraj.uprawnionych += w.uprawnionych
        kraj.kart_wydanych += w.kart_wydanych
        kraj.głosów_oddanych += w.głosów_oddanych
        kraj.głosów_nieważnych += w.głosów_nieważnych
        kraj.głosów_ważnych += w.głosów_ważnych

    # f = GminaFilter(request.GET, queryset=Gmina.objects.all())

    questionForm = GminaQuestionForm()
    kandydaci = daj_tabele_wyników_kandydatów('kraj', 'POLSKA - TO jest niepotrzebne')
    województwa = Województwo.objects.all()
    return render(request, 'kraj2.html', locals())

def województwo(request, skrót):
    skrót = 'PL-' + skrót
    w = get_object_or_404(Województwo, nazwa_skrót=skrót)
    questionForm = GminaQuestionForm( )
    kandydaci = daj_tabele_wyników_kandydatów('województwo', w.nazwa)
    okręgi = Okręg.objects.filter(województwo=w.nazwa)
    return render(request, 'województwo2.html', locals())

def okręg(request, numer):
    o = get_object_or_404(Okręg, numer=numer)
    questionForm = GminaQuestionForm( )
    kandydaci = daj_tabele_wyników_kandydatów('okręg', o.numer)
    gminy = Gmina.objects.filter(okręg=o.numer)
    return render(request, 'okręg2.html', locals())

def gmina(request, id):
    g = get_object_or_404(Gmina, id_gminy=id)
    questionForm = GminaQuestionForm( )
    kandydaci = daj_tabele_wyników_kandydatów('gmina', g.id_gminy)
    message = "NA DOLE STRONY MOŻNA OD TERAZ ZMIENIAĆ WYNIKI!"
    message_wrong = "PODANO ZŁĄ LICZBĘ!"
    if request.method == 'POST':
        głosy = []
        i = 0
        for k in kandydaci:
            głosy.append(request.POST.get(k.nazwa))
            if głosy[i].isdigit():
                głosy[i] = int(głosy[i])
            else:
                message = message_wrong
            i += 1
        if message != message_wrong:
    #       tutaj każdemu kandydatowi
    #       zmieniamy głosy w Gminie, okręgu i województwie,
    #       a następnie zmieniamy liczbę
    #       uprwnionych, kart wydanych,
    #       głosów oddanych, głosów ważnych
    #       w Gminie, okręgu i województwie
            zmień_głosy(głosy, kandydaci, id)
            return HttpResponseRedirect(request.path)
    return render(request, 'gmina2.html', locals())

@require_POST
def loginView(request):
    user = authenticate(username=request.POST["username"], password=request.POST["password"])
    url = request.POST.get('next')
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(url)
    else:
        return HttpResponseForbidden('<meta http-equiv="refresh" content="2;url=%s"> Zły użytkownik lub hasło.' % url)

@require_POST
def logoutView(request):
    logout(request)
    url = request.POST.get('next')
    return HttpResponseRedirect(url)

def przekierujDoGminy(request):
    nazwa = request.POST.get('nazwa')
    gminy = Gmina.objects.filter(nazwa__icontains=nazwa)
    if gminy.count() > 0:
        return render( request, 'wyszukajGmine.html', locals( ) )
    url = request.POST.get('next')
    return HttpResponseForbidden('<meta http-equiv="refresh" content="2;url=%s"> Nie ma takiej gminy.' % url)