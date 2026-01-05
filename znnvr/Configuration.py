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
import re
import json

class Configuration():
	def __init__(self, filename: str):
		self._filename = filename
		with open(os.path.expanduser(filename)) as f:
			self._config = json.load(f)
		self._finalize_config()

	def _finalize_config(self):
		if len(self.camera_names) != len(set(self.camera_names)):
			raise ValueError(f"Configuration file {self._filename} has error: duplicate camera names found")

		REPL_RE = re.compile(r"[^a-zA-Z0-9]+")
		identifiers = set()
		for camera in self.cameras:
			identifier = REPL_RE.sub("-", camera["name"].lower())
			if identifier in identifiers:
				raise ValueError(f"Configuration file {self._filename} has error: camera {camera['name']} has duplicate identifier {identifier}")
			identifiers.add(identifier)
			camera["identifier"] = identifier
			camera["systemd-rec-service"] = f"znnvr-rec-{identifier}.service"

	@property
	def cameras(self):
		return self._config.get("cameras", [ ])

	@property
	def camera_names(self):
		return [ camera["name"] for camera in self.cameras ]

	@property
	def target_directory(self):
		return self._config["target_directory"]

	@property
	def segment_time_secs(self):
		return self._config.get("segment_time_secs", 900)
