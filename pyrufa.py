#!/usr/bin/python3

import sys
import menu
import vars

if len(sys.argv) >= 2:
    vars.defaultContext = sys.argv[1]

menu.mainMenu(vars.defaultContext)
