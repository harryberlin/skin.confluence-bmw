#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'harryberlin'

import xbmc

# https://kodi.wiki/view/List_of_built-in_functions

KODI_ACTIONS = {'Playlist': 'Action(Playlist)',
                'Screenshot': 'Action(Screenshot)',
                'Favourites': 'ActivateWindow(Favourites)',
                'Mute': 'Action(Mute)',
                'Info': 'Action(Info)',
                'Fullscreen': 'Action(FullScreen)',
                'Stepforward': 'Action(StepForward)',
                'Stepback': 'Action(StepBack)',
                'K:Left': 'Action(Left)',
                'K:Right': 'Action(Right)',
                'K:Up': 'Action(Up)',
                'K:Down': 'Action(Down)',
                'K:Back': 'Action(Back)',
                'K:Context': 'Action(ContextMenu)',
                'OSD': 'Action(OSD)',
                'Volume +': 'Action(VolumeUp)',
                'Volume -': 'Action(VolumeDown)',
                'Show Subtitles': 'Action(ShowSubtitles)',
                'Show Video Menu': 'Action(ShowVideoMenu)',
                'Home': 'ActivateWindow(Home)',
                'Music': 'ActivateWindow(Music)',
                'Player': 'ActivateWindow(1135)',
                'Repeat': 'PlayerControl(Repeat)',
                'Random': 'PlayerControl(Random)'
                }

def log(string, lvl = 0):
    return xbmc.log('IBUSCOMMUNICATOR: %s' % string, xbmc.LOGNOTICE)


def note(heading, message = None, time = 5000):
    import xbmcgui
    xbmcgui.Dialog().notification(heading='%s' % heading, message='%s' % message if message else '', icon=ICON, time=time)
    log('NOTIFICATION: "%s%s"' % (heading, ' - %s' % message if message else ''))


def dialog_ok(label1, label2 = '', label3 = ''):
    import xbmcgui
    return xbmcgui.Dialog().ok('IBusCommunicator', label1, label2, label3)


def set_skin_string(skin_string):
    import xbmcgui

    favmusicpath = 'Favorite Music Path'
    favvideopath = 'Favorite Video Path'
    custom = '-- CUSTOM --'
    reset = '---- RESET ---'
    kodi_actions = sorted(KODI_ACTIONS.keys())
    kodi_actions.extend([favmusicpath,
                         favvideopath,
                         custom,
                         reset])
    selected = xbmcgui.Dialog().select('Choose Kodi Function', kodi_actions)
    if selected != -1:
        if kodi_actions[selected] == reset:
            xbmc.executebuiltin("Skin.Reset(%s)" % skin_string)
        elif kodi_actions[selected] == custom:
            response = xbmcgui.Dialog().input('Custom Kodi Function eingeben')
            if response == '':
                return
            xbmc.executebuiltin("Skin.SetString(%s,%s)" % (skin_string, response))
        elif kodi_actions[selected] == favmusicpath:
            response = xbmcgui.Dialog().browseSingle(0, favmusicpath, '', '', False, False, '')
            if response == '':
                return
            xbmc.executebuiltin("Skin.SetString(%s,%s)" % (skin_string, 'ActivateWindow(Music,%s)' % response))
        elif kodi_actions[selected] == favvideopath:
            response = xbmcgui.Dialog().browseSingle(0, favvideopath, '', '', False, False, '')
            if response == '':
                return
            xbmc.executebuiltin("Skin.SetString(%s,%s)" % (skin_string, 'ActivateWindow(Video,%s)' % response))
        else:
            xbmc.executebuiltin("Skin.SetString(%s,%s)" % (skin_string, kodi_actions[selected]))

    xbmc.sleep(1000)


def execute_skin_string(skin_string):
    skin_string = xbmc.getInfoLabel('$INFO[Skin.String(%s)]' % skin_string)
    #dialog_ok('',skin_string)
    if skin_string in KODI_ACTIONS.keys():

        xbmc.executebuiltin('%s' % KODI_ACTIONS.get(skin_string))
    else:
        xbmc.executebuiltin('%s' % skin_string)


def main():
    # Start Script
    # RunScript("special://skin/scripts/kodi_actions.py","command;skinstring")
    count = len(sys.argv) - 1
    if count > 0:
        given_args = sys.argv[1].split(';')
        if given_args[0].lower() == 'set':
            set_skin_string(given_args[1])

        if given_args[0].lower() == 'exec':
            execute_skin_string(given_args[1])

    else:
        # no params
        pass


if __name__ == '__main__':
    main()
