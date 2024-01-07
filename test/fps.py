from airtest.core.android import Android


def demo():
    try:
        Android().get_default_device()
    except:
        return False


print(demo())
