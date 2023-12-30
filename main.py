from datetime import datetime
from time import sleep
import dbus

# https://github.com/gajim/gajim/blob/6c69081dd4b722c87b8a76956b61340dc26304ff/gajim/remote.py#L30
OBJ_PATH = '/org/gajim/dbus/RemoteObject'
INTERFACE = 'org.gajim.dbus.RemoteInterface'
SERVICE = 'org.gajim.Gajim'

class GajimNYCountdown:
    def __init__(self) -> None:
        self.gajim = dbus.Interface(dbus.SessionBus().get_object(SERVICE, OBJ_PATH), INTERFACE)
        self.accs = self.gajim.list_accounts()
        self.completed = False

        now = datetime.now()
        self.nextyear = now.year+1

    def change_stat(self, acc: str, stat: str) -> None:
        self.gajim.change_status(self.gajim.get_status(""), stat, acc) 

    def update_stats(self) -> None:
        now = datetime.now()
        nextyearstr = f"00:00:00 01/01/{self.nextyear}"
        end = datetime.strptime(nextyearstr, "%H:%M:%S %d/%m/%Y")

        try:
            passed = datetime.strptime(str(end-now), "%H:%M:%S.%f")
        except:
            for a in self.accs:
                self.change_stat(a, "🥳🎉🥳🎉")
            self.completed = True
            return
        
        rhours = int(passed.strftime("%H")) 
        rmin   = int(passed.strftime("%M")) 
        rsec   = int(passed.strftime("%S")) 
        format = f"{rhours}h {rmin}m {rsec}s..."

        if rhours == 0 and rmin != 0 and rsec != 0:
            format = f"{rmin}m {rsec}s..."
        elif rhours == 0 and rmin == 0 and rsec != 0:
            format = f"🥁 {rsec} 🥁"
        elif rhours == 0 and rmin == 0 and rsec == 0:
            format = "🥁🥁🥁🥁🥁🥁"

        for a in self.accs:
            self.change_stat(a, format)

    def start(self):
        while not self.completed:
            self.update_stats()
            sleep(1)

if __name__ == "__main__":
    gc = GajimNYCountdown()
    gc.start()
