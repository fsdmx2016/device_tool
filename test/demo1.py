import os


def get_PID(package_name):
    pid = ''
    for app in package_name:
        result=os.popen('adb shell ps | findstr {}'.format(app))
        for line in result.readlines():
            line = '#'.join(line.split()) + '#'
            appstr = app + '#'
            if appstr in line:
                pid = line.split('#')[1]
    return pid
raw="adb shell logcat --pid="+get_PID("com.mt.mtxx.mtxx")+""
while True:
    result=os.popen(raw)
    for line in result.readlines():
        print(line)
