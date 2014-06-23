subsonic-xbmc-addon
===================

subsonic addon for xbmc

![screenshot](screenshot.jpg)

## Install
1. `curl -L https://github.com/xsteadfastx/subsonic-xbmc-addon/archive/master.zip -o subsonic.zip`
2. `cp -Rv subsonic-xbmc-addon/plugin.audio.subsonic ~/.xbmc/addons/`
3. Configure your url, username and password

## Workarounds
There is a problem that xbmc doesnt play the next song in queue. a workaround is to put the playercorefactory file in the userdata folder. this switches the default player to "dvdplayer" for subsonic. you do that with:
      cp userdata/playercorefactory.xml ~/.xbmc/userdata/

This creates another problem with playing some flac files. it looks like the xbmc dvdplayer has a problem with some mp3 transcoded flac files. you can disable the transcoding with setting "format" to "raw" in the addon-settings. remember the file size is the original one with this setting. a other way to play the transcoded files is using the context menu on a file "play with PAPPlayer". 
