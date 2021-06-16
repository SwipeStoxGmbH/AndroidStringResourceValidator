# AndroidStringResourceValidator

This is a simple script that will help you validate the placeholders in your translations and warn you if you do not have a string from the default language in one of your translation files.

### How to run
You need Python3 to run this file. You can run it from wherever using ```python3 stringsValidator.py``` in your terminal.

The script will ask you two things:
1. To insert your Android project's resources folder
  - if you are running the script from inside your resources folder, you can just press enter. If not, just copy and paste the path to your resources folder. For example ```/Users/user/Documents/android/presentation/src/main/res```
2. To insert the number of maximum placeholders in one string (e.g. ```%1$s Hello %2$s``` has 2 placeholders). If you just press Enter, it's going to use 5 as the default


The script will output the languages and keys that are not correct. It will tell you which keys do not have the same number of placeholders, and which keys are not present in the translations:
```
----------------------------------------------------------------------------------
-----------------------------------LANGUAGE: DE-----------------------------------
----------------------------------------------------------------------------------
!!!!!Key "set_language" is not present in the second language. Maybe it should be added.!!!!!
----------------------------------------------------------------------------------
key "account_name_to_short_error_message" is not valid, missing placeholders are: ['%d']
EN string: You need at least %d characters.
DE string: "Mind. Zeichen"
----------------------------------------------------------------------------------
```
