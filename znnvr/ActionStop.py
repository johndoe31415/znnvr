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

import re
import subprocess
from .ZnnvrAction import ZnnvrAction
from .Systemd import Systemd

class ActionStop(ZnnvrAction):
	def run(self):
		ZNNVR_SERVICE_REGEX = re.compile(r"znnvr-(rec|mon).*\.service")
		for unit in Systemd.status():
			unit_name = unit["unit"]
			if ZNNVR_SERVICE_REGEX.fullmatch(unit_name) is not None:
				subprocess.run([ "systemctl", "--user", "stop", unit_name ], check = False)
