# Written by: Anthony Kiesel
# URL: https://github.com/kieselai/bashForEach.py

import sys, os, argparse, re

# Local imports 
import simpleLogger
SimpleLogger = simpleLogger.SimpleLogger

class Formatter:
    """ Utility class to format strings and lists in various formats """
    @staticmethod
    def wrapStringIfTrue(doWrap, toPrefix, toAppend, stringToWrap):
        """ Add a string before and after a given string if the 'doWrap' condition is True
        Parameters:
            doWrap (boolean): Indicates whether or not to modify the original string
            toPrefix (string): This is the string to put in front of the 'stringToWrap'
            toAppend (string): This is the string to put after the 'stringToWrap'
            stringToWrap (string): This is the string to wrap with the 'toPrefix' 
                string in front and the 'toAppend' string at the end of the string.
        """
        return stringToWrap if not doWrap else toPrefix + stringToWrap + toAppend

    @staticmethod
    def ListAsString(lst, prettyFormat=False):
        """ Returns a string representing the list 
        Parameters: 
            lst (list or str): The list to represent as a string or a string to simply return
            prettyFormat (boolean): indicates whether or not to print brackets around a list
                or single quotes around a string.
        """
        if isinstance(lst, str): return Formatter.wrapStringIfTrue(prettyFormat, "'", "'", lst)
        elif isinstance(lst, list):
            formatted = ",".join([Formatter.ListAsString(el, prettyFormat) for el in lst])
            return Formatter.wrapStringIfTrue(prettyFormat, "[", "]", formatted)
        else: return ""

    @staticmethod
    def CoerceToList(args):
        """ If 'args' isn't already a list, wrap it in one """
        return args if isinstance(args, list) else [args]

    @staticmethod
    def FlattenArgsList(args):
        """ Given an args list, format it to be usable by the program 
        Parameters:
            args: list(list(string, string)) <--- Preferred
                Is sometimes received as a split string, which needs to be fixed
                list(list(char, char, char ...))  <-- Needs to become list(list(string, string))
        """
        if isinstance(args, list):
            if len(args) == 0: return None # If no arguments are provided, be explicit about it.
            elif all(isinstance(el, str) and len(el) == 1 for el in args):
                args = [["".join(args)]]
            else: args = [Formatter.FlattenArgsList(el) for el in args]
        elif not isinstance(args, str):
            SimpleLogger.outputVerbose("Arguments are unknown", ["Returning: ", args])
        return args

    @staticmethod
    def FlattenList(lst):
        """ Given a list with nested sub-lists, return a list containing all of 
            the elements in each of the sub-lists down to the deepest sub-list.
        Arguments:
            lst: list(...)
        """
        if isinstance(lst, list): 
            flatList = []
            for el in lst:
                if isinstance(el, list):
                    for sub_el in Formatter.FlattenList(el): flatList.append(sub_el)
                else: flatList.append(el)
            return flatList
        else: return lst
