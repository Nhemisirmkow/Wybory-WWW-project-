import csv
import color as color
from zadanie2.dane import Kandydaci, województwo_skrót
from zadanie2.models import Test, Kandydat, Gmina, Okręg, Województwo, Kandydat_Gmina, Kandydat_Okręg, \
    Kandydat_Województwo
import random

data = '/home/nicram/PycharmProjects/wybory2/pkw2000.csv'


def generate_color():
    color = '#{:02x}{:02x}{:02x}'.format( *map( lambda x: random.randint( 0, 255 ), range( 3 ) ) )
    return color


def load_test():
    for i in Kandydaci:
        print( i )
        Test.objects.update_or_create( nazwa=i )
        # for k in Test.objects.all():
        #     print(k.nazwa, "lol")


print( color.black )


def load_kandydat():
    for k in Kandydaci:
        Kandydat.objects.update_or_create( nazwa=k, kolor=generate_color( ) )


def zapisz_okręg(obiekt_okręgu, o_filter):
    o_filter.update( liczba_gmin=obiekt_okręgu.liczba_gmin,
                     uprawnionych=obiekt_okręgu.uprawnionych,
                     kart_wydanych=obiekt_okręgu.kart_wydanych,
                     głosów_oddanych=obiekt_okręgu.głosów_oddanych,
                     głosów_nieważnych=obiekt_okręgu.głosów_nieważnych,
                     głosów_ważnych=obiekt_okręgu.głosów_ważnych )


def zapisz_województwo(obiekt_województwa, w_filter):
    w_filter.update( liczba_okręgów=obiekt_województwa.liczba_okręgów,
                     uprawnionych=obiekt_województwa.uprawnionych,
                     kart_wydanych=obiekt_województwa.kart_wydanych,
                     głosów_oddanych=obiekt_województwa.głosów_oddanych,
                     głosów_nieważnych=obiekt_województwa.głosów_nieważnych,
                     głosów_ważnych=obiekt_województwa.głosów_ważnych )


class Województwo_obiekt( ):
    nazwa_skrót = ""
    nazwa = ""
    liczba_okręgów = 0
    uprawnionych = 0
    kart_wydanych = 0
    głosów_oddanych = 0
    głosów_nieważnych = 0
    głosów_ważnych = 0


class Okręg_obiekt( ):
    nazwa_skrót = ""
    nazwa = ""
    liczba_gmin = 0
    uprawnionych = 0
    kart_wydanych = 0
    głosów_oddanych = 0
    głosów_nieważnych = 0
    głosów_ważnych = 0


class Głos( ):
    # Odniesienie do obiektu z bazy danych
    nazwa = ""
    liczba = 0


def zmień_okręg(numer_okręgu, w1, w, kandydat, row, o1):
    o1 += 1
    Okręg.objects.create( numer=numer_okręgu, województwo=w1 )
    w.liczba_okręgów += 1
    for id, k in zip( range( 12 ), kandydat ):
        kandydat[id]["okręg"][numer_okręgu] = Głos( )
        kandydat[id]["okręg"][numer_okręgu].nazwa = o1
    return (o1, w, Okręg_obiekt( ), Okręg.objects.filter( numer=numer_okręgu ), numer_okręgu, kandydat)


def zmień_województwo(nazwa_województwa, kandydat, row):
    w1 = nazwa_województwa
    Województwo.objects.create( nazwa_skrót="PL-" + województwo_skrót[nazwa_województwa], nazwa=nazwa_województwa )
    for id, k in zip( range( 12 ), kandydat ):
        kandydat[id]["województwo"][nazwa_województwa] = Głos( )
        kandydat[id]["województwo"][nazwa_województwa].nazwa = w1
    return (
        w1, Województwo_obiekt( ), Województwo.objects.filter( nazwa=nazwa_województwa ), nazwa_województwa, kandydat)


def zapisz_kandydatów(kandydat):
    insert_list_kandydat_gmina = []
    insert_list_kandydat_województwo = []
    insert_list_kandydat_okręg = []
    for id, k in zip( range( 12 ), kandydat ):
        nazwa_kandydata = nazwa = Kandydaci[id]
        for g in k['gmina']:
            # print( k['gmina'][g].nazwa )
            insert_list_kandydat_gmina.append( Kandydat_Gmina( gmina=k['gmina'][g].nazwa,
                                                               nazwa=nazwa_kandydata,
                                                               liczba_głosów=k['gmina'][g].liczba ) )
        for o in k["okręg"]:
            insert_list_kandydat_okręg.append( Kandydat_Okręg( okręg=k['okręg'][o].nazwa,
                                                               nazwa=nazwa_kandydata,
                                                               liczba_głosów=k['okręg'][o].liczba ) )
        for w in k['województwo']:
            insert_list_kandydat_województwo.append( Kandydat_Województwo( województwo=k['województwo'][w].nazwa,
                                                                           nazwa=nazwa_kandydata,
                                                                           liczba_głosów=k['województwo'][w].liczba ) )
    Kandydat_Gmina.objects.bulk_create( insert_list_kandydat_gmina )
    Kandydat_Okręg.objects.bulk_create( insert_list_kandydat_okręg )
    Kandydat_Województwo.objects.bulk_create( insert_list_kandydat_województwo )


