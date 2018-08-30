import sqlite3
import Consol
import time

conn = sqlite3.connect('Database_liiga_game.db')
c = conn.cursor()

def games_name():
    c.execute("SELECT Game_ID, Game_Name FROM GAMES")
    games_list = c.fetchall()
    if games_list == []:
        print('NO GAMES')
    else:
        for game in games_list:
            print(str(game[0])+'. '+game[1])
def admins_list():
    print('-----------------------')
    c.execute("SELECT Admin_ID, First_Name, Last_Name, Mail, Games_ID FROM ADMINS")
    admin_list = c.fetchall()
    if admin_list != []:
        for admin in admin_list:
                print(str(admin[0])+'. '+admin[1]+' '+admin[2]+' '+admin[3]+' '+admin[4])
    else:
        print('NO ADMINS')
    print('-----------------------')
def admins_name():
    c.execute("SELECT Admin_ID, First_Name, Last_Name FROM ADMINS")
    admin_list = c.fetchall()
    if admin_list != []:
        for admin in admin_list:
                print(str(admin[0])+'. '+admin[1]+' '+admin[2])
    else:
        print('NO ADMINS')
def add_admin(First_Name, Last_Name, Mail, Games_ID):
    c.execute("INSERT INTO ADMINS (First_Name, Last_Name, Mail, Games_ID) VALUES (?,?,?,?)",(First_Name, Last_Name, Mail, Games_ID))
    conn.commit()
def make_admin():
    First_Name = input('First Name: ')
    Last_Name = input('Last Name: ')
    Mail = input('Mail: ')
    games_name()
    Games_ID = str(input('Games ID: '))
    add_admin(First_Name.upper(), Last_Name.upper(), Mail, Games_ID)
    print(First_Name+' '+Last_Name+' '+Mail+' '+Games_ID)
def delete_admin():
    c.execute("SELECT Admin_ID, First_Name, Last_Name FROM ADMINS")
    admin_list = c.fetchall()
    if admin_list != []:
        for admin in admin_list:
                print(str(admin[0])+'. '+admin[1]+' '+admin[2])
        delete = str(input('DELETE ADMIN NUMBERS: '))
        for admin in delete:
            c.execute("DELETE FROM ADMINS WHERE Admin_ID = ?",(admin,))
            conn.commit()
    else:
        print('NO ADMINS')

on = True
while on:
    admins_list()
    inputs = input("ADD(A) DELETE(D) QUIT(Q): ")
    if inputs.upper() == 'A':
        make_admin()
    if inputs.upper() == 'D':
        delete_admin()
    if inputs.upper() == 'Q':
        on = False