from datetime import datetime # for logs
import re # for regex support
import os # for scanning directories, deleting files, etc

# basic function that checks the validity of a regex string, some_reg provided
def valid_regex(some_reg: str):
    try:
        re.compile(some_reg)
        return True
    except:
        return False

# Each ReplacementStr object represents one line in the file containing strings to be replaced and to replace with
class ReplacementStr():
    find: str
    replace: str

    def __init__(self,find: str,replace: str):
        self.find = find
        self.replace = replace

# Class will contain all settings imported from the config file
class SETTINGS:
    DELIMITER: str = "||||"
    HYPERTEXT_SUPPORT: bool = True
    PROCESS_FILES_IN_CURRENT_DIR: bool = True
    FILES_CUSTOM_DIR: str = "/some/path"
    SAVE_FILES_THAT_WILL_BE_SCANNED_LOG: bool = True
    RUN_WITH_WARNINGS: bool = True
    EXTENSIONS: list[str] = ["html","htm","xhtml","xml"]
    BANNED_TAGS: list[str] = ["script","style","meta","link","svg"]
    ENCODING: str = 'utf-8'
    OVERWRITE_FILES: bool = False
    NEW_FILE_NAMES_SUFFIX: str = "_new"
    LOGS_FILE_NAME: str = "change-files.log"
    STRINGS_FILE_NAME: str = "regexp.dat"
    BANNED_FILE_NAMES: list[str] = ["readme.txt","regexp.dat","change-text.log"]
    SKIP_FILES_WITH_UNIDENTIFIED_TAGS: bool = True

# Exception handles when config file has an invalid setting
class InvalidSettingException(Exception):
    default_msg: str = "An error occurred. Your config file contains an invalid value for one of the lines: "
    
    def __init__(self, line: str, message: str = default_msg):
        self.message = message + " " + line
        super().__init__(self.message)

# Exception handles when config file has an invalid setting
class MissingSettingException(Exception):
    default_msg: str = "An error occurred. Your config file is missing a setting line: "
    
    def __init__(self, line: str, message: str = default_msg):
        self.message = message + " " + line
        super().__init__(self.message)

# Exception handles when strings file has an issue
class StringsFileException(Exception):
    default_msg: str = "An error occurred. Your regexp.dat file is likely causing this error. Please ensure all lines have a valid DELIMITER, the file is not empty, and does not have any empty new lines, then try running the script again."
    
    def __init__(self,message=default_msg):
        self.message = message
        super().__init__(self.message)

# Exception handles when the strings file is empty
class LineMissingDelimeterException(StringsFileException):
    default_msg: str = "Your file with string replacements likely contains one or more lines without a valid delimeter."
    def __init__(self, line:str, message=default_msg):
        self.message = message + f" Please check line {line} on the file and ensure it has a valid delimiter."
        super().__init__(self.message)

# Exception handles when the strings file is empty
class EmptyStringsFileException(StringsFileException):
    default_msg: str = "Your file with string replacements is empty. Please ensure this is not the case to proceed."
    def __init__(self,message=default_msg):
        self.message = message
        super().__init__(self.message)

print("""
        Warnings:
        - Please read the "readme.txt" file before using the script.
        - No lines can contain "\\n" in the config file.
        - You can either run the script for hypertext files or non-hypertext files - not both at the same time
        ----------------------------------------------------
        """)


if __file__ != "__main__":
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"
else:
    SCRIPT_DIR = os.getcwd()

print(f"Script is currently located at: {SCRIPT_DIR}. This will be taken as the working directory if no custom directory is specified otherwise.\n")

if os.path.exists(SCRIPT_DIR + 'findrepl.cfg'): # check if findrepl.cfg is in the script's directory
    print("Config file \"findrepl.cfg\" has been found in the script directory.")
    config_filename = "findrepl.cfg"
