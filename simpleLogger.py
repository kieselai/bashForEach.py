# Written by: Anthony Kiesel
# URL: https://github.com/kieselai/bashForEach.py

from colorama import init, Fore, Back
# Local imports 
import formatter

init(autoreset=True)
class SimpleLogger:
    """ Class Used to log messages to the terminal """
    @staticmethod
    def init(verboseLoggingEnabled):
        """ Initialize the logger with this function 
        Parameters: 
            verboseLoggingEnabled (boolean): switches verbose messages on/off
        """
        SimpleLogger.verboseLoggingEnabled = verboseLoggingEnabled 

    @staticmethod
    def output(*messages, **namedArgs):
        """ Print a message with optional colored output 
        Parameters: 
            *messages (string or list(string, ...)): messages to print
            foreground (string): optional named argument containing a code to set the foreground
            background (string): optional named argument containing a code to set the background
        """
        (foreground, background) = (namedArgs.get("foreground", Fore.RESET), namedArgs.get("background", Back.RESET))
        for msg in messages:
            # Make msg into a list that is 1 level deep
            msg = formatter.Formatter.FlattenList([msg])
            # Print color codes as well as the messages provided 
            print(foreground + background + "".join(msg))

    @staticmethod
    def outputVerbose(*messages):
        """ If verbose messages are enabled, print each message provided
        Parameters:
            *messages (string, or list(string)): messages to print
        """
        if (SimpleLogger.verboseLoggingEnabled):
            for m in messages: SimpleLogger.output(formatter.Formatter.CoerceToList(m), foreground=Fore.RED, background=Back.BLACK)

    @staticmethod
    def outputCommand(command):
        """ Print the command that is to be executed 
        Parameters: 
            command (string): the command to be printed
        """
        SimpleLogger.output(["\n>  ", command], foreground=Fore.CYAN, background=Back.BLACK)

# Initialize SimpleLogger to disable verbose logging by default
SimpleLogger.verboseLoggingEnabled = False
