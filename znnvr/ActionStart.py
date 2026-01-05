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
from .ZnnvrAction import ZnnvrAction
from .Configuration import Configuration
from .Systemd import Systemd

class ActionStart(ZnnvrAction):
	def _install(self, camera: dict):
		target_dir = os.path.realpath(f"{self._config.target_directory}/{camera['identifier']}")
		os.makedirs(target_dir, exist_ok = True)
		systemd_unit_filename = os.path.expanduser(f"~/.local/share/systemd/user/{camera['systemd-rec-service']}")

		cmd = [ "/usr/bin/ffmpeg", "-hide_banner", "-nostats" ]
			#-stimeout 5000000 -rw_timeout 5000000 \
		cmd += [ "-rtsp_transport", "tcp" ]
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

	def run(self):
		self._config = Configuration(self._args.config_file)
		self._run_command([ "uninstall" ])
		print(self._args)
		for camera in self._config.cameras:
			self._install(camera)
