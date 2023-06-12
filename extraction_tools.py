import re
import sys
import os
import fitz
import numpy
import pandas as pd
import json

def get_path():
    #Gets the location of the data
    data_location = get_necessary_index()

    #Location of the file for parsing
    print("Enter the path to the location of the PDF IE \\home\\bob\\job\\folder")
    path_link = input("Path = ")

    #Specifies file name
    print("\nIf you want a new file instead of appending to the default one enter ie: bob.txt")
    file_name = input("Name = ")

    #Specifies path
    print("\nSpecify where you want it to be saved, otherwise it will be saved in the current location")
    print("IE: \\Personal-Projects\\PDF-Scraper")
    path_save = input("Path = ")

    #Default File name
    if not file_name:
        file_name = "bob.txt"

    #check if the path exists and create it if it does not
    if not os.path.exists(path_save) and path_save not in ('', None, "null"):
        os.makedirs(path_save)

    #Creates the path for the file otherwise defaults to the current directory
    if path_save:
        path_save = os.path.join(path_save, file_name)
    else:
        path_save = file_name

    with open(path_save, "a+") as my_file:
        my_file.write("data = {}\n".format(path_save))

    current_pdf = fitz.open("BlackFR-LaPresse-NRC(2020).pdf")
    page_count = current_pdf.page_count
    extracted_name = "Bob"
    extracted_date = "2022"
    extracted_pub_name = "jamieson morgans"
    fivan = open("testing.txt", "w+", encoding="utf-8")

    for p_num in range(page_count):
        current_page = current_pdf.load_page(p_num)
        page_text = current_page.get_text()
        #print(page_text)
        #fivan.write(page_text)
        #fivan.write("{}\n".format(page_text))
        #name_person = re.findall(r'\b[A-Z][a-zA-Z\'-]+\b', page_text)
        #name_person2 = re.findall(r'\b[a-zA-Z]+(([\',.-]?[a-zA-Z]*)*)', page_text)
        #fivan.write("{}\n".format(name_person))
        name_person = page_text.splitlines()
        #fivan.write("{}\n".format(name_person))
        #fivan.write("{}\n".format(page_text.split()))
        #print(json.dumps(get_data(page_text), indent=4))
        #fivan.write("{}\n".format(page_text))
        date_test = re.findall('\w{4,10} +\d{2} +\w{4,9} +\d{4}', page_text)
        regex_name = "^[A-ZÀÂÄÇÉÈÊËÎÏÔÖÙÛÜŸ][a-zA-ZÀ-Ÿ-.]* +[A-ZÀÂÄÇÉÈÊËÎÏÔÖÙÛÜŸ][a-zA-ZÀ-Ÿ-. ]*"
        #print("date ----- == {}\n".format(date_test))
        #fivan.write("person 2 {}\n".format(name_person2))

        if not data_location:
            extracted_name = name_person[0] + " " + name_person[1]
        else:
            index_pub_name = int(data_location.get("pub_name"))
            index_author = int(data_location.get("author"))
            extracted_pub_name = name_person[index_pub_name]
            extracted_name = name_person[index_author]
            while not re.match(regex_name, extracted_name) and index_author < 5:
                index_pub_name += 1
                index_author += 1
                extracted_pub_name = name_person[index_pub_name]
                extracted_name = name_person[index_author]

            extracted_date = date_test

        if date_test:
            fivan.write("extracted\n name = {},\n date = {},\n pud_name = {}\n-----------------\n".format(extracted_name, extracted_date, extracted_pub_name))
        #print(current_pdf.metadata)

    fivan.close()
    current_pdf.close()

def get_necessary_index():
    print("If this is a trial run enter nothing, otherwise enter no")
    trial_var = input("Is the a Trial Run to find proper index?")
    data_mapped = None
    if trial_var == "no":
        data_indexes = input("Separate the three inputs with a space = ").split()
        try:
            data_mapped = map_conversion(data_indexes)
        except:
            print("Incorrect data length it needs to be 2 or less.")
            print(len(data_indexes))
    return data_mapped

def map_conversion(lst):
    names_dict = ["pub_name", "author"]
    res_dct = {names_dict[i]: lst[i] for i in range(0, len(lst))}
    return res_dct


#testing json conversion
def get_data(page_content):
    _dict = {}
    page_content_list = page_content.splitlines()
    print(page_content_list)
    for line in page_content_list:
        if ':' not in line:
            continue
        key, value = line.split(':')
        _dict[key.strip()] = value.strip()
    return _dict