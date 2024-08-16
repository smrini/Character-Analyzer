from PyPDF2 import PdfReader
from collections import Counter
import matplotlib.pyplot as plt
import string
import time
import os

print("Welcome to the PDF Content Analyzer!")
print("This program reads a PDF file and analyzes the frequency of different characters in its content.")
print("Created by Said Mrini")
print()

def analyze_pdf(pdf_path):
    while True:
        try:
            # Create a PDF file reader
            pdf_reader = PdfReader(pdf_path)
    
            # Initialize an empty string to hold the text content of the PDF
            text_content = ''
    
            # Loop through each page in the PDF and extract the text
            for page in pdf_reader.pages:
                text_content += page.extract_text()

            # If the PDF is read successfully, break the loop
            break

        except Exception as e:
            print("An error occurred while reading the PDF file!")
            print(f"Invalid path:{pdf_path}")
            pdf_path = input("Please enter a valid path/url: ")

    # Initialize the counters with all letters and numbers set to zero
    letters = Counter({ch: 0 for ch in string.ascii_lowercase})
    numbers = Counter({ch: 0 for ch in string.digits})

    # Update the counters with the actual character frequencies
    letters.update(ch for ch in text_content.lower() if ch in string.ascii_lowercase)
    numbers.update(ch for ch in text_content if ch.isdigit())
    symbols = Counter(ch for ch in text_content if ch in string.punctuation)

    # Calculate the total number of characters of each type and the total number of characters in the whole document
    total_letters = sum(letters.values())
    total_numbers = sum(numbers.values())
    total_symbols = sum(symbols.values())
    total_characters = total_letters + total_numbers + total_symbols

    # Prepare data for the charts, sorted by frequency
    items_letters = sorted(letters.items(), key=lambda x: x[1], reverse=True)
    items_numbers = sorted(numbers.items(), key=lambda x: x[1], reverse=True)
    items_symbols = sorted(symbols.items(), key=lambda x: x[1], reverse=True)

    labels_letters, values_letters = zip(*items_letters)
    labels_numbers, values_numbers = zip(*items_numbers)
    labels_symbols, values_symbols = zip(*items_symbols)

    # Plot a bar chart of the character frequencies for lowercase letters
    plt.figure(figsize=(13, 6))
    plt.bar(labels_letters, values_letters)
    plt.title(f'Letters (Total: {total_letters}, Overall Total: {total_characters})')
    rotation_angle = 60 if any(v >= 10000 for v in values_letters) else 0
    for i, v in enumerate(values_letters):
        x_position = i + 0.2 if v >= 10000 else i
        plt.text(x_position, v, str(v), ha='center', va='bottom', rotation=rotation_angle)
    plt.ylim(0, max(values_letters)*1.2)  # Adjust y limits
    plt.tight_layout()
    plt.show()

    # Plot a bar chart of the character frequencies for numbers
    plt.figure(figsize=(13, 6))
    plt.bar(labels_numbers, values_numbers)
    plt.title(f'Numbers (Total: {total_numbers}, Overall Total: {total_characters})')
    rotation_angle = 60 if any(v >= 10000 for v in values_numbers) else 0
    for i, v in enumerate(values_numbers):
        x_position = i + 0.2 if v >= 10000 else i
        plt.text(x_position, v, str(v), ha='center', va='bottom', rotation=rotation_angle)
    plt.ylim(0, max(values_numbers)*1.2)  # Adjust y limits
    plt.tight_layout()
    plt.show()

    # Plot a bar chart of the character frequencies for symbols
    plt.figure(figsize=(13, 6))
    plt.bar(labels_symbols, values_symbols)
    plt.title(f'Symbols (Total: {total_symbols}, Overall Total: {total_characters})')
    rotation_angle = 60 if any(v >= 10000 for v in values_symbols) else 0
    for i, v in enumerate(values_symbols):
        x_position = i + 0.2 if v >= 10000 else i
        plt.text(x_position, v, str(v), ha='center', va='bottom', rotation=rotation_angle)
    plt.ylim(0, max(values_symbols)*1.2)  # Adjust y limits
    plt.tight_layout()
    plt.show()

    # Ask the user if they want to save the results
    while True:
        save_results = input("Do you want to save the results to a text file? (y/n): ").lower()
        if save_results not in ['y', 'n', 'yes', 'no']:
            print("Invalid input. Please enter 'y' or 'n'.")
            continue
        if save_results in ['y', 'yes']:
            try:
                # Get the current directory
                current_directory = os.getcwd()
                # Create the full path for the results file
                results_file_path = os.path.join(current_directory, 'results.txt')
                with open(results_file_path, 'w') as f:
                    f.write(f"characters frequency of the content in PDF file:\n{pdf_path}\n\n")
                    f.write(f"Total characters: {total_characters}\n\n")
                    f.write(f"Total letters: {total_letters}\n")
                    f.write(f"Total numbers: {total_numbers}\n")
                    f.write(f"Total symbols: {total_symbols}\n\n")
                    f.write("\nLetters:\n")
                    for letter, count in items_letters:
                        f.write(f"{letter}: {count}\n")
                    f.write("\nNumbers:\n")
                    for number, count in items_numbers:
                        f.write(f"{number}: {count}\n")
                    f.write("\nSymbols:\n")
                    for symbol, count in items_symbols:
                        f.write(f"{symbol}: {count}\n")
                print(f"Results saved to results.txt at {current_directory}")
                time.sleep(3)  # Wait for 3 seconds
            except Exception as e:
                print(f"An error occurred while trying to save the results: {e}")
        break

# Ask for the PDF file path
pdf_path = input("Please enter the path to the PDF file: ")

# Call the function with the entered PDF file path
analyze_pdf(pdf_path)