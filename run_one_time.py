import datetime
import time
import configure_game as game
import configure_player as player
#import configure_mails as mail
#import configure_Sheet as Sheet
#import configure
#import Consol

update = False
sendMessage = False
#Consol.Message("SERVER RUN ONE TIME")
try:
        history = game.download_update_liiga(False)
        player.make_updates()
        #mail.send_mail_players_and_admin()
        if history == True:
                print('done')
                #Sheet.Sheet_Player_History()
        #Consol.Message("SERVER ONE TIME RUN DONE")
        #configure.SAVE()
except Exception as e:
        print('Fail')
        #Consol.Message("SERVER ONE TIME RUN FAILL: "+str(e))
