#!/bin/sh
reconnTimeOut=5
TERM=vt100
while /bin/true
        do /bin/socat $* 2>/dev/null
        sleep $reconnTimeOut
done
