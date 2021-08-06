#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @Author: Christophe Vermeren
# @Date: 2021-07-22 18:13:40
# @Last Modified by: Christophe Vermeren
# @Last Modified time: 2021-08-06 15:46:07


import argparse
import inspect
import os
import subprocess
import sys

from colorama import init, Fore
from time import time, ctime


#        _                  ____                _              _
#    ___| | __ _ ___ ___   / ___|___  _ __  ___| |_ __ _ _ __ | |_
#   / __| |/ _` / __/ __| | |   / _ \| '_ \/ __| __/ _` | '_ \| __|
#  | (__| | (_| \__ \__ \ | |__| (_) | | | \__ \ || (_| | | | | |_
#   \___|_|\__,_|___/___/  \____\___/|_| |_|___/\__\__,_|_| |_|\__|

class Constant:
    ''' A class specified with specific attribute references that contains
        data attributes with values that cannot be altered by the program
        during execution, i.e., the value is constant.
    '''

    # Class variables shared by all instances.
    RSYNC_CMD = "rsync"
    EXCLUDE = [".ansible/", ".docker/", ".minikube/", "awx/", "factcache/",
               "volume/", "Max Payne Savegames/", "HardWest/", "id_rsa*",
               "known_hosts", "main.log"]
    INCLUDE = [".config/gtk-2.0/", ".config/gtk-3.0/", ".config/gtk-4.0/",
               ".config/kde.org/", ".config/keepassxc/", ".config/manjaro/",
               ".config/plasma-workspace/", ".bashrc", ".bash_profile",
               ".hplip/", ".icons/", ".kde4/", ".themes/", ".ssh/",
               "Development/", "Documents/", "Music/", "Pictures/", "Public/",
               "Templates/", "Videos/"]


''' End of class Constant '''


#        _                __     __        _               _ _
#    ___| | __ _ ___ ___  \ \   / /__ _ __| |__   ___  ___(_) |_ _   _
#   / __| |/ _` / __/ __|  \ \ / / _ \ '__| '_ \ / _ \/ __| | __| | | |
#  | (__| | (_| \__ \__ \   \ V /  __/ |  | |_) | (_) \__ \ | |_| |_| |
#   \___|_|\__,_|___/___/    \_/ \___|_|  |_.__/ \___/|___/_|\__|\__, |
#                                                                |___/

class Verbosity:
    ''' To print colored terminal output '''

    def __init__(self, verbose=0):
        ''' Parameterized constructor
            Constructor with parameters is known as parameterized constructor.
            The parameterized constructor take its first argument as a
            reference to the instance being constructed known as self and the
            rest of the arguments are provided by the programmer.

            Args:
                verbose: verbose level mode
        '''
        self.verbose = verbose if verbose is not None else 0

        # Part of colorama,
        # Turn off color changes at the end of every print
        init(autoreset=True)
    ''' End of def __init__(self, verbose=0) '''

    # ██████╗ ██╗   ██╗██████╗ ██╗     ██╗ ██████╗
    # ██╔══██╗██║   ██║██╔══██╗██║     ██║██╔════╝
    # ██████╔╝██║   ██║██████╔╝██║     ██║██║
    # ██╔═══╝ ██║   ██║██╔══██╗██║     ██║██║
    # ██║     ╚██████╔╝██████╔╝███████╗██║╚██████╗
    # ╚═╝      ╚═════╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝

    def debug(self, msg):
        ''' Public method attribute - debug

            Args:
                msg: a text string to be displayed
        '''
        if self.verbose >= 2:
            print(Fore.BLUE + "[" + Fore.MAGENTA + "DEBUG"
                  + Fore.BLUE + "] " + Fore.WHITE + msg)
    ''' End of def debug(self, msg) '''

    def error(self, msg):
        ''' Public method attribute - error

            Args:
                msg: a text string to be displayed
        '''
        print(Fore.BLUE + "[" + Fore.RED + "ERR"
              + Fore.BLUE + "] " + Fore.WHITE + msg)

        # Means there was some issue / error / problem and that is why the
        # program is exiting.
        sys.exit(1)
    ''' End of def error(self, msg) '''

    def info(self, msg):
        ''' Public method attribute - info

            Args:
                msg: a text string to be displayed
        '''
        if self.verbose >= 1:
            print(Fore.BLUE + "[" + Fore.YELLOW + "INFO"
                  + Fore.BLUE + "] " + Fore.WHITE + msg)
    ''' End of def info(self, msg) '''

    def ok(self, msg):
        ''' Public method attribute - ok

            Args:
                msg: a text string to be displayed
        '''
        if self.verbose >= 1:
            print(Fore.BLUE + "[" + Fore.GREEN + "OK"
                  + Fore.BLUE + "] " + Fore.WHITE + msg)
    ''' End of def ok(self, msg) '''

    def warning(self, msg):
        ''' Public method attribute - warning

            Args:
                msg: a text string to be displayed
        '''
        print(Fore.BLUE + "[" + Fore.BLUE + "WARN"
              + Fore.BLUE + "] " + Fore.WHITE + msg)
    ''' End of def warning(self, msg) '''


