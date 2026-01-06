#	znnvr - Zero Nonsense NVR
#	Copyright (C) 2026-2026 Johannes Bauer
#
#	This file is part of znnvr.
#
#	znnvr is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	znnvr is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with znnvr; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

import os
import sys
import subprocess
from .ZnnvrAction import ZnnvrAction
from .Configuration import Configuration
from .Systemd import Systemd

class ActionStart(ZnnvrAction):
	def _install(self, camera: dict):
		target_dir = os.path.realpath(f"{self._config.target_directory}/{camera['identifier']}")
		os.makedirs(target_dir, exist_ok = True)
		systemd_unit_filename = os.path.expanduser(f"~/.local/share/systemd/user/{camera['systemd-rec-service']}")

		cmd = [ "/usr/bin/ffmpeg" ]
		cmd += [ "-nostdin", "-hide_banner", "-nostats", "-loglevel", "warning" ]
		cmd += [ "-rtsp_transport", "tcp" ]
		cmd += [ "-timeout", str(round(self._config.stream_timeout_secs * 1000000)) ]
		cmd += [ "-i", camera["uri"] ]
		cmd += [ "-c", "copy" ]
		cmd += [ "-f", "segment", "-segment_time", str(self._config.segment_time_secs) ]
		cmd += [ "-reset_timestamps", "1" ]
		cmd += [ "-strftime", "1" ]
		cmd += [ f"{target_dir}/%Y_%m_%d_%H_%M_%S.mkv" ]

		with open(systemd_unit_filename, "w") as f:
			print("[Unit]", file = f)
			print(f"Description=ZNNVR recording of {camera['name']} to {target_dir}", file = f)
			print("After=network-online.target", file = f)
			print("Wants=network-online.target", file = f)
			print(file = f)
			print("[Service]", file = f)
			print(f"ExecStart={Systemd.escape(cmd)}", file = f)
			print("Restart=always", file = f)
			print("RestartSec=30", file = f)
			print(file = f)
			print("[Install]", file = f)
			print("WantedBy=default.target", file = f)

	def _validate_linger(self):
		loginctl_args = Systemd.loginctl_show_my_user()
		linger_state = loginctl_args.get("Linger")
		if linger_state != "yes":
			print(f"Warning: linger for user {os.environ['USER']} is set to \"{linger_state}\".", file = sys.stderr)
			print("This may cause your recording jobs to be terminated by systemd.", file = sys.stderr)
			print(f"To fix this, do as root: loginctl enable-linger {os.environ['USER']}", file = sys.stderr)

	def run(self):
		self._config = Configuration(self._args.config_file)
		self._run_command([ "uninstall" ])
		self._validate_linger()
		for camera in self._config.cameras:
			self._install(camera)

		subprocess.run([ "systemctl", "--user", "daemon-reload" ], check = True)
		for camera in self._config.cameras:
			subprocess.run([ "systemctl", "--user", "start", camera["systemd-rec-service"] ], check = True)
