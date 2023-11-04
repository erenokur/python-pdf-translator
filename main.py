import os
from pdf2docx import parse
import argostranslate.package, argostranslate.translate
import argostranslatefiles
from argostranslatefiles import argostranslatefiles

# Select languages
from_code = "en"
to_code = "tr"

# Download and install Argos Translate package
argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()
package_to_install = next(
    filter(
        lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
    )
)
argostranslate.package.install_from_path(package_to_install.download())

# load installed languages
installed_languages = argostranslate.translate.get_installed_languages()
from_lang = list(filter(
    lambda x: x.code == from_code,
    installed_languages))[0]
to_lang = list(filter(
    lambda x: x.code == to_code,
    installed_languages))[0]
underlying_translation = from_lang.get_translation(to_lang)

# Get the current working directory where the script is located
current_directory = os.path.dirname(os.path.abspath(__file__))

# Define the directory name you want to search
directory_to_search = "PDF's"

# Combine the current directory path with the directory to search
search_directory = os.path.join(current_directory, directory_to_search)

# Convert PDF files to docx files
def convert_to_docx(file):
    # Get the file name without the extension
    file_name = os.path.splitext(file)[0]

    # Get the file extension
    file_extension = os.path.splitext(file)[1]

    # Check if the file is a PDF file
    if file_extension == ".pdf":
        # Create a path to the PDF file
        pdf_file_path = os.path.join(search_directory, file)

        # Create a path to the docx file
        docx_file_path = os.path.join(search_directory, f"{file_name}.docx")

        # Convert the PDF file to a docx file
        parse(pdf_file_path, docx_file_path, start=0, end=None)

        # Print a message to indicate that the conversion was successful
        print(f"Successfully converted '{file}' to '{file_name}.docx'.")
        return docx_file_path

# Check if the directory exists
if os.path.exists(search_directory) and os.path.isdir(search_directory):
    # Use os.listdir to get a list of all files in the search directory
    all_files = [file for file in os.listdir(search_directory) if os.path.isfile(os.path.join(search_directory, file))]

    # Now, 'all_files' contains the names of all files in the "PDF's" directory
    print("List of files in the 'PDF's' directory:")
    for file in all_files:
        argostranslatefiles.translate_file(underlying_translation, os.path.abspath(convert_to_docx(file)))
else:
    os.mkdir(search_directory)
    print(f"The '{directory_to_search}' directory does not exist in the current directory. Now, it has been created.")
