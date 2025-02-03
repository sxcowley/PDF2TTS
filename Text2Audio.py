import PyPDF2
from tkinter import Tk, filedialog
from gtts import gTTS
import os
import pyttsx3

def select_file():
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    return file_path

def get_page_range(prompt_message):
    while True:
        try:
            start_page = int(input(prompt_message))
            if start_page < 1:
                print("Please enter a valid page number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value for the page range.")
    return start_page

def main():
    # Get file path from user selection
    file_path = select_file()
    if not file_path:
        print("No file selected. Exiting...")
        return

    print(f"Selected PDF file: {file_path}")

    # Initialize the text-to-speech engine with no additional messages (silent mode)
    tts_engine = pyttsx3.init()
    tts_engine.setProperty('rate', 150)  # Optional: Adjust speech rate
    tts_engine.setProperty('volume', 1.0)  # Optional: Set volume level

    # Open and read the PDF file
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Get user input for page range
    start_page = get_page_range("Enter the starting page number: ")
    end_page = get_page_range("Enter the ending page number (inclusive): ")

    print(f"Reading pages from {start_page} to {end_page}...")

    # Determine the path to the Downloads folder
    downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')

    # Extract and read the text from each page in the specified range
    for page_num in range(start_page - 1, end_page):
        if page_num < len(pdf_reader.pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()

            print(f"Processing Page {page_num + 1}...")

            # Save the speech to a file in the Downloads folder
            tts = gTTS(text=text, lang='en')
            mp3_file_path = os.path.join(downloads_path, f"page_{page_num + 1}.mp3")
            tts.save(mp3_file_path)
            print(f"Page {page_num + 1} saved as '{mp3_file_path}'.")

            # Optionally, play the saved audio
            os.system(f"start {mp3_file_path}")

        else:
            print("End of PDF reached. No more pages to read.")
            break

    # Run the engine to speak the text (optional)
    tts_engine.say("PDF processing complete.")
    tts_engine.runAndWait()

    # Close the PDF file
    pdf_file.close()
    print("PDF processing complete.")

if __name__ == "__main__":
    main()