else: # findrepl.cfg not found in script directory
    config_filename = input("Enter the config file's filename, or press ENTER to continue with default settings: ")
    if config_filename == "":
        print("Script will run using the default settings listed below:")
        print(f"DELIMITER: \"{SETTINGS.DELIMITER}\"")
        print(f"Hypertext Support: {SETTINGS.HYPERTEXT_SUPPORT}")
        print(f"Current Directory For Files: {SETTINGS.PROCESS_FILES_IN_CURRENT_DIR}")
        print(f"Save log for files that will be scanned: {SETTINGS.SAVE_FILES_THAT_WILL_BE_SCANNED_LOG}")
        print(f"Run with warnings: {SETTINGS.RUN_WITH_WARNINGS}")
        print(f"Extensions: {SETTINGS.EXTENSIONS}")
        print(f"Banned tags: {SETTINGS.BANNED_TAGS}")
        print(f"Default encoding: {SETTINGS.ENCODING}")
        print(f"Overwrite Files: {SETTINGS.OVERWRITE_FILES}")
        print(f"Suffix for new file names: \"{SETTINGS.NEW_FILE_NAMES_SUFFIX}\"")
        print(f"Logs file filename: {SETTINGS.LOGS_FILE_NAME}")
        print(f"Strings file filename: {SETTINGS.STRINGS_FILE_NAME}")
        print(f"Skip Files with unidentified tags: {SETTINGS.SKIP_FILES_WITH_UNIDENTIFIED_TAGS}")

