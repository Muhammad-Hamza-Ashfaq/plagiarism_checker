# CodexCue Python Internship -- Project-4__PLAGIARISM_CHECKER
# Muhammad Hamza Ashfaq -- h.ashfaq16@gmail.com


import nltk
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import tkinter as tk
from tkinter import filedialog, scrolledtext

nltk.download('punkt')
nltk.download('stopwords')

class PlagiarismChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Plagiarism Checker")
        self.root.geometry("800x600")
        
        # File selection
        tk.Label(root, text="Select Files to Compare:", font=('Arial', 12)).pack(pady=10)
        
        self.file1_label = tk.Label(root, text="File 1: Not selected", font=('Arial', 10))
        self.file1_label.pack()
        
        self.file2_label = tk.Label(root, text="File 2: Not selected", font=('Arial', 10))
        self.file2_label.pack()
        
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Select File 1", command=lambda: self.select_file(1)).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Select File 2", command=lambda: self.select_file(2)).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Check Plagiarism", command=self.check_plagiarism, 
                 bg='green', fg='white').grid(row=0, column=2, padx=5)
        
        # Results
        self.result_label = tk.Label(root, text="", font=('Arial', 12))
        self.result_label.pack(pady=10)
        
        self.text_display = scrolledtext.ScrolledText(root, width=80, height=20, font=('Arial', 10))
        self.text_display.pack(pady=10)
        
        self.file1_path = ""
        self.file2_path = ""
        self.ps = PorterStemmer()
    
    def select_file(self, file_num):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            if file_num == 1:
                self.file1_path = file_path
                self.file1_label.config(text=f"File 1: {file_path.split('/')[-1]}")
            else:
                self.file2_path = file_path
                self.file2_label.config(text=f"File 2: {file_path.split('/')[-1]}")
    
    def preprocess_text(self, text):
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        

        # Tokenize
        tokenizer = TreebankWordTokenizer()
        tokens = tokenizer.tokenize(text)
        
        # Remove stopwords and stem
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [self.ps.stem(word) for word in tokens if word not in stop_words]
        
        return filtered_tokens
    
    def calculate_similarity(self, tokens1, tokens2):
        # Create frequency distributions
        freq1 = nltk.FreqDist(tokens1)
        freq2 = nltk.FreqDist(tokens2)
        
        # Get all unique words
        all_words = list(set(tokens1 + tokens2))
        
        # Calculate dot product
        dot_product = sum(freq1[word] * freq2[word] for word in all_words)
        
        # Calculate magnitudes
        mag1 = sum(freq1[word] ** 2 for word in all_words) ** 0.5
        mag2 = sum(freq2[word] ** 2 for word in all_words) ** 0.5
        
        # Calculate cosine similarity
        if mag1 * mag2 == 0:
            return 0
        return dot_product / (mag1 * mag2)
    
    def check_plagiarism(self):
        if not self.file1_path or not self.file2_path:
            self.result_label.config(text="Please select both files!", fg='red')
            return
        
        # try:
        with open(self.file1_path, 'r') as f1, open(self.file2_path, 'r') as f2:
            text1 = f1.read()
            text2 = f2.read()
                
            tokens1 = self.preprocess_text(text1)
            tokens2 = self.preprocess_text(text2)
                
            similarity = self.calculate_similarity(tokens1, tokens2)
            similarity_percent = round(similarity * 100, 2)
                
            self.result_label.config(text=f"Similarity: {similarity_percent}%", fg='blue')
                
            # Display text comparison
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(tk.END, "=== File 1 ===\n")
            self.text_display.insert(tk.END, text1[:1000] + ("..." if len(text1) > 1000 else "") + "\n\n")
            self.text_display.insert(tk.END, "=== File 2 ===\n")
            self.text_display.insert(tk.END, text2[:1000] + ("..." if len(text2) > 1000 else ""))
                
        # except Exception as e:
            # self.result_label.config(text=f"Error: {str(e)}", fg='red')

if __name__ == "__main__":
    root = tk.Tk()
    app = PlagiarismChecker(root)
    root.mainloop()