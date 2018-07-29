import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()
def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS LIIGATILANNE(TIME INT,HPK INT, HIFK INT, ILVES INT, JUKURIT INT, JYP INT, KALPA INT, KOOKOO INT, KARPAT INT, LUKKO INT, PELICANS INT, SAIPA INT, SPORT INT, TAPPARA INT, TPS INT, ASSAT INT)")

def data_entry():
    c.execute("INSERT INTO tab VALUES(1452549219,'2016-01-11 13:53:39','Python',6)")
    conn.commit()
    c.close()
    conn.close()
    
create_table()
#data_entry()