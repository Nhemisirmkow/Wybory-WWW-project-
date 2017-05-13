from django.test import TestCase
from zadanie2.loadDataBase import load_kandydat, load_test, load_dane

# Create your tests here.
from zadanie2.models import Gmina, Kandydat_Gmina, Okręg, Województwo, Kandydat_Okręg, Kandydat_Województwo


class TestOfTests(TestCase):

    def setUp(self):
        self.jeden = 1
        self.dwa = 2

    def testTests(self):
        self.assertEquals(self.jeden + self.jeden, self.dwa)
        # self.assertEquals(True, False)

class ModelTestCase(TestCase):

    def setUp(self):
        self.lew = Gmina.objects.create(nazwa="lew", id_gminy=3453)
        self.lwi_okręg = Okręg.objects.create(numer=69, głosów_oddanych=9999)
        self.lwie_województwo = Województwo.objects.create(nazwa="Rajska Dolina", kart_wydanych=777)

        self.lew_trocki_gminny = Kandydat_Gmina.objects.create(nazwa="lew", gmina=3453)
        # self.lew_trocki_okręgowy = Kandydat_Okręg.objects.create(nazwa="lew_trocki", okręg="over")
        self.lew_trocki_okręgowy = Kandydat_Okręg.objects.create(nazwa="lew_trocki", okręg=0)
        self.lew_trocki_wojewódzki = Kandydat_Województwo.objects.create(nazwa="lew trocki", liczba_głosów = 10)

    def testCreate(self):
        self.assertEquals(self.lew.nazwa, "lew")
        self.assertEquals(self.lew.id_gminy, 3453)

        self.assertEquals(self.lwi_okręg.__str__(), '69')
        self.assertEquals(self.lwi_okręg.głosów_oddanych, 9999)

        self.assertEquals(self.lwie_województwo.__str__(), "Rajska Dolina")
        self.assertEquals(self.lwie_województwo.kart_wydanych, 777)

        self.assertEquals(self.lew_trocki_gminny.gmina, 3453)
        self.assertEquals(self.lew_trocki_gminny.__str__(), "3453 : lew")

        self.assertEquals(self.lew_trocki_okręgowy.__str__(), "0 : lew_trocki")

        self.assertEquals(self.lew_trocki_wojewódzki.__str__(), " : lew trocki")
        self.assertEquals(self.lew_trocki_wojewódzki.liczba_głosów, 10)

        # self.assertEquals(True, False)

    def testUpdate(self):
        self.lew_trocki_wojewódzki.liczba_głosów = 12
        self.assertEquals(self.lew_trocki_wojewódzki.liczba_głosów, 12)
        # self.asserEquals(True, False)

class ViewsTestCase(TestCase):

    def setUp(self):
        self.lew = Gmina.objects.create(nazwa="lew", id_gminy=3453)
        self.lwi_okręg = Okręg.objects.create(numer=69, głosów_oddanych=9999)
        self.lwie_województwo = Województwo.objects.create(nazwa_skrót="RD",
                                                           nazwa="RajskaDolina",
                                                           uprawnionych = 1000,
                                                           kart_wydanych=777,
                                                           głosów_oddanych = 100,
                                                           głosów_nieważnych = 12,
                                                           głosów_ważnych = 88)
        self.Dolnośląskie = Województwo.objects.create(nazwa="DOLNOŚLĄSKIE",
                                                       nazwa_skrót="PL-DS",
                                                       uprawnionych = 6,
                                                       kart_wydanych = 5,
                                                       głosów_oddanych = 4,
                                                       głosów_nieważnych = 3,
                                                       głosów_ważnych = 1)

        self.lew_trocki_gminny = Kandydat_Gmina.objects.create(nazwa="lew", gmina=3453)
        # self.lew_trocki_okręgowy = Kandydat_Okręg.objects.create(nazwa="lew_trocki", okręg="over")
        self.lew_trocki_okręgowy = Kandydat_Okręg.objects.create(nazwa="lew_trocki", okręg=0)
        self.lew_trocki_wojewódzki = Kandydat_Województwo.objects.create(nazwa="lew trocki", liczba_głosów = 10)


    def test_call_view_loads(self):

        response = self.client.get('/zadanie2/kraj')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kraj2.html')

        response = self.client.get('/zadanie2/województwo/PL-DS')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'województwo2.html')

        response = self.client.get('/zadanie2/gmina/3453')
        self.assertEqual( response.status_code, 200 )
        self.assertTemplateUsed(response, 'gmina2.html')

        response = self.client.post('/zadanie2/przekierujDoGminy', {'nazwa': "D"})
        # print (response)
        # Nie znaleziono gminy
        self.assertEqual( response.status_code, 403 )

        response = self.client.post('/zadanie2/przekierujDoGminy', {'nazwa': "lew"})
        # print (response)
        self.assertEqual( response.status_code, 200 )
        self.assertTemplateUsed(response, 'wyszukajGmine.html')


# load_test()
# load_kandydat()
# load_dane()