if config_filename != "": # if a config file is provided
    # empty the defaults (so missing settings in the config file can be identified)
    SETTINGS.DELIMITER: str = None
    SETTINGS.HYPERTEXT_SUPPORT: bool = None
    SETTINGS.PROCESS_FILES_IN_CURRENT_DIR: bool = None
    SETTINGS.FILES_CUSTOM_DIR: str = None
    SETTINGS.SAVE_FILES_THAT_WILL_BE_SCANNED_LOG: bool = None
    SETTINGS.RUN_WITH_WARNINGS: bool = None
    SETTINGS.EXTENSIONS: list[str] = None
    SETTINGS.BANNED_TAGS: list[str] = None
    SETTINGS.ENCODING: str = None
    SETTINGS.OVERWRITE_FILES: bool = None
    SETTINGS.NEW_FILE_NAMES_SUFFIX: str = None
    SETTINGS.LOGS_FILE_NAME: str = None
    SETTINGS.STRINGS_FILE_NAME: str = None
    SETTINGS.BANNED_FILE_NAMES: list[str] = None
    SETTINGS.SKIP_FILES_WITH_UNIDENTIFIED_TAGS: bool = None


    if os.path.exists(SCRIPT_DIR + config_filename):
        print(f"{config_filename} will be used for carrying out the operations.")

    # Loading all the settings from the config file and ensuring their validity
    with open(SCRIPT_DIR + config_filename, 'r') as config_file:
        for line in config_file:
            line = line.strip("\n").split("=")
            if line[0] == "DELIMITER":
                SETTINGS.DELIMITER = line[1]
                print(f"DELIMITER: \"{line[1]}\"")
            if line[0] == "HYPERTEXT_SUPPORT":
                if line[1] == "YES":
                    SETTINGS.HYPERTEXT_SUPPORT = True
                elif line[1] == "NO":
                    SETTINGS.HYPERTEXT_SUPPORT = False
                else:
                    raise InvalidSettingException(line[0])
                print(f"Hypertext Support: {line[1]}")
            if line[0] == "PROCESS_FILES_IN_CURRENT_DIR":
                if line[1] == "YES":
                    SETTINGS.PROCESS_FILES_IN_CURRENT_DIR = True
                elif line[1] == "NO":
                    SETTINGS.PROCESS_FILES_IN_CURRENT_DIR = False
                else:
                    raise InvalidSettingException(line[0])
                print(f"Current Directory For Files: {line[1]}")
            if line[0] == "FILES_CUSTOM_DIR":
                if line[1][-1] == "/":
                    line[1] = line[1][:-1]
                SETTINGS.FILES_CUSTOM_DIR = line[1]
                if not SETTINGS.PROCESS_FILES_IN_CURRENT_DIR:
                    print(f"Custom Files Directory: {line[1]}")
            if line[0] == "SAVE_FILES_THAT_WILL_BE_SCANNED_LOG":
                if line[1] == "YES":
                    SETTINGS.SAVE_FILES_THAT_WILL_BE_SCANNED_LOG = True
                elif line[1] == "NO":
                    SETTINGS.SAVE_FILES_THAT_WILL_BE_SCANNED_LOG = False
                else:
                    raise InvalidSettingException(line[0])
                print(f"Save log for files that will be scanned: {line[1]}")
            if line[0] == "RUN_WITH_WARNINGS":
                if line[1] == "YES":
                    SETTINGS.RUN_WITH_WARNINGS = True
                elif line[1] == "NO":
                    SETTINGS.RUN_WITH_WARNINGS = False
                else:
                    raise InvalidSettingException(line[0])
                print(f"Run with warnings: {line[1]}")
            if line[0] == "EXTENSIONS":
                SETTINGS.EXTENSIONS = line[1].split(",")
                print(f"Extensions: {line[1]}")
            if line[0] == "BANNED_TAGS":
                SETTINGS.BANNED_TAGS = line[1].split(",")
                print(f"Banned tags: {line[1]}")
            if line[0] == "ENCODING":
                SETTINGS.ENCODING = line[1]
                print(f"Default encoding: {line[1]}")
            if line[0] == "OVERWRITE_FILES":
                if line[1] == "YES":
                    SETTINGS.OVERWRITE_FILES = True
                elif line[1] == "NO":
                    SETTINGS.OVERWRITE_FILES = False
                else:
                    raise InvalidSettingException(line[0])
                print(f"Overwrite Files: {line[1]}")
            if line[0] == "NEW_FILE_NAMES_SUFFIX":
                SETTINGS.NEW_FILE_NAMES_SUFFIX = line[1]
                if not SETTINGS.OVERWRITE_FILES:
                    print(f"Suffix for new file names: \"{line[1]}\"")
            if line[0] == "LOGS_FILE_NAME":
                if line[1] and line[1] is not None:
                    SETTINGS.LOGS_FILE_NAME = line[1]
                else:
                    raise InvalidSettingException(line[0])
                print(f"Logs file filename: {line[1]}")
            if line[0] == "STRINGS_FILE_NAME":
                if line[1] and line[1] is not None:
                    SETTINGS.STRINGS_FILE_NAME = line[1]
                else:
                    raise InvalidSettingException(line[0])
                print(f"Strings file filename: {line[1]}")
            if line[0] == "BANNED_FILE_NAMES":
                if line[1] and line[1] is not None:
                    SETTINGS.BANNED_FILE_NAMES = line[1].split(",")
                else:
                    raise InvalidSettingException(line[0])
                print(f"Banned filenames: {line[1]}")
            if line[0] == "SKIP_FILES_WITH_UNIDENTIFIED_TAGS":
                if line[1] == "YES":
                    SETTINGS.SKIP_FILES_WITH_UNIDENTIFIED_TAGS = True
                elif line[1] == "NO":
                    SETTINGS.SKIP_FILES_WITH_UNIDENTIFIED_TAGS = False
                else:
                    raise InvalidSettingException(line[0])
                print(f"Skip files with unidentified tags: {line[1]}")

# Ensuring all settings exist to avoid issues during operations
try:
    if SETTINGS.DELIMITER == None:
        raise MissingSettingException("DELIMITER")
except:
    raise MissingSettingException("DELIMITER")
try:
    if SETTINGS.HYPERTEXT_SUPPORT == None:
        raise MissingSettingException("HYPERTEXT_SUPPORT")
