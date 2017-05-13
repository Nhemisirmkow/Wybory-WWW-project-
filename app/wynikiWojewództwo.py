from jinja2 import Environment, PackageLoader
from jinja2 import select_autoescape
from app.kandydaci import Kandydaci_Test
from app.kandydaci import Kandydaci
from app.dane import województwo_skrót
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

template = env.get_template("województwo.html")

from app.wyniki import głosy

for województwo in głosy:
    okręgi = {}
    województwo_nazwa = województwo
    liczba_okręgów = len(głosy[województwo])
    liczba_uprawnionych = 0
    liczba_kart_wydanych = 0
    liczba_głosów_oddanych = 0
    liczba_głosów_nieważnych = 0
    liczba_głosów_ważnych = 0
    kandydaci = Kandydaci
    liczba_wszystkich_głosów = 0
    for kandydat in kandydaci:
        kandydat[2] = 0

    for okręg in głosy[województwo]:
        okręgi[okręg] = {}
        okręgi[okręg]['uprawnieni'] = 0
        okręgi[okręg]['karty wydane'] = 0
        okręgi[okręg]['głosy oddane'] = 0
        okręgi[okręg]['głosy nieważne'] = 0
        okręgi[okręg]['głosy ważne'] = 0
        # gminy2 = sorted([x for x in gminy], key = lambda element: element[0])
        for gmina in głosy[województwo][okręg]:
            # gmina_nazwa = głosy[województwo][okręg][gmina][0]
            # if gmina_nazwa != 'Boguchwała' : continue
            # liczba_obwodów += głosy[województwo][okręg][gmina][2]['obwody']
            okręgi[okręg]['uprawnieni'] += int (głosy[województwo][okręg][gmina][2]['uprawnieni'])
            liczba_uprawnionych += int (głosy[województwo][okręg][gmina][2]['uprawnieni'])
            okręgi[okręg]['karty wydane'] += int (głosy[województwo][okręg][gmina][2]['karty wydane'])
            liczba_kart_wydanych += int (głosy[województwo][okręg][gmina][2]['karty wydane'])
            okręgi[okręg]['głosy oddane'] += int (głosy[województwo][okręg][gmina][2]['głosy oddane'])
            liczba_głosów_oddanych += int (głosy[województwo][okręg][gmina][2]['głosy oddane'])
            okręgi[okręg]['głosy nieważne'] += int (głosy[województwo][okręg][gmina][2]['głosy nieważne'])
            liczba_głosów_nieważnych += int (głosy[województwo][okręg][gmina][2]['głosy nieważne'])
            okręgi[okręg]['głosy ważne'] += int (głosy[województwo][okręg][gmina][2]['głosy ważne'])
            liczba_głosów_ważnych += int (głosy[województwo][okręg][gmina][2]['głosy ważne'])
            kandydaci_głosy = głosy[województwo][okręg][gmina][2]['kandydaci']
            for kandydat in kandydaci:
                kandydat[2] += int (kandydaci_głosy[kandydat[0]])
                liczba_wszystkich_głosów += int (kandydaci_głosy[kandydat[0]])
    for kandydat in kandydaci:
        #kandydat['wynik procentowy'] = kandydat['wynik'] / liczba_wszystkich_głosów
        kandydat[3] = 100 * (kandydat[2] / liczba_wszystkich_głosów)
    with open("../output/województwo/PL-" + województwo_skrót[województwo] + ".html", "w") as out:
        out.write(template.render(locals()))