def load_dane():
    # pierwszy = Województwo.objects.all()
    nazwa_poprzednia_województwa = ""
    numer_poprzedni_okręgu = -1

    w_filter = Województwo.objects.filter( nazwa="" )
    o_filter = Okręg.objects.filter( numer=-1 )

    w = Województwo_obiekt( )
    o = Okręg_obiekt( )
    o1 = 0
    # kandydat = [{
    #         "gmina": {},
    #         "okręg": {},
    #         "województwo": {},
    #     } for i in range(12)]
    kandydat = [{}] * 12
    for i in range( 12 ):
        kandydat[i] = {
            "gmina": {},
            "okręg": {},
            "województwo": {},
        }

    licznik = -1

    with open( data ) as file:
        insert_list_gmina = []
        reader = csv.reader( file )
        for row in reader:
            licznik += 1
            print( "jeszcze ładuję statystyki", licznik )
            if row[3] != 'Gmina':
                if nazwa_poprzednia_województwa == row[0]:
                    # Nie zmieniamy województwa
                    if numer_poprzedni_okręgu != row[1]:
                        # Zapisujemy ostateczne dane okręgu
                        zapisz_okręg( o, o_filter )
                        # Zmieniamy okręg
                        (o1, w, o, o_filter, numer_poprzedni_okręgu, kandydat) = zmień_okręg( row[1], w1, w, kandydat,
                                                                                              row, o1 )
                else:
                    # Zapisujemy ostateczne dane wojeówdztwa
                    zapisz_województwo( w, w_filter )
                    # Zmieniło się województwo
                    (w1, w, w_filter, nazwa_poprzednia_województwa, kandydat) = zmień_województwo( row[0], kandydat,
                                                                                                   row )
                    # Zapisujemy ostateczne dane okręgu
                    zapisz_okręg( o, o_filter )
                    # Zmienił się też okręg
                    (o1, w, o, o_filter, numer_poprzedni_okręgu, kandydat) = zmień_okręg( row[1], w1, w, kandydat, row,
                                                                                          o1 )
                # Mamy aktualny okręg i województwo.
                # dodajemy gminę
                insert_list_gmina.append( Gmina( id_gminy=licznik,
                                                 kod_gminy=row[2],
                                                 nazwa=row[3],
                                                 liczba_obwodów=int( row[5] ),
                                                 uprawnionych=int( row[6] ),
                                                 kart_wydanych=int( row[7] ),
                                                 głosów_oddanych=int( row[8] ),
                                                 głosów_nieważnych=int( row[9] ),
                                                 głosów_ważnych=int( row[10] ),
                                                 okręg=o1 ) )

                # updateujemy głosy
                for id, k in zip( range( 12 ), kandydat ):
                    kandydat[id]["gmina"][licznik] = Głos( )
                    kandydat[id]["gmina"][licznik].nazwa = licznik
                    # 11 kolumna to pierwszy kandydat
                    kandydat[id]["gmina"][licznik].liczba = row[id + 11]
                    kandydat[id]["okręg"][str( o1 )].liczba += int( row[id + 11] )
                    kandydat[id]["województwo"][w1].liczba += int( row[id + 11] )

                # updateujemy okręg - referencja już jest
                o.liczba_gmin += 1
                o.uprawnionych += int( row[6] )
                o.kart_wydanych += int( row[7] )
                o.głosów_oddanych += int( row[8] )
                o.głosów_nieważnych += int( row[9] )
                o.głosów_ważnych += int( row[10] )

                # updateujemy województwo - liczba_okręgów zmieniona przy dodawaniu okręgu
                w.uprawnionych += int( row[6] )
                w.kart_wydanych += int( row[7] )
                w.głosów_oddanych += int( row[8] )
                w.głosów_nieważnych += int( row[9] )
                w.głosów_ważnych += int( row[10] )

    Gmina.objects.bulk_create( insert_list_gmina )
    zapisz_okręg( o, o_filter )
    zapisz_województwo( w, w_filter )
    zapisz_kandydatów( kandydat )
