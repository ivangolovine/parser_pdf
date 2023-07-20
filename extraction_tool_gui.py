import re
import sys
import os
import fitz
import numpy
import pandas as pd
import json


#Possibly replace the no date with checking if there is enough indexes instead

def list_of_files(file_paths, file_name_txt, file_name_xml, path_save, trial_run_enable, data_indexes):
    count = 0
    for file_path in file_paths:
        count += 1
        file_name_xml_export = file_name_xml + str(count)
        len_file = len(file_path)
        file_extension = file_path[len_file - 4:len_file]
        if file_extension == ".pdf":
            print(file_path[len_file-4:len_file])
            get_path(file_path, file_name_txt, path_save, trial_run_enable, data_indexes)
        else:
            print("Test")

        convert_to_excel("testing2.txt", file_name_xml_export, path_save)



def get_path(file_path, file_name, path_save, trial_run_enable, data_indexes):
    #Gets the location of the data
    data_location = get_necessary_index(trial_run_enable, data_indexes)
    #Location of the file for parsing
    path_link = os.path.join(file_path)
    #Specifies the output type
    file_type = "xlsx"


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

    with open(path_save,  "w+", encoding="utf-8") as my_file:
        my_file.write("data = {}\n".format(path_save))

    current_pdf = fitz.open(path_link)

    page_count = current_pdf.page_count
    extracted_name = "Bob"
    extracted_date = "2022"
    extracted_pub_name = "jamieson morgans"

    fivan = open("demofile.txt", "w+", encoding="utf-8")
    fTesting = open("testing.txt", "w+", encoding="utf-8")
    fconv_file = open("testing2.txt", "w+", encoding="utf-8")
    fconv_file.write(
        "Title\tStoreId\tArticleType\tAuthors\tcompanies\tcopyright\tdocumentType\tentryDate\tissn\tlanguage\tlanguageOfSummary\tplaceOfPublication\tpubdate\tpubtitle\tyear\tDocumentURL\tclassification\tclassificationCodes\tidentifierKeywords\tmajorClassificationCodes\tstartPage\tsubjectClassifications\tsubjectTerms\tsubjects\tFindACopy\tDatabase\n")

    for p_num in range(page_count):
        current_page = current_pdf.load_page(p_num)
        page_text = current_page.get_text()
        name_person = page_text.splitlines()
        fTesting.write("%s\n" % name_person)
        date_test = re.findall('\w{4,10} +\d{2} +\w{4,9} +\d{4}', page_text)
        regex_name = "^[A-ZÀÂÄÇÉÈÊËÎÏÔÖÙÛÜŸ][a-zA-ZÀ-Ÿ-.]* +[A-ZÀÂÄÇÉÈÊËÎÏÔÖÙÛÜŸ][a-zA-ZÀ-Ÿ-. ]*"

        if not data_location or not date_test:
            continue
        else:
            index_pub_name = int(data_location.get("pub_name"))
            index_author = int(data_location.get("author"))
            extracted_pub_name = name_person[index_pub_name]
            extracted_name = name_person[index_author]
            while index_author < len(name_person):
                extracted_pub_name = name_person[index_pub_name]
                extracted_name = name_person[index_author]
                if "La Presse" in extracted_name or "La Presse" in extracted_pub_name:
                    index_pub_name += 1
                    index_author += 1
                    continue

                if re.match(regex_name, extracted_name):
                    if extracted_pub_name[0].islower():
                        extracted_pub_name = name_person[index_pub_name-1] + " " + name_person[index_pub_name]
                    break
                index_pub_name += 1
                index_author += 1

        if date_test:
            extracted_date = date_test[0]
            fivan.write("extracted\n name = {},\n date = {},\n pud_name = {}\n-----------------\n".format(extracted_name, extracted_date, extracted_pub_name))
        if date_test and file_type == "xlsx":
            extracted_date = date_test[0]
            fconv_file.write("{}\t\t\t{}\t\t\t\t\t\t\t\t\t{}\n".format(extracted_pub_name, extracted_name, extracted_date))

        #print(current_pdf.metadata)
    current_pdf.close()
    fivan.close()
    fTesting.close()
    fconv_file.close()
def get_necessary_index(trial_run_enable, data_indexes):
    data_mapped = None
    if trial_run_enable == 0:
        print("{}".format(data_indexes.split()))
        try:
            data_mapped = map_conversion(data_indexes.split())
        except:
            print("Incorrect data length it needs to be 2 or less.")
            print(len(data_indexes))
    return data_mapped

def map_conversion(lst):
    names_dict = ["pub_name", "author"]
    res_dct = {names_dict[i]: lst[i] for i in range(0, len(lst))}
    return res_dct

def convert_to_excel(conv_file, file_name_xml, path_save):
    file_name_xml = validate_path_save(path_save, file_name_xml)
    df = pd.read_csv(conv_file, sep="\t")
    df.to_excel(file_name_xml + '.xlsx', 'Sheet1', index=False)

def validate_path_save(path_save, file_name):
    # check if the path exists and create it if it does not
    if not os.path.exists(path_save) and path_save not in ('', None, "null"):
        os.makedirs(path_save)

    # Creates the path for the file otherwise defaults to the current directory
    if path_save:
        path_save = os.path.join(path_save, file_name)
    else:
        path_save = file_name

    return path_save