from zadanie2.models import Kandydat, Kandydat_Województwo, Kandydat_Okręg, Kandydat_Gmina, Okręg, Gmina, Województwo


def daj_tabele_wyników_kandydatów(zasięg, kod_zasięgu):
    def znajdź_liczbe_głosów_kandydata_w_kraju(nazwa):
        w_filter = Kandydat_Województwo.objects.filter( nazwa=nazwa )
        wynik = 0
        for w in w_filter:
            wynik += w.liczba_głosów
        return wynik

    kandydaci = [object] * Kandydat.objects.all( ).count( )

    idx = 0
    liczba_wszystkich_głosów = 0
    for k in Kandydat.objects.all( ):
        kandydaci[idx] = Kandydaci( )
        kandydaci[idx].kolor = k.kolor
        kandydaci[idx].nazwa = k.nazwa
        if zasięg == 'kraj':
            kandydaci[idx].liczba_głosów = znajdź_liczbe_głosów_kandydata_w_kraju( k.nazwa )
        elif zasięg == 'województwo':
            kandydaci[idx].liczba_głosów = Kandydat_Województwo.objects.get( województwo=kod_zasięgu,
                                                                             nazwa=k.nazwa ).liczba_głosów
        elif zasięg == 'okręg':
            kandydaci[idx].liczba_głosów = Kandydat_Okręg.objects.get( okręg=kod_zasięgu, nazwa=k.nazwa ).liczba_głosów
        elif zasięg == 'gmina':
            kandydaci[idx].liczba_głosów = Kandydat_Gmina.objects.get( gmina=kod_zasięgu, nazwa=k.nazwa ).liczba_głosów
        else:
            kandydaci[idx].liczba_głosów = -1
        liczba_wszystkich_głosów += kandydaci[idx].liczba_głosów
        idx += 1

    for k in kandydaci:
        k.procentowy_wynik = k.liczba_głosów / liczba_wszystkich_głosów * 100.00

    return kandydaci


def zmień_głosy_kandydata(nazwa, nowa_liczba, id_gminy):
    # print("Zmienię", Kandydat_Gmina.objects.get(nazwa=nazwa, gmina=id_gminy), "na", nowa_liczba )
    Kandydat_Gmina.objects.filter( nazwa=nazwa, gmina=id_gminy ).update( liczba_głosów=nowa_liczba )
    numer_okręgu = Gmina.objects.get( id_gminy=id_gminy ).okręg
    # print("Zmienię", Kandydat_Okręg.objects.get(nazwa=nazwa, okręg=numer_okręgu), "na", nowa_liczba)
    Kandydat_Okręg.objects.filter( nazwa=nazwa, okręg=numer_okręgu ).update( liczba_głosów=nowa_liczba )
    nazwa_województwa = Okręg.objects.get( numer=numer_okręgu ).województwo
    # print("Zmienię", Kandydat_Województwo.objects.get(nazwa=nazwa, województwo=nazwa_województwa), "na", nowa_liczba)
    Kandydat_Województwo.objects.filter( nazwa=nazwa, województwo=nazwa_województwa ).update(
        liczba_głosów=nowa_liczba )


def zmień_głosy(głosy, kandydaci, id_gminy):
    liczba_kandydatów = len( głosy )
    więcej_głosów = 0
    for i, k in zip( range( liczba_kandydatów ), kandydaci ):
        if głosy[i] != k.liczba_głosów:
            zmień_głosy_kandydata( k.nazwa, głosy[i], id_gminy )
            więcej_głosów += głosy[i] - k.liczba_głosów
    # print(więcej_głosów)
    g = Gmina.objects.get( id_gminy=id_gminy )
    # print("Zmienię", g, "na", g.uprawnionych + więcej_głosów,
    #       g.kart_wydanych + więcej_głosów, g.głosów_oddanych + więcej_głosów,
    #       g.głosów_ważnych + więcej_głosów)
    Gmina.objects.filter( id_gminy=id_gminy ).update( uprawnionych=g.uprawnionych + więcej_głosów,
                                                      kart_wydanych=g.kart_wydanych + więcej_głosów,
                                                      głosów_oddanych=g.głosów_oddanych + więcej_głosów,
                                                      głosów_ważnych=g.głosów_ważnych + więcej_głosów )
    o = Okręg.objects.get( numer=g.okręg )
    # print("Zmienię", o, "na", o.uprawnionych + więcej_głosów,
    #       o.kart_wydanych + więcej_głosów, o.głosów_oddanych + więcej_głosów,
    #       o.głosów_ważnych + więcej_głosów)
    Okręg.objects.filter( numer=o.numer ).update( uprawnionych=o.uprawnionych + więcej_głosów,
                                                  kart_wydanych=o.kart_wydanych + więcej_głosów,
                                                  głosów_oddanych=o.głosów_oddanych + więcej_głosów,
                                                  głosów_ważnych=o.głosów_ważnych + więcej_głosów )
    w = Województwo.objects.get( nazwa=o.województwo )
    # print("Zmienię", w, "na", w.uprawnionych + więcej_głosów,
    #       w.kart_wydanych + więcej_głosów, w.głosów_oddanych + więcej_głosów,
    #       w.głosów_ważnych + więcej_głosów)
    Województwo.objects.filter( nazwa=w.nazwa ).update( uprawnionych=w.uprawnionych + więcej_głosów,
                                                        kart_wydanych=w.kart_wydanych + więcej_głosów,
                                                        głosów_oddanych=w.głosów_oddanych + więcej_głosów,
                                                        głosów_ważnych=w.głosów_ważnych + więcej_głosów )


class Kandydaci( ):
    kolor = ""
    procentowy_wynik = 0
    liczba_głosów = 0
    nazwa = ""
