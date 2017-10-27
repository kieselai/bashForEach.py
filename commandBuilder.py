# Written by: Anthony Kiesel
# URL: https://github.com/kieselai/bashForEach.py

import re
# Local imports 
from simpleLogger import SimpleLogger
from formatter    import Formatter
class CommandBuilder:
    @staticmethod
    def InsertCommandArguments(commandStr, params):
        """ Builds commands using a template string and a list of arguments 
            Parameters:
            commandStr (string): A template for the command to be created
            params (list(string, string...)): n parameters that will replace
                template placeholders in the command string template for the nth placeholder.
            EX: 
                commandStr="openssl dgst -{1} {0}"
                params=['testFile.txt','sha256']
                final_command="openssl dgst -sha256 testFile.txt"
        """
        SimpleLogger.outputVerbose(
            ["Command template is: ", commandStr], 
            ["Arguments are: ", Formatter.ListAsString(params, True)]
        )
        # For each parameter index, replace all "{i}" placeholders 
        # in the commandString with the parameter value
        for i in range(0, len(params)): 
            commandStr = commandStr.replace("{" + str(i) + "}", params[i])
        # Replace any parameter values that were not provided with an empty string
        commandStr = re.sub(r'\{[0-9]+\}', '', commandStr)
        SimpleLogger.outputVerbose(["Final command is: ", commandStr])
        return commandStr

    @staticmethod
    def InsertCommandArgumentsForEach(commandStr, parameterLists):
        """ For each argument list in parameterLists, build a command string using those options.
        Parameters:
            commandStr (string): Template for the command to be executed
            parameterLists (list(list(string, string...))):  Each list contains the parameters to 
                replace the template placeholders in the command and represents the options of a distinct command.
        """
        cmds = []
        for idx in range(0, len(parameterLists)):
            # The nth command
            SimpleLogger.outputVerbose(["\n", "Command number: ", str(idx)])
            # Append the nth command to the return array
            cmds.append(CommandBuilder.InsertCommandArguments(commandStr, parameterLists[idx]))
        return cmds

    @staticmethod
    def CreateCommandsFromDistinctArgumentIndices(commandStr, argLists):
        """ Create n commands from argLists, pairing command parameters by sub-list index.
            The ith list coorelates to the ith parameter
            The nth option in each list is used to build the nth command.
        Parameters:
            commandStr (string): Template for the command to be created
            argLists (list(list(string, string...))): contains options for each of the parameters to be used
        """
        if isinstance(argLists, list) and len(argLists) > 0:
            pairedArgs = [[lst[i] for lst in argLists] for i in range(0, len(argLists[0]))]
            SimpleLogger.outputVerbose(["Index Paired Arguments: ", Formatter.ListAsString(pairedArgs, True)])
            return CommandBuilder.InsertCommandArgumentsForEach(commandStr, pairedArgs)

    @staticmethod
    def GetAllArgumentCombinations(argLists):
        """ Takes several lists with at least one element and returns a list containing 
            possible combinations between all of the lists.
            The ith list can be used only in the ith position of all possible combinations
            Parameters: 
                argLists (list(list(string, string, ...))): 
                Each sub-list (the ith list) contains the possible options to be used in the ith place of a combination list.
         """
        if isinstance(argLists, list) and len(argLists) > 0:
            combinations = [[c] for c in argLists[0]]
            for lst in argLists[1:]:
                combinations = [existingCombination + [option] for existingCombination in combinations for option in lst]
            SimpleLogger.outputVerbose(["Combinations: ", Formatter.ListAsString(combinations, True)])
            return combinations

    @staticmethod
    def CreateCommandsFromAllArgumentCombinations(commandStr, argLists):
        """ Create commands representing every combination of the supplied options of sub-lists in argLists 
        Parameters: 
            commandStr (string): Template for the command to be created
            argLists (list(list(string, string...))): contains options for each of the parameters to be used
        """
        if not isinstance(argLists, list): return
        comboArgs = CommandBuilder.GetAllArgumentCombinations(argLists)
        return CommandBuilder.InsertCommandArgumentsForEach(commandStr, comboArgs)
