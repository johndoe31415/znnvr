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
import json
import subprocess

class Systemd():
	@classmethod
	def status(cls):
		proc = subprocess.run([ "systemctl", "--user", "-o", "json" ], check = True, capture_output = True)
		return json.loads(proc.stdout)

	@classmethod
	def loginctl_show_my_user(cls):
		proc = subprocess.run([ "loginctl", "show-user", os.environ["USER"] ], check = True, capture_output = True)
		result = { }
		for line in proc.stdout.decode("utf-8").split("\n"):
			if "=" in line:
				(key, value) = line.split("=", maxsplit = 1)
				result[key] = value
		return result

	@classmethod
	def escape(cls, cmd: list[str]):
		def _escape(arg):
			return arg.replace("%", "%%")
		return " ".join(_escape(arg) for arg in cmd)
