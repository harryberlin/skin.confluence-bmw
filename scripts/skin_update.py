#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://api.github.com/repos/harryberlin/skin.confluence-bmw/git/refs/heads/kodi_18
# https://api.github.com/repos/harryberlin/skin.confluence-bmw/git/commits/1151a83a19b3103817ea6f137229d657ebc30b07


# 'https://github.com/harryberlin/skin.confluence-bmw/zipball/kodi_18'
# "https://codeload.github.com/harryberlin/skin.confluence-bmw/legacy.zip/kodi_18"
#url = 'https://github.com/harryberlin/skin.confluence-bmw/zipball/kodi_18'
# https://github.com/harryberlin/skin.confluence-bmw/archive/ed9854b0a6329463aee099697d2d5dbd1acaef48.zip

import os
import json
import urllib, urllib2
#import datetime
import zipfile

import xbmc, xbmcgui, xbmcaddon

ADDON = xbmcaddon.Addon('skin.confluence-bmw')
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_ZIP_NAME = 'skin.confluence-bmw.zip'
ADDON_URL = 'https://github.com/harryberlin/skin.confluence-bmw/archive/kodi_18.zip'
ADDON_PATH = ADDON.getAddonInfo('path')
ADDON_USER_PATH = os.path.join(xbmc.translatePath('special://userdata'), 'addon_data', ADDON_ID)


def _pbhook(numblocks, blocksize, filesize, url=None, dp=None):
    if dp.iscanceled():
        print "Download Abgebrochen"
        raise Exception("dialog canceled")
        #dp.close()

    try:
        percent = min((numblocks * blocksize * 100) / filesize, 100)
        current_size = '%.*f' % (2, numblocks*blocksize/1024.0/1024.0)
        total_size = '%.*f' % (2, filesize/1024.0/1024.0)
        print percent
        teststr = '%s / %s MB / %s%%' % (current_size, total_size, percent)
        dp.update(int(10+percent*0.4), 'Downloading...', teststr, '%s%%' % int(10+percent*0.4))
    except:
        pass
        #percent = 100
        #dp.update(percent)


def is_internet_available():
    try:
        urllib2.urlopen('http://216.58.192.142', timeout=1)
        return True
    except:
        return False


def log(string):
    if xbmc.getCondVisibility('Skin.HasSetting(SkinDebug)'):
        xbmc.log('%s: %s' % (ADDON_ID, string), xbmc.LOGNOTICE)


def dialog_progressbar_timeout(dp, line_1, line_2, line_3, timeout=3000):
    for _ in range(100, 0, -1):
        if dp.iscanceled():
            break
        dp.update(_, line_1, line_2, line_3)
        xbmc.sleep(timeout/100)


def update(owner, repo, branch='master'):
    dp = xbmcgui.DialogProgress()
    dp.create('Updating %s' % ADDON_ID, 'Check Connection...')
    dp.update(1, 'Check Connection...', ' ', '1%')

    try:

        if not is_internet_available():
            #xbmc.executebuiltin("Notification(Skin Updater,VERBINDUNGSFEHLER!,500)")
            raise Exception('No Internet connection')

        dp.update(5, 'Check for new Version on github...', ' ', '5%')
        try:
            url = 'https://api.github.com/repos/%s/%s/git/refs/heads/%s' % (owner, repo, branch)

            res = json.loads(urllib2.urlopen(url).read())
            log(res)

            sha_url = res['object']['url']

            res = json.loads(urllib2.urlopen(sha_url).read())
            commit_date = res['committer']['date']
            sha = res['sha']
        except:
            raise Exception('Try again later')

        print sha

        if xbmc.getInfoLabel('Skin.String(github_sha)') == sha:
            raise Exception('No Update required')

        print 'downloading file'
        #download_file('https://github.com/harryberlin/skin.confluence-bmw/zipball/kodi_18', "%s\skin.confluence-bmw.zip" % (os.path.join('C:\\', 'temp')))
        #download_file("https://github.com/%s/%s/archive/%s.zip" % (owner, repo, sha), "%s\skin.confluence-bmw-%s.zip" % (os.path.join('C:\\', 'temp'), sha))
        #dialog = xbmcgui.Dialog()
        #if dialog.yesno("BMW RaspControl Skin Updater", "Are you sure to update the Skin?") == 1:
        #    pass

        dp.update(10, 'Downloading...', ' ', '10%')
        url = "https://github.com/%s/%s/archive/%s.zip" % (owner, repo, sha)
        #target_path = os.path.join(ADDON_USER_PATH, "skin.confluence-bmw-%s.zip" % sha)
        target_path = os.path.join(ADDON_USER_PATH, ADDON_ZIP_NAME)

        # https://www.programcreek.com/python/example/663/urllib.urlretrieve

        urllib.urlretrieve(url, target_path, lambda nb, bs, fs, url=url: _pbhook(nb, bs, fs, url, dp))

        dp.update(50, 'Check Zipfile...', ' ', '50%')

        the_zip_file = zipfile.ZipFile(target_path, 'r')
        ret = the_zip_file.testzip()

        if ret is not None:
            raise Exception('Zipfile is bad')

        dp.update(50, 'Checked Zipfile', ' ', '50%')

        zip_count = 0
        zip_max_count = len(the_zip_file.infolist())

        for zipinfo in the_zip_file.infolist():
            zip_count += 1
            if zipinfo.filename.endswith('.gitignore'):
                continue
            if zipinfo.filename.startswith('skin.confluence-bmw'):
                #%s' % os.path.split(zipinfo.filename)[1]
                zipinfo.filename = zipinfo.filename.replace('skin.confluence-bmw-%s' % sha, '')
                dp.update(int(50+int(float(zip_count)/float(zip_max_count)*100)*0.50), 'Extracting Files...', '%s / %s / %s%%' % (zip_count, zip_max_count, int(float(zip_count)/float(zip_max_count)*100)), '%s%%' % int(50+int(float(zip_count)/float(zip_max_count)*100)*0.50))

                try:
                    import test
                    # for testing to don't overwrite myself
                    the_zip_file.extract(zipinfo, os.path.join(ADDON_PATH, 'test'))
                except ImportError:
                    # for working release
                    the_zip_file.extract(zipinfo, ADDON_PATH)


        the_zip_file.close()

        xbmc.executebuiltin("Skin.SetString(github_sha,%s)" % sha)
        xbmc.sleep(400)
        #date_string = datetime.datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')

        xbmc.executebuiltin("Skin.SetString(github_commit_date,%s)" % (commit_date.replace('T', ' ').replace('Z', ' ')))

        dialog_progressbar_timeout(dp, 'Update finished', 'Reloading Skin...', ' ', 3000)

        #xbmc.executebuiltin("Notification(Skin Updater,Update erfolgreich!,5000)")
        xbmc.executebuiltin("ReloadSkin()")
        xbmc.executebuiltin("XBMC.UpdateLocalAddons()")

    except Exception as e:
        #dp.update(0, e.message, ' ', ' ')

        #for _ in range(10,0,-1):
        #    dp.update(_*10, e.message, ' ', ' ')
        #    xbmc.sleep(300)
        dialog_progressbar_timeout(dp, e.message, ' ', ' ', 7000)
        #xbmc.executebuiltin("Notification(Skin Updater,%s,7000)" % e.message)

    finally:
        #the_zip_file.close()
        dp.close()


def main():
    update('harryberlin', 'skin.confluence-bmw', 'kodi_18')


if __name__ == '__main__':
    main()
