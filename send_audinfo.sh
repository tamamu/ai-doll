#!/bin/sh

#./aud_info.sh | ./send_message.py -f example.audacious
./aud_info.sh | ./send_message.py -f example.audacious
sleep 1

while true;
do
  ./aud_info.sh | ./send_message.py -u example.audacious &
  sleep 1
done
