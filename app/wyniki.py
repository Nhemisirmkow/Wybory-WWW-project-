import csv

'''
from jinja2 import Environment, PackageLoader
from jinja2 import select_autoescape
'''

data = '/home/nicram/PycharmProjects/wybory2/pkw2000.csv'

'''
env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template("index.html")


class Pokemon:
    def __init__(self, name, number):
        self.name = name;
        self.number = number


pokemons = [
    Pokemon("Pikachu", 25),
    Pokemon("Raichu", 26)
]

xs = [[1, 2, 3, 4]]



with open("output.html", "w") as out:
    number = 42
    string = "siedemnaście"
    out.write(template.render(locals()))
'''

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

głosy={}


with open(data) as file:
    reader = csv.reader(file)
    for row in reader:
        if row[3] != 'Gmina':

            kandydaci={
                'Dariusz Maciej GRABOWSKI':row[11],
                'Piotr IKONOWICZ':row[12],
                'Jarosław KALINOWSKI':row[13],
                'Janusz KORWIN - MIKKE':row[14],
                'Marian KRZAKLEWSKI':row[15],
                'Aleksander KWAŚNIEWSKI':row[16],
                'Andrzej LEPPER':row[17],
                'Jan ŁOPUSZAŃSKI':row[18],
                'Andrzej Marian OLECHOWSKI':row[19],
                'Bogdan PAWŁOWSKI':row[20],
                'Lech WAŁĘSA':row[21],
                'Tadeusz Adam WILECKI':row[22],
                'TEST1':234,
                'TEST2':4234,
            }

            wyniki = {
                'obwody':row[5],
                'uprawnieni':row[6],
                'karty wydane':row[7],
                'głosy oddane':row[8],
                'głosy nieważne':row[9],
                'głosy ważne':row[10],
                'kandydaci':kandydaci,
            }

            if row[0] not in głosy:
                głosy[row[0]] = {}
            if row[1] not in głosy[row[0]]:
                głosy[row[0]][row[1]] = {}
            if row[2] not in głosy[row[0]][row[1]]:
                głosy[row[0]][row[1]][row[2]] = {}
            głosy[row[0]][row[1]][row[2]]=[
                row[3],
                row[4],
                wyniki
            ]

"""
                with open(row[4]+".html", "w") as out:
                kodGminy=row[3]
                wyniki=row[4]
                out.write(template.render(leocals()))
            """