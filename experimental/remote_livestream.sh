raspivid -o - -t 0 -w 640 -h 360 -fps 25 -n | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554}' :demux=h264
