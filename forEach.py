#!/usr/bin/python

from colorama import init, Fore, Back, Style

import sys, os, argparse, re



init(autoreset=True)

isVerbose = False





def logVerbose(message):

    global isVerbose

    message = lstToStr(message, True)

    if isVerbose:

        print "\n"+ Fore.RED + Back.BLACK + message



def flatten(lst):

    if isinstance(lst, str):

        return lst

    if isinstance(lst, list) and len(lst) == 0:

        return ""

    if isinstance(lst, list)  and all(isinstance(el, str) for el in lst):

        logVerbose("Arguments = list of characters")

        logVerbose(["Returning", "".join(lst)])

    return "".join(lst)

    elif isinstance(lst, list):

        logVerbose("Arguments = list")

        val = [ flatten(el) for el in lst ]

        logVerbose([ "Returning", val])

        return val

    else:

        logVerbose("Arguments are unknown")

        logVerbose("Returning", lst)

        return lst



def lstToStr(lst, printBrackets=False, isFirst=True):

    returnStr = ""

    if isinstance(lst, list):

        if printBrackets and not isFirst:

            returnStr+="["

        for i in range(0, len(lst)):

            if isinstance(lst[i], list):

                returnStr += lstToStr(lst[i], printBrackets, False)

            elif isinstance(lst[i], str):

                if printBrackets and not isFirst:

                   returnStr += "'"+lst[i] + "'"

                else:

                   returnStr += lst[i]

                

            if i!= len(lst)-1 and printBrackets and not isFirst:

                returnStr+=","

        if printBrackets and not isFirst:

            returnStr+="]"



    elif isinstance(lst, str):

        return lst

    return returnStr



def makeCommand(commandString, arguments):

    logVerbose(["command is: ", commandString, " arguments are: ", arguments])

    cmd = commandString

    for i in range(0, len(arguments)):

        placeholder = "{"+str(i)+"}"

        cmd = cmd.replace(placeholder, arguments[i])

    cmd = re.sub(r'\{[0-9]+\}', '', cmd)

    return cmd;

def makeMultipleCommands( commandStr, argLists):

    cmds = []

    for arguments in argLists:

    cmd = makeCommand( commandStr, arguments)

    cmds.append(cmd)

    return cmds

def runCommand(cmd):

    print Fore.CYAN + Back.BLACK + "\n>", cmd

    os.system( cmd )

def multiple(cmds):

    for cmd in cmds:

        runCommand(cmd)



def map(lsts):

    logVerbose([ "In Map.  lsts is: ", lsts])

    if isinstance(lsts, list) and len(lsts)>0:

    mapped = [[]]

        for l in  lsts:

            rowCombinations = []

            for el in l:

                reduced = [ m + [el] for m in mapped ]

                rowCombinations.extend(reduced)

            

            mapped = rowCombinations

            logVerbose(["Added layer of arguments", mapped])

        logVerbose(["Mapped", mapped])

        return mapped



def combine(argLists):

    if isinstance(argLists, list) and len(argLists) > 1:

      return  map(argLists) 

    elif isinstance(argLists, list) and len(argLists) == 1 and all(  isinstance(el, str) for el in argLists[0]):

      logVerbose( [ "Returning ", [ [ el ] for el in argLists[0]], " from combine"])

      return  [ [ el ] for el in argLists[0 ]]



parser = argparse.ArgumentParser()

parser.add_argument('-args', action='append', type=list, dest='listOfLists', nargs='+')

parser.add_argument('-cmd', action='store', dest='cmd')

parser.add_argument('-single', action='store_true', dest='isSingle', default=False)

parser.add_argument('-v', action='store_true', dest='isVerbose', default=False)

args = parser.parse_args()

isVerbose = args.isVerbose

var = lstToStr(args.listOfLists)

logVerbose([var, "listofLists, reduced"])

logVerbose( "Command: "+args.cmd+"\nArguments: "+lstToStr(flatten(args.listOfLists), True))

cmdArgs = []



for argList in args.listOfLists: 

    words =  [ lstToStr(word) for word in argList ]

    cmdArgs.append(words)



if args.isSingle:

    logVerbose( "Using multiple mode")

    multiple( makeMultipleCommands( args.cmd, cmdArgs ))

else:

    logVerbose("Using combine mode")

    result = combine( cmdArgs )

    logVerbose(["Combine result is: ", result])

    multiple( makeMultipleCommands( args.cmd, result))