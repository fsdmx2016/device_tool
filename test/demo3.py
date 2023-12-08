from airtest.core.android import Android

dev = Android()
while True:
    print(dev.logcat("com.mt.mtxx.mtxx", "*:W", 60))