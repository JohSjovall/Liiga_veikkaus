import datetime
import time
import configure_game as game
import configure_player as player
import configure_mails as mail
import Consol

update = False
sendMessage = False
Consol.Message("SERVER ON")
try:
    while True:
        timeHouer = int(datetime.datetime.fromtimestamp(time.time()).strftime('%H'))
        if timeHouer == 3 or timeHouer == 5:
            update = game.download_update_liiga(update)
        if update:
            player.make_updates()
            sendMessage = True
            update = False
        if sendMessage and timeHouer == 7:
            sendMessage = False
        time.sleep(3600)
except Exception as e:
    Consol.Message("SERVER FAILL: "+e)