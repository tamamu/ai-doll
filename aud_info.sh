#!/bin/sh

if ! song=`audtool current-song-tuple-data title`; then
  echo "No Playing"
else
  stat=`audtool playback-status`
  case "$stat" in
    "playing" ) mark="PLAY" ;;
    "paused" ) mark="PAUSE" ;;
    "stopped" ) mark="STOP" ;;
    * ) mark="$stat" ;;
  esac
  now=`audtool current-song-output-length`
  length=`audtool current-song-length`
  echo $mark $song $now "/" $length
fi
