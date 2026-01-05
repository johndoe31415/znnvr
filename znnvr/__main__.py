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

import sys
from .MultiCommand import MultiCommand
from .ActionStart import ActionStart
from .ActionStop import ActionStop
from .ActionUninstall import ActionUninstall

def main(args: list[str] | None = None):
	mc = MultiCommand(description = "znnvr: Zero Nonsense NVR")

	def genparser(parser):
		parser.add_argument("-c", "--config-file", metavar = "filename", default = "~/.config/znnvr_config.json", help = "Specifies the configuration file to use. Defaults to %(default)s.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity. Can be given multiple times.")
	mc.register("start", "Install/update and start systemd units that ensure the camera streams are recorded", genparser, action = ActionStart)

	def genparser(parser):
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity. Can be given multiple times.")
	mc.register("stop", "Stop all znnvr systemd units", genparser, action = ActionStop)

	def genparser(parser):
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity. Can be given multiple times.")
	mc.register("uninstall", "Remove all znnvr systemd units", genparser, action = ActionUninstall)

	returncode = mc.run(args or sys.argv[1:])
	return returncode or 0
