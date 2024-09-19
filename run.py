import datetime
import time
import configure_game as game
import configure_player as player
import configure_mails as mail
import configure_Sheet as Sheet
import configure
import Consol

configure.SAVE()
update = False
sendMessage = False
Consol.Message("SERVER ON")
try:
    while True:
        time.sleep(900)
        timeHouer = int(datetime.datetime.fromtimestamp(time.time()).strftime('%H'))
        if timeHouer == 3 or timeHouer == 5:
            update = game.download_update_liiga(update)
            configure.SAVE()
            time.sleep(3600)
        if update:
            player.make_updates()
            sendMessage = True
            update = False
            configure.SAVE()
        if sendMessage and timeHouer == 7:
            mail.send_mail_players_and_admin()
            sendMessage = False
            Sheet.Sheet_Run_List()
            configure.SAVE()
            time.sleep(3600)
except Exception as e:
    Consol.ErroMessage("SERVER FAILL: "+str(e))