from jinja2 import Environment, PackageLoader
from jinja2 import select_autoescape

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

template = env.get_template("gmina.html")

from app.wyniki import głosy

for województwo in głosy:
    for okręg in głosy[województwo]:
        for gmina in głosy[województwo][okręg]:
            gmina_nazwa = głosy[województwo][okręg][gmina][0]
            liczba_obwodów = głosy[województwo][okręg][gmina][2]['obwody']
            liczba_uprawnionych = głosy[województwo][okręg][gmina][2]['uprawnieni']
            liczba_kart_wydanych = głosy[województwo][okręg][gmina][2]['karty wydane']
            liczba_głosów_oddanych = głosy[województwo][okręg][gmina][2]['głosy oddane']
            liczba_głosów_nieważnych = głosy[województwo][okręg][gmina][2]['głosy nieważne']
            liczba_głosów_ważnych = głosy[województwo][okręg][gmina][2]['głosy ważne']
            kandydaci = Kandydaci
            kandydaci_głosy = głosy[województwo][okręg][gmina][2]['kandydaci']
            liczba_wszystkich_głosów = 0
            for kandydat in kandydaci:
                kandydat[2] = int (kandydaci_głosy[kandydat[0]])
                liczba_wszystkich_głosów += kandydat[2]
            for kandydat in kandydaci:
                #kandydat['wynik procentowy'] = kandydat['wynik'] / liczba_wszystkich_głosów
                kandydat[3] = 100 * (kandydat[2] / liczba_wszystkich_głosów)
            with open("output/gmina/" + głosy[województwo][okręg][gmina][0] + ".html", "w") as out:
                out.write(template.render(locals()))