except:
    raise MissingSettingException("HYPERTEXT_SUPPORT")
try:
    if SETTINGS.PROCESS_FILES_IN_CURRENT_DIR == None:
        raise MissingSettingException("PROCESS_FILES_IN_CURRENT_DIR")
except:
    raise MissingSettingException("PROCESS_FILES_IN_CURRENT_DIR")
try:
    if SETTINGS.FILES_CUSTOM_DIR == None:
        raise MissingSettingException("FILES_CUSTOM_DIR")
except:
    raise MissingSettingException("FILES_CUSTOM_DIR")
try:
    if SETTINGS.SAVE_FILES_THAT_WILL_BE_SCANNED_LOG == None:
        raise MissingSettingException("SAVE_FILES_THAT_WILL_BE_SCANNED_LOG")
except:
    raise MissingSettingException("SAVE_FILES_THAT_WILL_BE_SCANNED_LOG")
try:
    if SETTINGS.RUN_WITH_WARNINGS == None:
        raise MissingSettingException("RUN_WITH_WARNINGS")
except:
    raise MissingSettingException("RUN_WITH_WARNINGS")
try:
    if SETTINGS.EXTENSIONS == None:
        raise MissingSettingException("EXTENSIONS")
except:
    raise MissingSettingException("EXTENSIONS")
try:
    if SETTINGS.BANNED_TAGS == None:
        raise MissingSettingException("BANNED_TAGS")
except:
    raise MissingSettingException("BANNED_TAGS")
try:
    if SETTINGS.ENCODING == None:
        raise MissingSettingException("ENCODING")
except:
    raise MissingSettingException("ENCODING")
try:
    if SETTINGS.OVERWRITE_FILES == None:
        raise MissingSettingException("OVERWRITE_FILES")
except:
    raise MissingSettingException("OVERWRITE_FILES")
try:
    if SETTINGS.NEW_FILE_NAMES_SUFFIX == None:
        raise MissingSettingException("NEW_FILE_NAMES_SUFFIX")
except:
    raise MissingSettingException("NEW_FILE_NAMES_SUFFIX")
try:
    if SETTINGS.LOGS_FILE_NAME == None:
        raise MissingSettingException("LOGS_FILE_NAME")
except:
    raise MissingSettingException("LOGS_FILE_NAME")
try:
    if SETTINGS.STRINGS_FILE_NAME == None:
        raise MissingSettingException("STRINGS_FILE_NAME")
except:
    raise MissingSettingException("STRINGS_FILE_NAME")
try:
    if SETTINGS.BANNED_FILE_NAMES == None:
        raise MissingSettingException("BANNED_FILE_NAMES")
except:
    raise MissingSettingException("BANNED_FILE_NAMES")
try:
    if SETTINGS.SKIP_FILES_WITH_UNIDENTIFIED_TAGS == None:
        raise MissingSettingException("SKIP_FILES_WITH_UNIDENTIFIED_TAGS")
except:
    raise MissingSettingException("SKIP_FILES_WITH_UNIDENTIFIED_TAGS")



strings = [] # array will contain all string objects

# storing all strings in the provided file as objects:
try:
    with open(SCRIPT_DIR + SETTINGS.STRINGS_FILE_NAME, "r", encoding=SETTINGS.ENCODING) as strings_file:
        count = 1
        for line in strings_file:
            s = line.split(SETTINGS.DELIMITER)
            strings.append(ReplacementStr(s[0].strip("\n"),s[1].strip("\n")))
            count += 1
except IndexError:
    raise LineMissingDelimeterException(count)
except:
    raise StringsFileException

invalid_regex = [] # will store potential invalid regex in the strings file
count = 1 # count 

# Loop through the strings in the provided strings file, also check for the invalid regex
# print("The following strings will be scanned and replaced (if found):")
for string in strings:
    regex_valid = valid_regex(string.find)
    if regex_valid == False:
        invalid_regex.append([string.find, count])
    count += 1
