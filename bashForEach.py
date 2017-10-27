#!/usr/bin/python

# Written by: Anthony Kiesel
# URL: https://github.com/kieselai/bashForEach.py

import argparse

# Local imports 
from bashForEachCommand import BashForEachCommand
from commandTaskRunner  import CommandTaskRunner
from formatter          import Formatter
from simpleLogger       import SimpleLogger


def bashForEach(commandTemplateString, argumentLists, runAllArgumentCombinations=False, logVerbose=False):
    """ This function takes a templated command and uses argument lists for each parameter to run the 
        command several times using different options for the templated arguments.  
        EX:  commandTemplateString = "openssl dgst -{1} {0}"
        Each argument list given correlates to an index in the command string template.
        The first  argument list (argumentLists[0]) would contain options to be used at index 0.
        The second argument list (argumentLists[1]) would contain options to be used at index 1.
        Any additional lists would correlate to increasing index numbers.

        parameters: 
        commandTemplateString (string): contains a templated command to execute.
        argumentLists (list(list(string, string...)): a list of lists containing strings.  
            The nth list contains options for the nth argument in the command template string.
        runAllArgumentCombinations (boolean): This is a flag that tells the application to
            run all possible combinations of the provided arguments.  
            The default is simply to pair arguments based on their index. 
            Without this flag set, the nth item in every list will be used to execute the nth command.
        logVerbose (boolean): This option tells the program to print extra info to the screen.
    """
    # Set logger to print verbose messages
    SimpleLogger.init(logVerbose)
    cmd = BashForEachCommand(commandTemplateString, argumentLists, runAllArgumentCombinations)
    #If arguments were provided
    if cmd.argumentLists is not None:
        commandsToRun = cmd.buildCommands()
        CommandTaskRunner.runMultiple(commandsToRun)  # Run all commands

# If running from command line rather than through an import statement
if __name__ == "__main__":
    _args_help_msg = """
        For each set of arguments to be used in the given command, 
        use the --args flag followed by a list of arguments to be 
        used for the nth argument position.
        ===================================================
        EX:
        ===================================================
        --args fileone.txt filetwo.txt filethree.txt
        --args someoption_1 someoption_2 someoption_3
    """
    _combos_help_msg = """
        Flag that specifies that Combination Arguments 
        are used instead of Indexed Arguments.
        ===================================================
        Indexed Arguments:
            Each argument list is expected to be the 
            same length.

            The number of commands is equal to the 
            number of arguments provided in each list.

            The nth element in all of the argument 
            lists coorelates to the nth command 
            executed.

            Likewise, the nth argument list contains a 
            list of each option to be ran with the nth 
            argument.
        ===================================================
        Combination Arguments:
            Argument lists can be any length greater 
            than 0.

            The number of commmands is equal to the 
            number of possible combinations of all 
            argument lists.

            For each argument list, each option in the 
            list is combined with all possible options 
            from previous argument lists.

            The nth argument list correlates to the nth 
            argument placeholder index.
    """
    # Create a command line interface
    parser = argparse.ArgumentParser()
    addArg = parser.add_argument
    parser.add_argument('--cmd',           action='store',      dest='cmd',          type=str)
    parser.add_argument('--args',          action='append',     dest='argumentList', type=list,     help=_args_help_msg, nargs='+')
    parser.add_argument('--combos',        action='store_true', dest='runCombos',    default=False, help=_combos_help_msg)
    parser.add_argument('-v', '--verbose', action='store_true', dest='logVerbose',   default=False)
    args = parser.parse_args()
    # Use arguments provided from command line to run commands
    bashForEach(args.cmd, args.argumentList, args.runCombos, args.logVerbose)
