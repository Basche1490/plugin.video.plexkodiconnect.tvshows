# -*- coding: utf-8 -*-
# We need this in order to use add-on paths like
# 'plugin://plugin.video.plexkodiconnect.MOVIES' in the Kodi video database
###############################################################################
import logging
import sys
from os import path as os_path

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

_ADDON = xbmcaddon.Addon(id='plugin.video.plexkodiconnect.tvshows')
try:
    _ADDON_PATH = _ADDON.getAddonInfo('path').decode('utf-8')
except TypeError:
    _ADDON_PATH = _ADDON.getAddonInfo('path').decode()
try:
    _BASE_RESOURCE = xbmc.translatePath(os_path.join(
        _ADDON_PATH,
        'resources',
        'lib')).decode('utf-8')
except TypeError:
    _BASE_RESOURCE = xbmc.translatePath(os_path.join(
        _ADDON_PATH,
        'resources',
        'lib')).decode()
sys.path.append(_BASE_RESOURCE)

###############################################################################
import pickler
import PKC_listitem
import utils
import loghandler
###############################################################################
loghandler.config()
LOG = logging.getLogger('PLEX.TVSHOWS')
###############################################################################

HANDLE = int(sys.argv[1])


def play():
    """
    Start up playback_starter in main Python thread
    """
    LOG.debug('Full sys.argv received: %s', sys.argv)
    # Put the request into the 'queue'
    if not sys.argv[2]:
        utils.plex_command('NAVIGATE', sys.argv[0])
    else:
        utils.plex_command('PLAY', sys.argv[2])
    # Wait for the result
    while not pickler.pickl_window('plex_result'):
        xbmc.sleep(50)
    result = pickler.unpickle_me()
    if result is None:
        LOG.error('Error encountered, aborting')
        xbmcplugin.setResolvedUrl(HANDLE, False, xbmcgui.ListItem())
    elif result.listitem:
        listitem = PKC_listitem.convert_PKC_to_listitem(result.listitem)
        xbmcplugin.setResolvedUrl(HANDLE, True, listitem)


if __name__ == '__main__':
    LOG.info('PKC add-on for tv shows started')
    play()
    LOG.info('PKC add-on for tv shows stopped')
