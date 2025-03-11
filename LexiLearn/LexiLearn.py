import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import random

class VocabularyApp:
    def __init__(self, master):
        self.master = master
        self.master.title("LexiLearn")
        self.master.geometry("800x600")
        
        # Load the Excel file with all units (sheets)
        self.data = self.load_data("Vocab.xlsx")
        self.units = list(self.data.keys())
        self.current_unit = None
        self.vocab_list = []  # List to hold the vocab cards for the chosen unit
        
        # Variables for flashcard review
        self.current_index = 0
        
        # Variables for test mode
        self.score = 0
        self.total_questions = 0
        
        # Create the main menu frame
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill="both", expand=True)
        self.create_main_menu()
    
    def load_data(self, filename):
        """
        Loads the Excel file and converts each sheet to a list of dictionaries.
        Each key of the returned dict is the unit name.
        """
        try:
            # Read all sheets from the Excel file
            data = pd.read_excel(filename, sheet_name=None)
            # Convert each dataframe to a list of records (dictionaries)
            for unit, df in data.items():
                data[unit] = df.to_dict(orient="records")
            return data
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")
            self.master.destroy()
    
    def create_main_menu(self):
        # Clear any widgets in main_frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        title_label = tk.Label(self.main_frame, text="Vocabulary Review App", font=("Helvetica", 20))
        title_label.pack(pady=20)
        
        unit_label = tk.Label(self.main_frame, text="Select Unit:", font=("Helvetica", 16))
        unit_label.pack(pady=10)
        
        # Create a drop-down to select a unit (sheet)
        self.unit_var = tk.StringVar()
        self.unit_var.set(self.units[0])
        unit_dropdown = ttk.Combobox(self.main_frame, textvariable=self.unit_var, values=self.units, state="readonly", font=("Helvetica", 14))
        unit_dropdown.pack(pady=5)
        
        # Buttons to choose between review and test modes
        review_button = tk.Button(self.main_frame, text="Review Mode", font=("Helvetica", 14), width=20, command=self.start_review_mode)
        review_button.pack(pady=10)
        
        test_button = tk.Button(self.main_frame, text="Test Mode", font=("Helvetica", 14), width=20, command=self.start_test_mode)
        test_button.pack(pady=10)
    
    # ----------------------- Flashcard Review Mode -----------------------
    def start_review_mode(self):
        self.current_unit = self.unit_var.get()
        # Copy the list of vocabulary items for the chosen unit and shuffle them
        self.vocab_list = self.data[self.current_unit].copy()
        random.shuffle(self.vocab_list)
        self.current_index = 0
        
        # Create a new frame for review mode and hide the main menu frame
        self.review_frame = tk.Frame(self.master)
        self.review_frame.pack(fill="both", expand=True)
        self.main_frame.pack_forget()
        
        # Flashcard front (Word) and details (other info)
        self.card_front = tk.Label(self.review_frame, text="", font=("Helvetica", 28), wraplength=750)
        self.card_front.pack(pady=40)
        
        self.detail_label = tk.Label(self.review_frame, text="", font=("Helvetica", 16), wraplength=750)
        self.detail_label.pack(pady=10)
        
        # Buttons for flipping, navigating cards, and going back to the menu
        flip_button = tk.Button(self.review_frame, text="Flip Card", font=("Helvetica", 14), command=self.flip_card)
        flip_button.pack(pady=10)
        
        next_button = tk.Button(self.review_frame, text="Next Card", font=("Helvetica", 14), command=self.next_card)
        next_button.pack(pady=10)
        
        back_button = tk.Button(self.review_frame, text="Back to Menu", font=("Helvetica", 14), command=self.back_to_menu_from_review)
        back_button.pack(pady=10)
        
        # Initially show the front of the first card
        self.show_card(front=True)
    
    def show_card(self, front=True):
        if self.current_index < 0 or self.current_index >= len(self.vocab_list):
            messagebox.showinfo("Info", "No more cards in this unit.")
            return
        
        card = self.vocab_list[self.current_index]
        if front:
            # Only show the word
            self.card_front.config(text=card.get("Word", ""))
            self.detail_label.config(text="")
        else:
            # Show full details from the card
            details = f"Persian Meaning: {card.get('Persian meaning', '')}\n"
            details += f"Part of Speech: {card.get('parts of speech', '')}\n"
            details += f"Definition: {card.get('Definition', '')}\n"
            details += f"Pronunciation: {card.get('Pronunciation', '')}\n"
            details += f"Examples: {card.get('Examples', '')}"
            self.detail_label.config(text=details)
    
    def flip_card(self):
        # If details are not shown, flip to show them; if already shown, flip back.
        if self.detail_label.cget("text") == "":
            self.show_card(front=False)
        else:
            self.show_card(front=True)
    
    def next_card(self):
        self.current_index += 1
        if self.current_index >= len(self.vocab_list):
            messagebox.showinfo("Info", "You have reviewed all cards in this unit. Restarting the deck.")
            self.current_index = 0
            random.shuffle(self.vocab_list)
        self.show_card(front=True)
    
    def back_to_menu_from_review(self):
        self.review_frame.destroy()
        self.main_frame.pack(fill="both", expand=True)
    
    # ----------------------- Test Mode -----------------------
    def start_test_mode(self):
        self.current_unit = self.unit_var.get()
        self.vocab_list = self.data[self.current_unit].copy()
        random.shuffle(self.vocab_list)
        self.current_index = 0
        self.score = 0
        self.total_questions = 0
        
        # Create a new frame for test mode and hide main menu
        self.test_frame = tk.Frame(self.master)
        self.test_frame.pack(fill="both", expand=True)
        self.main_frame.pack_forget()
        
        self.question_label = tk.Label(self.test_frame, text="", font=("Helvetica", 18), wraplength=750)
        self.question_label.pack(pady=20)
        
        # Variable and radio buttons for multiple-choice answers
        self.answer_var = tk.StringVar()
        self.option_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(self.test_frame, text="", variable=self.answer_var, value="", font=("Helvetica", 14))
            rb.pack(anchor="w", padx=50, pady=5)
            self.option_buttons.append(rb)
        
        self.submit_button = tk.Button(self.test_frame, text="Submit Answer", font=("Helvetica", 14), command=self.submit_answer)
        self.submit_button.pack(pady=10)
        
        self.feedback_label = tk.Label(self.test_frame, text="", font=("Helvetica", 16))
        self.feedback_label.pack(pady=10)
        
        next_button = tk.Button(self.test_frame, text="Next Question", font=("Helvetica", 14), command=self.next_question)
        next_button.pack(pady=10)
        
        back_button = tk.Button(self.test_frame, text="Back to Menu", font=("Helvetica", 14), command=self.back_to_menu_from_test)
        back_button.pack(pady=10)
        
        self.generate_question()
    
    def generate_question(self):
        """
        Creates a multiple-choice question asking for the Persian meaning of a word.
        One option is correct and three others are chosen as distractors.
        """
        if not self.vocab_list:
            messagebox.showinfo("Info", "No vocabulary available for this unit.")
            return
        
        self.current_card = random.choice(self.vocab_list)
        word = self.current_card.get("Word", "")
        correct_answer = self.current_card.get("Persian meaning", "")
        
        self.question_label.config(text=f"What is the Persian meaning of the word: {word}?")
        
        # Get distractor answers (ensure they are different from the correct answer)
        distractors = [card.get("Persian meaning", "") for card in self.vocab_list if card.get("Persian meaning", "") != correct_answer]
        if len(distractors) >= 3:
            wrong_answers = random.sample(distractors, 3)
        else:
            wrong_answers = distractors.copy()
            # If there are not enough distractors, fill with "N/A"
            while len(wrong_answers) < 3:
                wrong_answers.append("N/A")
        
        options = [correct_answer] + wrong_answers
        random.shuffle(options)
        self.correct_option = correct_answer
        
        self.answer_var.set("")  # Reset selection
        for i, rb in enumerate(self.option_buttons):
            rb.config(text=options[i], value=options[i])
        
        self.feedback_label.config(text="")
    
    def submit_answer(self):
        selected = self.answer_var.get()
        if not selected:
            messagebox.showwarning("Warning", "Please select an answer!")
            return
        
        self.total_questions += 1
        if selected == self.correct_option:
            self.score += 1
            self.feedback_label.config(text="Correct!", fg="green")
        else:
            self.feedback_label.config(text=f"Incorrect! The correct answer was: {self.correct_option}", fg="red")
    
    def next_question(self):
        self.generate_question()
    
    def back_to_menu_from_test(self):
        if messagebox.askyesno("Exit Test", "Are you sure you want to exit? Your progress will be lost."):
            self.test_frame.destroy()
            self.main_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = VocabularyApp(root)
    root.mainloop()
