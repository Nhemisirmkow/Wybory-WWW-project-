from jinja2 import Environment, PackageLoader
from jinja2 import select_autoescape
from app.kandydaci import Kandydaci_Test
from app.kandydaci import Kandydaci
'''
    głosy["województwo"]["nr okręgu"]["kod gminy"] -> "nazwa gminy",
                                                      "powiat",
                                                      wyniki -> obwody,
                                                                uprawnieni,
                                                                karty wydane,
                                                                głosy oddane,
                                                                głosy nieważne,
                                                                głosy ważne,
                                                                kandydaci -> ...

'''

env = Environment(
        loader=PackageLoader('app', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
        )

template = env.get_template("okręg.html")

from app.wyniki import głosy

for województwo in głosy:
    for okręg in głosy[województwo]:
        liczba_gmin = len(głosy[województwo][okręg])
        okręg_nazwa = okręg;
        liczba_uprawnionych = 0
        liczba_kart_wydanych = 0
        liczba_głosów_oddanych = 0
        liczba_głosów_nieważnych = 0
        liczba_głosów_ważnych = 0
        kandydaci = Kandydaci
        gminy = głosy[województwo][okręg]
        # gminy2 = sorted([x for x in gminy], key = lambda element: element[0])
        for kandydat in kandydaci:
            kandydat[2] = 0
        liczba_wszystkich_głosów = 0
        for gmina in głosy[województwo][okręg]:
            # gmina_nazwa = głosy[województwo][okręg][gmina][0]
            # if gmina_nazwa != 'Boguchwała' : continue
            # liczba_obwodów += głosy[województwo][okręg][gmina][2]['obwody']
            liczba_uprawnionych += int (głosy[województwo][okręg][gmina][2]['uprawnieni'])
            liczba_kart_wydanych += int (głosy[województwo][okręg][gmina][2]['karty wydane'])
            liczba_głosów_oddanych += int (głosy[województwo][okręg][gmina][2]['głosy oddane'])
            liczba_głosów_nieważnych += int (głosy[województwo][okręg][gmina][2]['głosy nieważne'])
            liczba_głosów_ważnych += int (głosy[województwo][okręg][gmina][2]['głosy ważne'])
            kandydaci_głosy = głosy[województwo][okręg][gmina][2]['kandydaci']
            for kandydat in kandydaci:
                kandydat[2] += int (kandydaci_głosy[kandydat[0]])
                liczba_wszystkich_głosów += int (kandydaci_głosy[kandydat[0]])
        for kandydat in kandydaci:
            #kandydat['wynik procentowy'] = kandydat['wynik'] / liczba_wszystkich_głosów
            kandydat[3] = 100 * (kandydat[2] / liczba_wszystkich_głosów)
        with open("output/okręg/" + okręg + ".html", "w") as out:
            out.write(template.render(locals()))
