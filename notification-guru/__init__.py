import gi
import os
import dbus
from dbus.mainloop.glib import DBusGMainLoop

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator

APP_INDICATOR_ID = 'abhiNaJaoChodKar'
INITIAL_FILTERS = ['gnome-settings-daemon']


class NotificationGuru:
    def __init__(self):
        self.messages = list()
        self.indicator = appindicator.Indicator.new(APP_INDICATOR_ID,
                                                    os.path.abspath('ic_notifications_active_white_24dp.png'),
                                                    appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.refresh_menu()

        DBusGMainLoop(set_as_default=True)

        self.bus = dbus.SessionBus()
        self.bus.add_match_string_non_blocking(
            "eavesdrop=true, interface='org.freedesktop.Notifications', member='Notify'")
        self.bus.add_message_filter(self.notifications)

        gtk.main()

        pass

    def refresh_menu(self):
        self.indicator.set_menu(self.build_menu())

    def build_menu(self):
        menu = gtk.Menu()
        i = 0
        for message in self.messages:
            i += 1
            strMessage = '' + message[3] + ' | ' + message[0] + ' | ' + message[4] + ''
            item = gtk.MenuItem(strMessage)
            item.set_use_underline(True)
            item.connect('activate', menuItemHandler, i-1, self)
            menu.append(item)
        item_quit = gtk.MenuItem('Quit')
        item_quit.connect('activate', self.quit)
        menu.append(item_quit)
        menu.show_all()
        return menu

    @staticmethod
    def quit(source):
        gtk.main_quit()

    def modifyAllMenuItems(self):
        self.indicator.set_menu(self.build_menu())
        pass

    def notifications(self, bus, message):
        if len(message.get_args_list()) > 1:
            msg = list(message.get_args_list())
            if INITIAL_FILTERS.__contains__(msg[0]):
                pass
            else:
                self.messages.append(msg)
                self.modifyAllMenuItems()
        print([arg for arg in message.get_args_list()])


def menuItemHandler(source, id, guru):
    del guru.messages[id]
    guru.refresh_menu()


def main():
    NotificationGuru()


if __name__ == "__main__":
    main()
