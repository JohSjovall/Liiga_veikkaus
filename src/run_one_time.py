import datetime
import time
import configure_game as game
import configure_player as player
import configure_mails as mail
import configure_Sheet as Sheet
import configure
import Consol

update = False
sendMessage = False
Consol.Message("SERVER RUN ONE TIME")
try:
        #Sheet.Sheet_Run_List()
        history = game.download_update_liiga(False)
        player.make_updates()
        history = True
        if history == True:
               player.make_updates()
               mail.send_mail_players_and_admin()
        #      Sheet.Sheet_Run_List()
               Consol.Message("SERVER ONE TIME RUN DONE")
        configure.SAVE()
except Exception as e:
        print('Fail')
        Consol.Message("SERVER ONE TIME RUN FAILL: "+str(e))
