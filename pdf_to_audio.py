import PyPDF2
import openai
from gtts import gTTS
import os
from dotenv import load_dotenv

class PaperToAudiobook:
    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.openai_api_key

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file."""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return None

    def summarize_text(self, text, target_length=2500):
        """
        Summarize text using OpenAI's API.
        Target length of 2500 words is approximately 20 minutes when spoken.
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": (
                        "You are a research paper summarizer. Create a clear, engaging summary "
                        "that captures the key points, methodology, results, and implications. "
                        "The summary should be suitable for audio narration and maintain academic rigor."
                    )},
                    {"role": "user", "content": f"Summarize this research paper in approximately {target_length} words: {text}"}
                ]
            )
            return response.choices[0].message['content']
        except Exception as e:
            print(f"Error summarizing text: {e}")
            return None

    def convert_to_audio(self, text, output_path="output.mp3"):
        """Convert text to audio using gTTS."""
        try:
            tts = gTTS(text=text, lang='en')
            tts.save(output_path)
            return True
        except Exception as e:
            print(f"Error converting to audio: {e}")
            return False

    def process_paper(self, pdf_path, output_audio_path="output.mp3"):
        """Process the paper from PDF to audio."""
        # Extract text from PDF
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            return False

        # Summarize the text
        summary = self.summarize_text(text)
        if not summary:
            return False

        # Convert to audio
        success = self.convert_to_audio(summary, output_audio_path)
        return success

def main():
    # Create instance of converter
    converter = PaperToAudiobook()
    
    # Process paper
    success = converter.process_paper("input.pdf")
    
    if success:
        print("Successfully converted paper to audiobook!")
    else:
        print("Error occurred during conversion.")

if __name__ == "__main__":
    main()