''' End of class Verbosity '''


#        _                 ____             _
#    ___| | __ _ ___ ___  | __ )  __ _  ___| | ___   _ _ __
#   / __| |/ _` / __/ __| |  _ \ / _` |/ __| |/ / | | | '_ \
#  | (__| | (_| \__ \__ \ | |_) | (_| | (__|   <| |_| | |_) |
#   \___|_|\__,_|___/___/ |____/ \__,_|\___|_|\_\\__,_| .__/
#                                                     |_|

class Backup(Verbosity):
    ''' Class object - Backup

        Args:
            Verbosity: declare that the Backup object class inherits from the
                       Verbosity class
    '''

    command = []  # Empty list
    destination = ""
    exclude_lines = []  # Empty list
    include_lines = []  # Empty list

    def __init__(self):
        ''' Default constructor
            The default constructor is simple constructor which doesn’t accept
            any arguments.It’s definition has only one argument which is a
            reference to the instance being constructed.
        '''
        parser = argparse.ArgumentParser()
        parser.add_argument("destination", help="base of backup destination")
        parser.add_argument("-v", "--verbosity", action="count",
                            help="increase output verbosity")
        args = parser.parse_args()
        super().__init__(args.verbosity)

        self.debug("--- Constructor : " + self.__who_ami_i())

        self.ok("Script '"
                + os.path.basename(sys.argv[0]) + "' initiated on "
                + ctime(time()))

        self.debug("The argument --verbosity is passed with value "
                   + str(self.verbose))

        self.home = os.path.expanduser("~")
        self.username = os.path.split(self.home)[-1]
        self.ok("User\t\t\t: " + self.username)

        if not self.home.endswith("/"):
            self.home += "/"

        self.ok("Source directory\t\t: " + self.home + " (home dir)")

        if args.destination.startswith("/"):
            if os.path.isdir(args.destination):
                self.debug("Base directory for backup exist.")
                self.destination += args.destination.rstrip(
                    "/") + "/" + self.username
                self.__base_dir()
            else:
                self.error("Base directory '" + args.destination
                           + "' for backup doesn't exist.")
        else:
            self.error("The provided positional argument '"
                       + args.destination + "' isn't a path structure.")

        self.debug("--- End of Constructor : " + self.__who_ami_i() + "\n")
    ''' End of def __init__(self) '''

    # ██████╗ ██████╗ ██╗██╗   ██╗ █████╗ ████████╗███████╗
    # ██╔══██╗██╔══██╗██║██║   ██║██╔══██╗╚══██╔══╝██╔════╝
    # ██████╔╝██████╔╝██║██║   ██║███████║   ██║   █████╗
    # ██╔═══╝ ██╔══██╗██║╚██╗ ██╔╝██╔══██║   ██║   ██╔══╝
    # ██║     ██║  ██║██║ ╚████╔╝ ██║  ██║   ██║   ███████╗
    # ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═╝  ╚═╝   ╚═╝   ╚══════╝

    def __base_dir(self):
        ''' Private method attribute - __base_dir
        '''
        if not os.path.isdir(self.destination):
            try:
                os.mkdir(self.destination, mode=0o740,)
            except PermissionError:
                self.error(
                    "Permission denied: You don't seem to have the rights to "
                    + "do that.")
            else:
                self.ok("Directory '" + self.destination + "' created!")

        self.ok("Destination directory\t: " + self.destination)
    ''' End of def __base_dir(self) '''

    def __dirfile_check(self, item, wildcard=False):
        ''' Private method attribute - __dirfile_check

            Args:
                item: dir name or filename
                wildcard: True -- to transfer directory and all its contents
                          False -- only directory
        '''

        if os.path.isdir(self.home + item):
            if wildcard:
                self.include_lines.append('--include="' + item + '/***"')
            else:

                self.include_lines.append('--include="' + item + '/"')
        elif os.path.isfile(item):
            self.include_lines.append('--include="' + item + '"')
        else:
            self.warning("Item '" + item
                         + "' doesn't exist and will not be included.")
    ''' End of def _dirfile_check(self, item) '''

    def __valid_include(self, item):
        ''' Private method attribute - __valid_include

            Args:
                item: a list a file or directory <list>
        '''
        max = len(item)

        for index in range(len(item)):

            if index == 0 and max > 1:
                dir_string = item[index] + "/"
                string = '--include="' + item[index] + '/"'

                cond = any(element in string for element in self.include_lines)

                if not cond:
                    self.__dirfile_check(item[index], False)

            elif index == 0 and max == 1:
                self.__dirfile_check(item[index], True)
            elif (index + 1) == max:
                dir_string += item[index]
                self.__dirfile_check(dir_string, True)
            else:
                string = "--include='" + dir_string + item[index] + "/'"

                if string not in self.include_lines:
                    self.__dirfile_check(dir_string + item[index], False)
                dir_string += item[index] + "/"  # Append to string

    ''' End of def __valid_include(self, item) '''

    def __who_ami_i(self):
        ''' Private method attribute - __who_ami_i

            Args:
        '''
        return inspect.stack()[1][3]
    ''' End of def __who_ami_i(self) '''

    # ██████╗ ██╗   ██╗██████╗ ██╗     ██╗ ██████╗
    # ██╔══██╗██║   ██║██╔══██╗██║     ██║██╔════╝
    # ██████╔╝██║   ██║██████╔╝██║     ██║██║
    # ██╔═══╝ ██║   ██║██╔══██╗██║     ██║██║
    # ██║     ╚██████╔╝██████╔╝███████╗██║╚██████╗
    # ╚═╝      ╚═════╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝

    def is_tool(self, program):
        ''' Public method attribute - is_tool

            Args:
                program: name of program command < str >
        '''
        self.debug("--- Public Method : " + self.__who_ami_i())

        try:
            subprocess.call([program, "--version"],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
        except FileNotFoundError:
            self.error("bash: " + program + ": command not found")
        else:
            self.debug("bash: " + program + ": command found")

        self.command.append(program)
        if self.verbose > 0:
            self.command.append("--stats")  # Give some file-transfer stats

            vargs = "-"
            for n in range(0, self.verbose):
                vargs += "v"

            self.command.append(vargs)  # Increase verbosity

        self.command.append("-a")  # Archive mode
        self.command.append("-r")  # Recurse into directories
        self.command.append("-m")  # Prune empty directory chains from list
        self.command.append("-t")  # Preserve modification times

        # Delete extraneous files from dest dirs
        self.command.append("--delete")

        # Also delete excluded files from dest dirs
        self.command.append("--delete-excluded")

        self.debug("command list: " + str(self.command))
        self.debug("--- End of Public Method : " + self.__who_ami_i() + "\n")
    ''' End of def is_tool(self, program) '''

    def parse_exclude(self, alist):
        ''' Public method attribute - parse_exclude

            Args:
                alist: a list of folders and files required to be excluded
        '''
        self.debug("--- Public Method : " + self.__who_ami_i())

        if not isinstance(alist, list):
            self.error(
                "The passed argument for the variable alist isn't a list.")
        else:
            self.debug("List 'EXCLUDE' has " + str(len(alist)) + " elements.")

        for element in alist:
            self.exclude_lines.append('--exclude="' + element + '"')

        self.command.extend(self.exclude_lines)
        self.debug("exclude_lines: " + str(self.exclude_lines))
        self.debug("--- End of Public Method : " + self.__who_ami_i() + "\n")
    ''' End of def parse_exclude(self, alist) '''

    def parse_include(self, alist):
        ''' Public method attribute - parse_include

            Args:
                alist: a list of folders and files required to be included
        '''
        self.debug("--- Public Method : " + self.__who_ami_i())

        if not isinstance(alist, list):
            self.error(
                "The passed argument for the variable alist isn't a list.")
        elif len(alist) == 0:
            self.error(
                "The passed argument for the variable alist is empty.")
        else:
            self.debug("List 'INCLUDE' has " + str(len(alist)) + " elements.")

        for element in alist:

            # Remove the first characters if the first characters of the string
            # starts with ~/
            if element.startswith("~/"):
                element = element.lstrip("~/")

            # If the first character of the string starts with a slash (/) then
            # check if the string starts with the user home directory or not.
            if element.startswith("/"):
                if element.startswith(self.home):
                    element = element.lstrip(self.home)
                else:
                    continue

            # Remove the last character if the last character of the string
            # ends with a slash (/).
            if element.endswith("/"):
                element = element.rstrip("/")

            str2list = element.split("/")  # Split a string into a list

            if len(str2list) > 0:
                self.__valid_include(str2list)

        self.command.extend(self.include_lines)
        self.debug("include_lines: " + str(self.include_lines))
        self.debug("--- End of Public Method : " + self.__who_ami_i() + "\n")
    ''' End of def parse_include(self, alist) '''

    def run_command(self):
        ''' Public method attribute -  - run_command
            Execute command to initiate the backup
        '''
        self.debug("--- Public Method : " + self.__who_ami_i())

        self.command.append('--exclude="*"')
        self.command.append(self.home)
        self.command.append(self.destination)

        msg = subprocess.run(" ".join(self.command),
                             stdout=subprocess.PIPE, check=True, shell=True)
        if msg.returncode == 0:
            self.ok("Rsync completed!")

        self.debug("--- End of Public Method : " + self.__who_ami_i() + "\n")
    ''' End of def run_command(self) '''

# ██████╗ ███████╗███████╗    ███╗   ███╗ █████╗ ██╗███╗   ██╗
# ██╔══██╗██╔════╝██╔════╝    ████╗ ████║██╔══██╗██║████╗  ██║
# ██║  ██║█████╗  █████╗      ██╔████╔██║███████║██║██╔██╗ ██║
# ██║  ██║██╔══╝  ██╔══╝      ██║╚██╔╝██║██╔══██║██║██║╚██╗██║
# ██████╔╝███████╗██║         ██║ ╚═╝ ██║██║  ██║██║██║ ╚████║
# ╚═════╝ ╚══════╝╚═╝         ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝


def main():

    # New object instances (instantiation) of the classes 'Constant' and
    # 'Backup'
    c = Constant()
    r = Backup()

    # Calling object's methods
    r.is_tool(c.RSYNC_CMD)
    r.parse_exclude(c.EXCLUDE)
    r.parse_include(c.INCLUDE)
    r.run_command()


if __name__ == "__main__":
    main()
