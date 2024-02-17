#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  SunPeng
@Date    :  2024/1/11 17:38
@Desc    :
"""

import subprocess
import re


def get_fps_data(package_name):
    try:
        cmd = f"adb shell dumpsys gfxinfo {package_name}"
        result = subprocess.run(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout

        # Parse the FPS data from the output
        frame_stats_pattern = re.compile(r'(?<=---PROFILEDATA---[\s\S]*?Total frames rendered:)\s*(\d+)')
        match = frame_stats_pattern.search(output)
        if match:
            total_frames_rendered = int(match.group(1).strip())
            print(f"Total frames rendered: {total_frames_rendered}")
            # Additional parsing can be added here to extract more detailed FPS info

            return total_frames_rendered
        else:
            print("Could not find FPS data.")
            return None
    except subprocess.CalledProcessError as e:
        print("An error occurred while fetching FPS data: ", e)
        return None
