# Local imports 
from formatter      import Formatter
from commandBuilder import CommandBuilder
from simpleLogger   import SimpleLogger
class BashForEachCommand:
    """ This class represents a templated command to be ran multiple times using different arguments """
    def __init__(self, commandString, argLists, runAllArgumentCombinations=False):
        """ Initialize the command with the provided options 
            parameters: 
            commandString (string): Template for the command to be executed
            argLists (list(list(string, string...))): 
                A list containing sub-lists with options for each argument in the command template
            runAllArgumentCombinations (boolean): This option indicates that all possible 
                combinations of the parameters in the sub-lists of argLists should be used 
        """
        self.commandTemplateString = commandString
        self.argumentLists = Formatter.FlattenArgsList(argLists)
        if self.argumentLists is not None:
            self.argumentLists = [[Formatter.ListAsString(arg) for arg in lst] for lst in self.argumentLists]
        else: SimpleLogger.outputVerbose("No arguments were provided")
        self.runAllArgumentCombinations = runAllArgumentCombinations

    def buildCommands(self):
        """ Build the command strings to be executed using the provided arguments """
        SimpleLogger.outputVerbose(
            ["Command: ", self.commandTemplateString], 
            ["Arguments: "+Formatter.ListAsString(self.argumentLists, True)]
        )
        #Use every combinations of the argument lists
        if self.runAllArgumentCombinations:
            SimpleLogger.outputVerbose("Using combinatation arguments")
            return CommandBuilder.CreateCommandsFromAllArgumentCombinations(self.commandTemplateString, self.argumentLists)
        # Use the nth item in each list for the nth command executed
        else:
            SimpleLogger.outputVerbose("Using indexed arguments")
            return CommandBuilder.CreateCommandsFromDistinctArgumentIndices(self.commandTemplateString, self.argumentLists)
