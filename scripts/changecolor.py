#!/usr/bin/env python

import xbmc, xbmcgui, xbmcaddon
import re

# -- for skin --

bDebug = False

Farben={}
print xbmcaddon.Addon(xbmc.getSkinDir()).getAddonInfo('path').decode('utf-8')
#quit()
xmlfile=xbmcaddon.Addon(xbmc.getSkinDir()).getAddonInfo('path').decode('utf-8') + '/colors/defaults.xml'
xml = open(xmlfile, 'r').read()

print xml
#xml='<?xml version="1.0" encoding="utf-8"?><colors><color name="white">FFFFFFFF</color><color name="grey">FFb4b4b4</color><color name="grey2">FF999999</color><color name="grey3">FF505050</color><color name="black">FF000000</color><color name="blue">FF0084ff</color><color name="selected">FFEB9E17</color><color name="bmwamber">FFFF7E00</color></colors>'

match=re.findall('name="(.*?)" menutextcolor="true">(.*?)</',xml)
for farbe,wert in match:
    Farben[farbe] = wert
print Farben
#print Farben['blue']
Farbliste=Farben.keys()
Wertliste=Farben.values()
print 'Farbe 0: ' + Farbliste[0]
print Farben[Farbliste[0]]
print Wertliste

#Farbliste.extend(['USERDEFINED'])

ret = xbmcgui.Dialog().select('Choose a Color', Farbliste)

print ret
print 'selected: ' + Farbliste[ret]
if bDebug: xbmcgui.Dialog().ok("Choosed color", Farbliste[ret])
if not ret < 0:	xbmc.executebuiltin('Skin.SetString(TextColor1,' + Farbliste[ret] + ')')

pass