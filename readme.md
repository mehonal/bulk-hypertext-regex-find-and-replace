# What the script needs to run
- main.py (the main script file)
- a file containing the strings in the same directory as the script (default filename: regexp.dat)
- a file containing settings in the same directory of the script (default filename: findrepl.cfg)

# What to watch out for
- The settings file must include all settings. The script has been coded without hard-coded default fallbacks to ensure the script functions in accordance to the user's needs. This is done to prevent the the user's potential negligence of including a setting, resulting in an undesired fallback.
- No lines can contain "\n" in the settings file.
- HTML Comments are ignored in hypertext files.
- You can either run the script for hypertext files or non-hypertext files - not both at the same time
- The script has some built in exceptions to handle common possible errors that could result from the user's end. If the script is not working, there is a high chance that the exceptions thrown can reveal what the problem is.
- The script should hint at it in most cases but please be mindful of tab characters, spaces, and new lines in the strings and settings files.
- The script has been tested for .HTML, .XML, .XHTML, and .TXT files in limited contexts. Throughout the tests conducted, the script supported these files. However, empty lines and empty spaces and indentation could change. Other than this, no other issues were identified during the tests.
- The script has not been tested with more than a handful of files. A stress test is highly recommended before making changes on important files to see how the script handles large number of files on the provided devices.

Please proceed with caution. As cliche as it may sound, with great power comes great responsibility :)

# Script Modes
The script can run in two modes: HYPERTEXT_SUPPORT ON and HYPERTEXT_SUPPORT OFF. Here is what these modes mean:

## HYPERTEXT_SUPPORT ON

This would add support to HYPERTEXT_SUPPORT, which treats each tag as an individual element.

    - This mode can only run on hypertext files
    - This mode allows additional functionality unique to tags
        - One example of such functionality is banning tags which does not allow the script to alter the contents of specific tags such as 'script' or 'style.'
    - The following settings are only relevant when this mode is set to ON:
        - BANNED_TAGS, SKIP_FILES_WITH_UNIDENTIFIED_TAGS

## HYPERTEXT_SUPPORT OFF

This would treat each line of the provided file as an individual line, which would be used to parse the regex expressions and replace the matching ones.

    - This mode can run on hypertext and non-hypertext files
    - Running this with hypertext files is highly risky and should only be done with extreme caution.
        - If hypertext files are used with this mode, potential variables, class names, styles, URLs and more are prone to be changed, and resuling in unidentified alterations.



# Settings File

- DELIMITER=|||| Any delimiter to separate regex expressions to be searched and replaced

- HYPERTEXT_SUPPORT=YES/NO (input "YES" for HTML, XML, XHTML files, "NO" otherwise)

- PROCESS_FILES_IN_CURRENT_DIR=YES/NO (input "YES" to use files in the directory of the script, "NO" to input a custom files directory)

- FILES_CUSTOM_DIR=/some/random/path Only used if PROCESS_FILES_IN_CURRENT_DIR is set to "YES" and specifies the directory of the files to be scanned and used for the find and replace operations

- SAVE_FILES_THAT_WILL_BE_SCANNED_LOG=YES/NO (setting to "YES" will log the files that will be scanned and used in a .txt file in the directory of the script. A warning will be given to the user before proceeding, allowing them to check the file and optionally abort the script (if RUN_WITH_WARNINGS is set to "YES". Setting to "NO" will bypass this procedure)

- RUN_WITH_WARNINGS=YES/NO (setting to "YES" will bypass any warnings, and just run the script with the provided settings file)

- EXTENSIONS=html,xml,xhtml,txt (you may list the file extensions that will be used here. These are separated with commas.)

- BANNED_TAGS=script,style,meta,link,svg (you may specify any HTML/XHTML/XML tags here to be "banned" so that the contents of these tags are not altered, saving the website from breaking, and allowing content to ONLY be changed where it should be. Tags are separated with commas.)

- ENCODING=utf-8 (custom encoding can be added here, but should be checked for compliance with Pythons "open" and bs4's "encode" functions)

- OVERWRITE_FILES=YES/NO (setting to "YES" will overwrite the files that have contents to be replaced)

- NEW_FILE_NAMES_SUFFIX=_new (you may set a custom suffix for files that are altered. Please note that this suffix will be used even if OVERWRITE_FILES is set to "YES" for a brief moment, so be cautious of making it something that could cause name duplications, or leaving it empty.) 

- LOGS_FILE_NAME=logs.txt (you may specify the filename for the file containing all the logs of the operations done here. This file will be made and stored in the directory of the script if it does not exist already. If it exists, logs will be appended to the end of the file.)

- STRINGS_FILE_NAME=strings.txt (you may specify a filename for the file containing all the strings to be searched for and replaced here. This file should be stored in the directory of the script.)

- BANNED_FILE_NAMES=readme.txt,regexp.dat,change-text.log (you may specify a files to be ignored by the script here, separated by commas.)

- SKIP_FILES_WITH_UNIDENTIFIED_TAGS=YES (this setting is only used when HYPERTEXT_SUPPORT is ON, and related to non-XML files. Its main use is to identify files with unidentified tags (such as "<? ... ?>"), and ignore these files so their tags are preserved.)


## Example Settings File Configuration

DELIMITER=||||

HYPERTEXT_SUPPORT=YES

PROCESS_FILES_IN_CURRENT_DIR=YES

FILES_CUSTOM_DIR=/some/directory/path/here/

SAVE_FILES_THAT_WILL_BE_SCANNED_LOG=YES

RUN_WITH_WARNINGS=YES

EXTENSIONS=xml,htm,html,xhtml

BANNED_TAGS=script,style,meta,link,svg

ENCODING=utf-8

OVERWRITE_FILES=NO

NEW_FILE_NAMES_SUFFIX=_new

LOGS_FILE_NAME=change-text.log

STRINGS_FILE_NAME=regexp.dat

BANNED_FILE_NAMES=readme.txt,regexp.dat,change-text.log

SKIP_FILES_WITH_UNIDENTIFIED_TAGS=YES

# Strings File

The strings file should contain:
1. regex expressions to search for in the files
2. A delimiter (this is determined in the settings file)
3. What to replace the matching regex expressions with

## Example Strings File Configuration

Hello||||Hi

1234||||1,234

[Bb]eautiful\s[Ss]oup||||BS4

# Reported Issues

- Some special characters cannot be encoded properly in the logs file.