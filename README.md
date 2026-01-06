# znnvr
znnvr is the "Zero Nonsense NVR". It is intended to grab RTSP streams from a
CCTV video camera and put it into segmented files, no more, no less:

No object detection. No alerts. No triggers. No reencoding. No push
notifications. No web interface. No Docker container. No gazillion of
dependencies. No root privileges. No MariaDB database. No zones. No machine
learning. No bird identification. No YAML, oh God absolutely no YAML.

No nonsense. Just record video reliably, unmodified.


## Why?
There are multiple F/OSS NVR solutions on the market: Frigate, ZoneMinder,
Shinobi, to name a few. I hated them all with a burning passion. I have no idea
what they are doing under the hood but the ONLY job that is actually really
important to me (record the files) isn't done in a way that I like: it simply
does not work reliably.  The camera I'm using has a fairly large sensor and
people usually reduce the image quality to get detection/inference going.

There's tons of features that come at the price of killing performance on my
Raspberry Pi. Features I do not want and features I do not need. Features that
actually break the main thing I want (recording video).

I dislike that. My usecase is this: Record to disk. Overwrite old files.
Ideally, I never have to review those files. If some asshat comes along and
vandalizes my garden (true story), I'll find a way to review the footage.
Possibly use [dvr-scan](https://github.com/Breakthrough/DVR-Scan) on a more
capable computer (with GPU support) to find movement. But the NVR only needs to
reliably record. It has one job only and that is it.


# How?
znnvr is written in Python, but all heavy lifting is done by systemd and
ffmpeg. Python code is only used to do tasks that are not performance critical,
such as deleting old recordings.


## Usage
Place your configuration file in `~/.config/znnvr.json`. See the example file
provided, it should be self-explanatory. Then:

```
$ znnvr start
```

That's it. It will create a systemd unit for each of your cameras and start
recording. Do you hate `znnvr` and want to get rid of it? Be my guest:

```
$ znnvr uninstall
```

## Dependencies
Python3, ffmpeg.


## License
GNU GPL-3.
