import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from collections import Counter
import matplotlib.pyplot as plt
import string
import time
import os

print("Welcome to the Webpage Content Analyzer!")
print("This program fetches a webpage and analyzes the frequency of different characters in its content.")
print("Created by Said Mrini")
print()

def analyze_url(url):
    while True:
        try:
            # Fetch the webpage
            response = requests.get(url)

            # Check if the request was successful
            response.raise_for_status()
            break  # Break out of the loop if the request was successful
        except RequestException as e:
            # Split the error message at the first colon and take the first part
            error_message = str(e).split(":")[0]
            print(f"An error occurred while fetching the webpage: {error_message} \n")
            url = input("Please enter a valid URL: ")  # Ask the user to enter a valid URL

    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the text content of the webpage
    text_content = soup.get_text()

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
                    f.write(f"characters frequency of the content on URL:\n{url}\n\n")
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

# Ask for the URL
url = input("Please enter the URL: ")

# Call the function with the entered URL
analyze_url(url)