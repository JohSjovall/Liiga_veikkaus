import csv

def csv_read_test(dokument_name):
    with open(dokument_name+'.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for line in csv_reader:
            TeamList=[]
            puutuva = False
            liikaa = []
            joukkue = ['HPK', 'HIFK', 'ILVES', 'JUKURIT', 'JYP', 'KALPA', 'KARPAT', 'LUKKO', 'PELICANS', 'SAIPA', 'SPORT', 'TAPPARA', 'TPS', 'ASSAT', 'KOOKOO']
            for x in range(5,20):
                if line[x] in TeamList:
                    liikaa.append(line[x])
                    puutuva = True
                else:
                    TeamList.append(line[x])
            if puutuva:
                print(line[3],line[4],line[1])
                print("listassa esiintyy useasti",liikaa)
                for x in TeamList:
                    if x in joukkue:
                        joukkue.remove(x)
                    else:
                        pass
                print("listasta puuttuu:",joukkue)
            else:
                pass
csv_read_test('testi')