if count <= 1:
    raise EmptyStringsFileException
else:
    print(f"{count-1} strings taken from the file {SETTINGS.STRINGS_FILE_NAME} will be found and replaced everywhere in the provided files if found.")


# If invalid regex exists, warn the user
if invalid_regex and invalid_regex is not None:
    print() # new line for readability
    print("Warning! The program identified the following regex that were invalid:")
    for invalid_item in invalid_regex:
        print(f"Line {invalid_item[1]}: {invalid_item[0]}")
del count # removes count since it is no longer necessary
print() # new line for readability


if SETTINGS.RUN_WITH_WARNINGS:
    a = input("Press any key to continue or q to CANCEL: ")
    if a == 'q':
        exit()
    del a

extensions = tuple(SETTINGS.EXTENSIONS)

files_to_use = [] # array containing the filenames of the files to run the script with    

if SETTINGS.PROCESS_FILES_IN_CURRENT_DIR:
    for file in os.listdir(SCRIPT_DIR):
        if file.endswith(extensions):
            if file not in SETTINGS.BANNED_FILE_NAMES and file != SETTINGS.STRINGS_FILE_NAME and file != SETTINGS.LOGS_FILE_NAME and file != config_filename:
                files_to_use.append(file)
                    
else:
    for file in os.listdir(SETTINGS.FILES_CUSTOM_DIR):
        if file.endswith(extensions):
            if file not in SETTINGS.BANNED_FILE_NAMES and file != SETTINGS.STRINGS_FILE_NAME and file != SETTINGS.LOGS_FILE_NAME and file != config_filename:
                files_to_use.append(file)

if not files_to_use: # accounts for if no files will be affected
    print("There are no files to be edited with the extension/s that you have provided.")
    exit()
else:
    print(f"{len(files_to_use)} files will be searched.")
    if SETTINGS.SAVE_FILES_THAT_WILL_BE_SCANNED_LOG:
        files_that_will_be_tweaked_file = open('change-files.log', "w", encoding=SETTINGS.ENCODING)
        for file in files_to_use:
            files_that_will_be_tweaked_file.write(file + "\n")
        files_that_will_be_tweaked_file.close()
        print("The files that will be used have been stored in a \"change-files.log\" file.")
    if SETTINGS.RUN_WITH_WARNINGS:
        a = input("Press any key to continue or q to CANCEL: ")
        if a == 'q':
            exit()
        del a
