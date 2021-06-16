#!/usr/local/bin/python3

import os
import pathlib
import xml.etree.ElementTree as ET

languages = []
full_list_of_placeholders = []
placeholders = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'o', 's', 'x']
currentAbsolutePath = pathlib.Path().absolute()
defaultLanguageTree = ET.parse('{}/values/strings.xml'.format(currentAbsolutePath))
defaultLanguageRoot = defaultLanguageTree.getroot()
defaultLanguageKeys = defaultLanguageRoot.findall('string')
secondLanguageRoot = None

resourcesFolderPath = input('Enter your resources folder path (leave empty if this script is inside the folder '
                            'already): ')
max_number_of_placeholders = input('Enter the max. number of placeholders in one string (default is 5): ')
if not max_number_of_placeholders:
    max_number_of_placeholders = 5
else:
    max_number_of_placeholders = int(max_number_of_placeholders)

for placeholder in placeholders:
    i = 0
    while i <= int(max_number_of_placeholders):
        if i == 0:
            full_list_of_placeholders.append('%{}'.format(placeholder))
        else:
            full_list_of_placeholders.append('%{}${}'.format(i, placeholder))
        i += 1


def filter_folders(folder_name):
    if 'night' in folder_name:
        return False
    if 'values-' in folder_name:
        return True
    else:
        return False


def get_languages():
    directory_list = list()
    for root, dirs, files in os.walk("./", topdown=False):
        for name in dirs:
            directory_list.append(os.path.join(root, name))

    filtered_directories = filter(filter_folders, directory_list)

    for directory in filtered_directories:
        languages.append(directory[-2::])


def validate_placeholders(default_string, second_language_string, string_key, language_code):
    incorrect_placeholders = []
    valid = True
    for placeholder in full_list_of_placeholders:
        default_language_placeholder_number = default_string.count(placeholder)
        second_language_placeholder_number = second_language_string.count(placeholder)
        if default_language_placeholder_number > second_language_placeholder_number:
            valid = False
            incorrect_placeholders.append(placeholder)

    if not valid:
        print('key "{}" is not valid, missing placeholders are: {}'.format(string_key, incorrect_placeholders))
        print('EN string: {}'.format(default_string))
        print('{} string: {}'.format(language_code.upper(), second_language_string))
        print('----------------------------------------------------------------------------------')

    return valid, incorrect_placeholders


def validate_languages():
    for language in languages:
        print('\n\n\n----------------------------------------------------------------------------------')
        print('-----------------------------------LANGUAGE: {}-----------------------------------'.format(
            language.upper()))
        print('----------------------------------------------------------------------------------')
        path = resourcesFolderPath if resourcesFolderPath else currentAbsolutePath

        second_language_tree = ET.parse('{}/values-{}/strings.xml'.format(path, language))
        second_language_root = second_language_tree.getroot()

        for default_language_string in defaultLanguageKeys:
            string_key = default_language_string.attrib['name']
            if default_language_string.text is None:
                continue
            if 'translatable' in default_language_string.attrib and default_language_string.attrib[
                'translatable'] == 'false':
                continue
            if check_if_string_exists_in_second_language(second_language_root, string_key):
                contains_placeholder = any(
                    placeholder in default_language_string.text for placeholder in full_list_of_placeholders)
                if not contains_placeholder:
                    continue
                second_language_string = second_language_root.findall("./*[@name='{}']".format(string_key))
                if second_language_string is None:
                    continue
                validate_placeholders(default_language_string.text, second_language_string[0].text, string_key, language)


def check_if_string_exists_in_second_language(second_language_root, string_key):
    second_language_string = second_language_root.findall("./*[@name='{}']".format(string_key))
    if len(second_language_string) == 0:
        print('!!!!!Key "{}" is not present in the second language. Maybe it should be added.!!!!!'.format(string_key))
        print('----------------------------------------------------------------------------------')
        return False
    else:
        return True


get_languages()
validate_languages()
