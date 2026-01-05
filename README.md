# znnvr
znnvr is the "Zero Nonsense NVR". It is intended to grab RTSP streams from a
CCTV video camera and put it into segmented files, no more, no less:

No object detection. No alerts. No triggers. No reencoding. No push
notifications. No web interface. No Docker container. No gazillion of
dependencies. No root privileges. No MariaDB database. No YAML, oh God
absolutely no YAML.

No nonsense. Just NVR.


## Why?
There are multiple F/OSS NVR solutions on the market: Frigate, ZoneMinder,
Shinobi, to name a few. I hated them all with a burning passion. I have no idea
what they are doing under the hood but the ONLY job that is actually really
important to me (record the files) isn't done in a way that I like. There's
tons of features that come at the price of killing performance on my Raspberry
Pi.

I don't want that. My usecase is this: Record to disk. Overwrite old files.
Ideally, I never review those files. If some asshat comes along and vandalizes
my garden (true story), I'll find a way to review the footage. But it needs to
be recorded and it needs to be reliable until then.


# How?
znnvr is written in Python, but all heavy lifting is done by systemd and
ffmpeg. Python code is only used to do tasks that are not performance critical,
such as deleting old recordings.


## Dependencies
Python3, ffmpeg.


## License
GNU GPL-3.