total_changes = 0
files_to_skip = []
if files_to_use:
    if SETTINGS.HYPERTEXT_SUPPORT == False: # for plaintext/non-hypertext files
        with open(SCRIPT_DIR + SETTINGS.LOGS_FILE_NAME, 'a', encoding=SETTINGS.ENCODING) as logs:
            for file in files_to_use:
                if not SETTINGS.PROCESS_FILES_IN_CURRENT_DIR:
                    file_name = f"{SETTINGS.FILES_CUSTOM_DIR}/{file}"
                else:
                    file_name = SCRIPT_DIR + file
                with open(file_name, "r", encoding=SETTINGS.ENCODING) as original:
                    file_split = file_name.split(".")
                    new_file_name = f'{file_split[0]}{SETTINGS.NEW_FILE_NAMES_SUFFIX}.{file_split[1]}'
                    print(new_file_name)
                    with open(new_file_name, "w", encoding=SETTINGS.ENCODING) as new:
                        changed_tags = False
                        for i in original: # for each line in the original file
                            for string in strings:
                                if re.search(string.find, i):
                                    changed_tags = True # used later to not delete _new file since changes were actually made.
                                    old = str(i).strip("\n")
                                    i = re.sub(string.find, string.replace, i)
                                    new_log = i.strip("\n")
                                    info = f'{file} CHANGE ({datetime.now()}): \"{old}\" --------> \"{new_log}\"\n'
                                    logs.write(info)
                                    total_changes += 1
                            new.write(i)
                    if changed_tags == False: # only delete file if there are no changed tags
                        os.remove(new_file_name)
    else: # for hypertext files
        from bs4 import BeautifulSoup, Comment
        with open(SCRIPT_DIR + SETTINGS.LOGS_FILE_NAME, 'a', encoding=SETTINGS.ENCODING) as logs: 
            for file in files_to_use:
                if not SETTINGS.PROCESS_FILES_IN_CURRENT_DIR:
                    file_name = f"{SETTINGS.FILES_CUSTOM_DIR}/{file}"
                else:
                    file_name = SCRIPT_DIR + file
                with open(file_name, "r", encoding=SETTINGS.ENCODING) as original:
                    changed_tags = False
                    has_unidentified_tags = False
                    file_split = file_name.split(".")
                    if file_split[1] == "xml": # to preserve XML (case sensitivity, etc)
                        soup = BeautifulSoup(original, 'xml')
                    else:
                        soup = BeautifulSoup(original, 'lxml')
                    for string in strings:
                        tags_with_changes = soup.find_all(string=re.compile(string.find))
                        for tag in tags_with_changes:
                            if SETTINGS.SKIP_FILES_WITH_UNIDENTIFIED_TAGS:
                                print(tag.name)
                                if tag.name == None and file_split[1] != 'xml':
                                    has_unidentified_tags = True
                                    changed_tags = False
                                    files_to_skip.append(file)
                                    info = f"{file} SKIPPED ({datetime.now()}): The file contains an unidentified tag (such as '<? ... ?>'), and has been skipped due to this reason"
                                    print(info) # this is being printed to CLI as well since it is important for the user to know and likely rare for most use cases.
                                    logs.write(info)
                                    # break # breaks out of inner loop (for tag in tags_with_changes)
                            if (tag.parent.name not in SETTINGS.BANNED_TAGS) and (not isinstance(tag, Comment)):
                                old = str(tag.text).strip("\n")
                                new_tag = re.sub(string.find,string.replace,tag)
                                tag.replace_with(new_tag)
                                new_log = new_tag.strip("\n")
                                info = f'{file} CHANGE ({datetime.now()}): \"{old}\" --------> \"{new_log}\"\n'
                                logs.write(info)
                                total_changes += 1
                                changed_tags = True
                        if has_unidentified_tags:
                            pass # break # breaks out of outer loop (for string in strings)
                    if changed_tags and not has_unidentified_tags:
                        new_file_name = f'{file_split[0]}{SETTINGS.NEW_FILE_NAMES_SUFFIX}.{file_split[1]}'
                        with open(new_file_name, "w", encoding=SETTINGS.ENCODING) as new:
                            soup.prettify(formatter=None)
                            soup.encode(SETTINGS.ENCODING)
                            new.write(str(soup))
                    tags_with_changes = None
    if SETTINGS.OVERWRITE_FILES:
        for file in files_to_use:
            if file not in files_to_skip:
                if not SETTINGS.PROCESS_FILES_IN_CURRENT_DIR:
                    file_name = f"{SETTINGS.FILES_CUSTOM_DIR}/{file}"
                else:
                    file_name = SCRIPT_DIR + file
                file_split = file_name.split(".")
                new_file_name = f'{file_split[0]}{SETTINGS.NEW_FILE_NAMES_SUFFIX}.{file_split[1]}'
                if os.path.exists(new_file_name):
                    with open(file_name, "w", encoding=SETTINGS.ENCODING) as original:
                        with open(new_file_name, "r", encoding=SETTINGS.ENCODING) as new:
                            for line in new:
                                original.write(line)
                    os.remove(new_file_name)

print(f"Script has successfully completed running. {total_changes} changes were made in total.")
print(f"If any actions (changes or files being skipped) were logged, they have been added to the {SETTINGS.LOGS_FILE_NAME} file.")

input('Press the Enter key to continue')
