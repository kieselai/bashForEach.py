# Written by: Anthony Kiesel
# URL: https://github.com/kieselai/bashForEach.py

import os
# Local imports 
from simpleLogger import SimpleLogger

class CommandTaskRunner:
    @staticmethod
    def runSingle(cmd):
        """ Run a single Command
        Parameters:
            cmd: string 
        """
        SimpleLogger.outputCommand(cmd)
        os.system(cmd)
    @staticmethod
    def runMultiple(cmds):
        """ Run every command provided in cmds 
        Paramters:
            cmds: list(string)
        """
        for cmd in cmds: CommandTaskRunner.runSingle(cmd)
