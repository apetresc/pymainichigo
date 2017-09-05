from subprocess import call

from xvfbwrapper import Xvfb


with Xvfb(width=1024, height=768, colordepth=24) as xvfb:
    call(['processing-java', '--sketch=/home/apetresc/dev/personal/dailygo/goban', '--run'])
