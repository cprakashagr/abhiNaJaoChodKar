import gi
import os
import dbus
from dbus.mainloop.glib import DBusGMainLoop

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator


APP_INDICATOR_ID = 'abhiNaJaoChodKar'

messages = []
indicator = None

class NotificationGuru:

    def __init__(self):
        indicator = appindicator.Indicator.new(APP_INDICATOR_ID, os.path.abspath('ic_alarm_add_white_24dp.png'), appindicator.IndicatorCategory.APPLICATION_STATUS)
        indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        indicator.set_menu(self.build_menu())

        DBusGMainLoop(set_as_default=True)

        bus = dbus.SessionBus()
        bus.add_match_string_non_blocking("eavesdrop=true, interface='org.freedesktop.Notifications', member='Notify'")
        bus.add_message_filter(self.notifications)

        gtk.main()

        pass

    def build_menu(self):
        menu = gtk.Menu()
        item_quit = gtk.MenuItem('Quit')
        item_quit.connect('activate', quit)
        menu.append(item_quit)
        menu.show_all()
        return menu


    def quit(self, source):
        gtk.main_quit()

    def modifyAllMenuItems(self):
        # print(indicator.get_menu())
        pass

    def notifications(self, bus, message):
        messages.append(message)
        self.modifyAllMenuItems()
        print([arg for arg in message.get_args_list()])


def main():
    NotificationGuru()
    pass


if __name__ == "__main__":
    main()
