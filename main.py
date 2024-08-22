import time
import tkinter as tk
import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pygame
from PIL import Image, ImageTk 

# Initialize pygame mixer
pygame.mixer.init()


class SerialReactionTimeTask:
    def __init__(self, root):
        self.root = root
        self.root.title("Serial Reaction Time")
        self.root.geometry("1920x1080")
        self.root.configure(bg="dark slate grey")

        # Show the instructions popup
        self.show_instructions_popup()

        # Create a frame to hold the Start Trial button
        button_frame = tk.Frame(self.root, bg="gray")
        button_frame.pack(side="right", pady=50)

        # Create a button for starting the trial
        self.start_trial_button = tk.Button(button_frame, text="Start Trial", command=self.start_trial)
        self.start_trial_button.pack(pady=5)

        # Initialize other variables
        self.current_block = 0
        self.current_position = 0
        self.user_inputs = []
        self.correct_score = 0
        self.incorrect_score = 0

        # Heading label for trial block
        self.heading_label = tk.Label(self.root, text="", bg="gray", fg="black", font=("Arial", 18, "bold"))
        self.heading_label.pack(pady=20)

        # Main canvas for central display
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='snow2')
        self.canvas.pack(padx=10, pady=10)

        # Create left and right canvases and pack them side by side
        self.left_canvas = tk.Canvas(self.root, width=400, height=400, bg="dark slate grey")
        self.left_canvas.pack(side="left", padx=20, pady=20)  # Adjust padx and pady for spacing

        self.right_canvas = tk.Canvas(self.root, width=400, height=400, bg="dark slate grey")
        self.right_canvas.pack(side="right", padx=20, pady=20)  # Adjust padx and pady for spacing


        # Message label to display instructions
        self.message_label = tk.Label(self.root, text="", bg="gray", fg="black", font=("Arial", 14))
        self.message_label.pack(pady=20)

        # Define blocks for each trial
        self.blocks = [
            [1, 2, 4, 3, 2, 1, 4, 3, 1, 2, 1, 2, 4, 3, 2, 1, 4, 3, 1, 2, 1, 2, 4, 3, 2, 1, 4, 3, 1, 2, 1, 2, 4, 3, 2, 1, 4, 3, 1, 2, 1, 2, 4, 3, 2, 1, 4, 3, 1, 2, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2],
            [3, 4, 1, 2, 4, 1, 3, 4, 2, 1, 3, 4, 1, 2, 4, 1, 3, 4, 2, 1, 3, 4, 1, 2, 4, 1, 3, 4, 2, 1, 3, 4, 1, 2, 4, 1, 3, 4, 2, 1, 3, 4, 1, 2, 4, 1, 3, 4, 2, 1, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2],
            [1, 3, 2, 4, 3, 1, 4, 2, 1, 3, 1, 3, 2, 4, 3, 1, 4, 2, 1, 3, 1, 3, 2, 4, 3, 1, 4, 2, 1, 3, 1, 3, 2, 4, 3, 1, 4, 2, 1, 3, 1, 3, 2, 4, 3, 1, 4, 2, 1, 3, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2],
            [4, 1, 3, 2, 1, 4, 2, 3, 1, 4, 4, 1, 3, 2, 1, 4, 2, 3, 1, 4, 4, 1, 3, 2, 1, 4, 2, 3, 1, 4, 4, 1, 3, 2, 1, 4, 2, 3, 1, 4, 4, 1, 3, 2, 1, 4, 2, 3, 1, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2],
            [2, 4, 3, 1, 4, 2, 1, 3, 4, 1, 2, 4, 3, 1, 4, 2, 1, 3, 4, 1, 2, 4, 3, 1, 4, 2, 1, 3, 4, 1, 2, 4, 3, 1, 4, 2, 1, 3, 4, 1, 2, 4, 3, 1, 4, 2, 1, 3, 4, 1, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2],
            [2, 1, 4, 3, 1, 4, 2, 1, 3, 4, 2, 1, 4, 3, 1, 4, 2, 1, 3, 4, 2, 1, 4, 3, 1, 4, 2, 1, 3, 4, 2, 1, 4, 3, 1, 4, 2, 1, 3, 4, 2, 1, 4, 3, 1, 4, 2, 1, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2],
            [3, 1, 4, 2, 4, 3, 2, 1, 4, 3, 2, 4, 1, 3, 2, 1, 4, 3, 1, 2, 1, 3, 2, 4, 3, 1, 4, 2, 1, 4, 4, 2, 3, 1, 2, 4, 3, 1, 4, 2, 2, 3, 1, 4, 3, 2, 1, 4, 3, 1, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2]
        ]

        # Updated shape and color mappings
        self.shape_mapping = [
            "circle",
            "triangle",
            "oval",
            "diamond",
            "rectangle",
            "hexagon",
            "star",
            "pentagon",
            "ellipse",
            "octagon"
        ]

        self.color_mapping = [
            "red", "blue", "yellow", "pink", "green", "purple", "orange", "brown", "indian red", "cyan"
        ]


        # Bind key presses to the corresponding methods
        self.root.bind("<KeyPress>", self.record_input)

        self.footer_label = tk.Label(self.root, text="Dr. Mehwish Qamar | dr.qamarmehwish@gmail.com | Universiti Sains Malaysia",
                                      bg="white", fg="black", font=("Arial", 12, "bold"))
        self.footer_label.pack(side=tk.BOTTOM, pady=50)

        self.download_button = None  # Initialize download button as None

        self.horizontal_positions = [100, 300, 500, 700]  # X-coordinates for positions 1, 2, 3, 4

        self.trial_active = False  # Variable to track trial state

        self.alarm_sound = pygame.mixer.Sound("./345061__metrostock99__annoying-modern-office-building-alarm.wav")

        # Initialize results tracking
        self.block_results = []

        # Update the display to include score information
        self.update_score_display()

        # Initialize the total score
        self.total_score = 0

        # Create a button for restarting the trial
        self.restart_trial_button = tk.Button(button_frame, text="Restart Trial", command=self.restart_trial, state=tk.DISABLED)
        self.restart_trial_button.pack(pady=5)

        self.trial_start_time = None

        self.shape_displayed = False  # Flag to indicate if a shape is currently being displayed

        # To prevent multiple inputs being recorded
        self.input_recorded = False

    def update_score_display(self):
        # Clear the left canvas
        self.left_canvas.delete("all")
        
        # Display the total score
        if self.current_block not in [0, 1]:  # Show score only for blocks other than 1 and 2
            self.left_canvas.create_text(200, 100, text=f"{self.total_score}", font=("Arial", 80, "bold"), fill="white")

    def show_instructions_popup(self):
        # Create a new top-level window
        popup = tk.Toplevel(self.root)
        popup.title("Instructions")
        popup.geometry("800x300")
        popup.configure(bg="cadet blue")

        # Create a frame to hold the instructions and the close button
        frame = tk.Frame(popup, bg="cadet blue")
        frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Create a label for instructions
        instructions = tk.Label(frame, text="Welcome to the Serial Reaction Time Task!\n\n"
                                            "In each trial, a shape will appear on the screen.\n"
                                            "Press the corresponding key (H, J, K, or L) as soon as you see the shape.\n"
                                            "Try to respond as quickly and accurately as possible.\n\n"
                                            "Press the 'Start Trial' button to begin the trial.\n\n"
                                            "Good luck!",
                                bg="wheat1", font=("Time New Roman", 12))
        instructions.pack(pady=10)

        # Create a button to close the popup
        close_button = tk.Button(frame, text="Close", command=popup.destroy)
        close_button.pack(pady=10)

        # Center the popup on the main window
        popup.transient(self.root)  # Set popup as a child of the root window
        popup.grab_set()  # Make the popup modal

    def start_trial(self):
        if self.trial_active:
            return

        self.trial_active = True
        self.current_position = 0
        self.user_inputs.clear()
        self.correct_score = 0
        self.incorrect_score = 0

        self.total_score = 0  # Reset the total score for the new block

        self.heading_label.config(text=f"Trial Block {self.current_block + 1}")
        self.canvas.delete("all")  # Clear any existing shapes

        if self.current_block in [4, 5]:
            self.alarm_sound.play(-1)

        if self.current_block == 0:
            # Schedule the start of Block 0 after a 3-second delay
            self.root.after(3000, self.display_trial)
        else:
            # Start the trial immediately if it's not Block 0
            self.display_trial()

    def gray_screen(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, 800, 600, fill='gray')  # Gray screen
        self.root.after(800, self.next_shape)
        
    def next_shape(self):
        if not self.trial_active:
            return
        self.root.bind("<KeyPress>", self.record_input)
        # self.current_position += 1
        if self.current_position >= len(self.blocks[self.current_block]):
            
            self.end_trial()
        else:
            self.display_trial()

    def display_trial(self):
        if not self.trial_active:
            return

        # Ensure no other shape is displayed if one is already shown
        if self.shape_displayed:
            return
        # Record the start time when the shape is displayed
        self.trial_start_time = time.time()

        # Ensure current_position is within bounds
        if self.current_position >= len(self.blocks[self.current_block]):
            self.end_trial()  # End trial if no more values are left
            return

        horizontal_positions = self.horizontal_positions
        sequence_number = self.blocks[self.current_block][self.current_position]
        shape = random.choice(self.shape_mapping)  # Default to circle if not found
        color = random.choice(self.color_mapping)
    
        self.canvas.delete("all")
        position_index = sequence_number - 1
        x_position = horizontal_positions[position_index]


        scale_factor = 1.5
        base_length = 150
        height = 100

        if shape == "diamond": 
            self.canvas.create_oval(
                x_position - 50 * scale_factor, 270 - 50 * scale_factor,
                x_position + 50 * scale_factor, 330 + 50 * scale_factor,
                fill=color
            )
        elif shape == "triangle":
            self.canvas.create_polygon(
                x_position, 300 - height * scale_factor,
                x_position - base_length // 2, 300 + height * scale_factor,
                x_position + base_length // 2, 300 + height * scale_factor,
                fill=color
            )
        elif shape == "oval":
            self.canvas.create_oval(
                x_position - 50 * scale_factor, 290 - 50 * scale_factor,
                x_position + 50 * scale_factor, 330 + 50 * scale_factor,
                fill=color
            )
        elif shape == "circle":
            self.canvas.create_polygon(
                x_position, 300 - height * scale_factor,
                x_position - base_length // 2, 300 + height * scale_factor,
                x_position + base_length // 2, 300 + height * scale_factor,
                fill=color
            )
        elif shape == "rectangle":
            self.canvas.create_rectangle(
                x_position - 50 * scale_factor, 300 - 25 * scale_factor,
                x_position + 50 * scale_factor, 300 + 25 * scale_factor,
                fill=color
            )
        elif shape == "hexagon":
            points = [
                (x_position, 300 - height * scale_factor),
                (x_position + base_length * scale_factor * 0.5, 300 - height * scale_factor * 0.5),
                (x_position + base_length * scale_factor * 0.5, 300 + height * scale_factor * 0.5),
                (x_position, 300 + height * scale_factor),
                (x_position - base_length * scale_factor * 0.5, 300 + height * scale_factor * 0.5),
                (x_position - base_length * scale_factor * 0.5, 300 - height * scale_factor * 0.5)
            ]
            self.canvas.create_polygon(points, fill=color)
        elif shape == "star":
            # Calculate points for a 5-pointed star
            points = [
                (x_position, 300 - 60 * scale_factor),  # Top point
                (x_position + 20 * scale_factor, 300 - 20 * scale_factor),  # Upper right
                (x_position + 60 * scale_factor, 300 - 20 * scale_factor),  # Right point
                (x_position + 30 * scale_factor, 300 + 10 * scale_factor),  # Lower right
                (x_position + 40 * scale_factor, 300 + 50 * scale_factor),  # Lower middle
                (x_position, 300 + 20 * scale_factor),  # Bottom point
                (x_position - 40 * scale_factor, 300 + 50 * scale_factor),  # Lower middle left
                (x_position - 30 * scale_factor, 300 + 10 * scale_factor),  # Lower left
                (x_position - 60 * scale_factor, 300 - 20 * scale_factor),  # Left point
                (x_position - 20 * scale_factor, 300 - 20 * scale_factor)   # Upper left
            ]
            self.canvas.create_polygon(points, fill=color)

        elif shape == "pentagon":
            points = [
                (x_position, 300 - height * scale_factor),
                (x_position + base_length * scale_factor * 0.5, 300 - height * scale_factor * 0.5),
                (x_position + base_length * scale_factor * 0.5, 300 + height * scale_factor * 0.5),
                (x_position, 300 + height * scale_factor),
                (x_position - base_length * scale_factor * 0.5, 300 + height * scale_factor * 0.5),
                (x_position - base_length * scale_factor * 0.5, 300 - height * scale_factor * 0.5)
            ]
            self.canvas.create_polygon(points, fill=color)
        elif shape == "ellipse":
            self.canvas.create_oval(
                x_position - 50 * scale_factor, 270 - 30 * scale_factor,
                x_position + 50 * scale_factor, 330 + 30 * scale_factor,
                fill=color
            )
        elif shape == "octagon":
            points = [
                (x_position + 50 * scale_factor, 300 - 50 * scale_factor),
                (x_position + 30 * scale_factor, 300 - 30 * scale_factor),
                (x_position + 30 * scale_factor, 300 + 30 * scale_factor),
                (x_position + 50 * scale_factor, 300 + 50 * scale_factor),
                (x_position, 300 + 50 * scale_factor),
                (x_position - 30 * scale_factor, 300 + 30 * scale_factor),
                (x_position - 30 * scale_factor, 300 - 30 * scale_factor),
                (x_position, 300 - 50 * scale_factor)
            ]
            self.canvas.create_polygon(points, fill=color)
        
        # Record the time when the shape is displayed
        self.current_shape_time = time.time()
        
        self.root.after(800, self.gray_screen)

        # Mark the shape as displayed
        self.shape_displayed = True
        # Set up to remove the shape and reset the flag after 600 ms
        self.root.after(800, self.reset_shape_flag)
        self.root.after(500, self.gray_screen)
        self.root.after(800, self.clear_right_canvas)
        self.current_position += 1
        print(f"current block {self.current_block} -- current position {self.current_position}")
        
    def reset_shape_flag(self):
        # Clear the canvas and reset the shape display flag
        self.canvas.delete("all")
        self.shape_displayed = False
        self.next_shape()

    def record_input(self, event):
        if not self.trial_active:
            return  # Ignore key presses if trial is not active

        key_mapping = {'h': 1, 'j': 2, 'k': 3, 'l': 4}
        
        if event.char in key_mapping:
            user_input = key_mapping[event.char]

            # Ensure trial_start_time is set before calculating reaction time
            if self.trial_start_time is not None:
                # Calculate reaction time
                reaction_time = (time.time() - self.trial_start_time) * 1000  # Convert to milliseconds

                # Check the user input with the calculated reaction time
                self.check_input(user_input, reaction_time)
            else:
                print("Error: Trial start time is not set")
            
            # Check if all values have been processed
            if self.current_position < len(self.blocks[self.current_block]):
                #self.current_position += 1  # Move to the next expected position
                self.display_trial()  # Display the trial again
            else:
                self.end_trial()  # End trial if no more values are left
        
    def check_input(self, user_input, reaction_time):
        reaction_time_ms = round(reaction_time)
        expected_value = self.blocks[self.current_block][self.current_position - 1]
        is_correct = user_input == expected_value

        if is_correct:
            self.total_score += 5  # Add 5 points for correct response
            self.correct_score += 1  # Increase correct score
            # Show green tick for correct input
            if self.current_block not in [0, 1]:  # Skip drawing for Block 1 and Block 2
                self.draw_green_tick()
        else:
            self.total_score -= 6  # Deduct 6 points for incorrect response
            self.incorrect_score += 1  # Increase incorrect score
            # Show red cross for incorrect input
            if self.current_block not in [0, 1]:  # Skip drawing for Block 1 and Block 2
                self.draw_red_cross()

        # Add reaction time and correctness to the block results
        self.block_results.append({
            'block': self.current_block + 1,
            'trial': self.current_position,
            'reaction_time': reaction_time_ms,
            'correct': 'Correct' if is_correct else 'Incorrect'
        })

        # Update the score display
        self.update_score_display()

    def end_trial(self):
        self.trial_active = False

        # Store results for this block
        self.block_results.append({
            'block': self.current_block + 1,  # Use 1-based index for blocks
            'correct': self.correct_score,
            'incorrect': self.incorrect_score,
            'total_score': self.total_score
        })

        pygame.mixer.stop()

        # Display a customized message for each block
        if self.current_block in [0, 1]:
            self.message_label.config(text=f"Block {self.current_block + 1} Complete!")
        else:
            if self.current_block == 2:
                self.message_label.config(text="Block 3 Complete! Keep going!")
            elif self.current_block == 3:
                self.message_label.config(text="Block 4 Complete! Almost there!")
            elif self.current_block == 4:
                self.message_label.config(text="Block 5 Complete! Final stretch!")
            elif self.current_block == 5:
                self.message_label.config(text="Block 6 Complete! You're almost done!")
            elif self.current_block == 6:
                self.message_label.config(text="Block 7 Complete! Well done!")
            elif self.current_block == 7:
                self.message_label.config(text="All Blocks Complete! Click 'Download Final PDF' to save the report.")

        if self.current_block < len(self.blocks) - 1:
            self.root.after(3000, self.start_next_block)  # 3 seconds rest before next block
        else:
            # All blocks complete, generate the final PDF
            self.message_label.config(text=f"Trial Block Complete!")
            self.generate_pdf()

            # Create and display the "Download Final PDF" button
            if self.download_button is None:
                self.download_button = tk.Button(self.root, text="Download Final PDF", command=self.generate_pdf)
                self.download_button.pack(pady=20)  # Ensure the button is visible
            else:
                self.download_button.pack(pady=20)  # Ensure the button is visible

            self.message_label.config(text="All Blocks Complete! Click 'Download Final PDF' to save the report.")
            self.start_trial_button.config(state=tk.NORMAL)
            self.footer_label.pack(side=tk.BOTTOM, pady=50)

            # Enable the restart button after completing all blocks
            self.restart_trial_button.config(state=tk.NORMAL)

        self.root.unbind("<KeyPress>")

    def start_next_block(self):
        self.current_block += 1
        self.start_trial()  # Start the next block

    def draw_green_tick(self):
        self.right_canvas.delete("all")  # Clear the canvas
        # Load the image
        try:
            image = Image.open("./correct.jpg")
            image = image.resize((200, 200))  # Resize image if necessary
            self.image_tk = ImageTk.PhotoImage(image)  # Convert image to PhotoImage

            # Display the image on the canvas
            self.right_canvas.create_image(200, 200, image=self.image_tk)  # Adjust coordinates as needed
        except Exception as e:
            print(f"Error loading image: {e}")

        
    def draw_red_cross(self):
        self.right_canvas.delete("all")  # Clear the canvas
        # Load the image
        try:
            image = Image.open("./wrong.png")
            image = image.resize((200, 200))  # Resize image if necessary
            self.image_tk = ImageTk.PhotoImage(image)  # Convert image to PhotoImage

            # Display the image on the canvas
            self.right_canvas.create_image(200, 200, image=self.image_tk)  # Adjust coordinates as needed
        except Exception as e:
            print(f"Error loading image: {e}")
    
    def clear_right_canvas(self):
        self.right_canvas.delete("all")

    def generate_pdf(self):
        filename = "final_report.pdf"

        # Create PDF
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter  # Get the dimensions of the page
        margin = 50
        y_position = height - margin  # Start from the top of the page

        # Draw the title
        c.drawString(margin, y_position, "Final Report")
        y_position -= 20

        current_block = None  # Track the current block number
        block_total_score = 0  # Track the total score for the current block

        # Draw the results
        for result in self.block_results:
            # Check if a new page is needed
            if y_position < margin + 40:
                c.showPage()  # Create a new page
                y_position = height - margin  # Reset y_position to top of the new page

            block_number = result.get('block')
            trial_number = result.get('trial', 'N/A')
            reaction_time = result.get('reaction_time', 'N/A')
            correctness = result.get('correct', 'N/A')
            total_score = result.get('total_score', 0)

            if block_number != current_block:
                # Print the block's total score at the end of the block
                if current_block is not None:
                    c.drawString(margin, y_position, f"Block {current_block} Total Score: {block_total_score}")
                    y_position -= 20

                # Start a new block
                c.drawString(margin, y_position, f"Block {block_number}:")
                y_position -= 20
                block_total_score = 0  # Reset block total score for new block

            # Print individual results
            if trial_number == 'Last':
                c.drawString(margin, y_position, f"Final Trial - Reaction Time: {reaction_time} ms: {correctness} entry")
            else:
                c.drawString(margin, y_position, f"Trial {trial_number} - Reaction Time: {reaction_time} ms: {correctness} entry")
            y_position -= 20

            # Update block total score
            block_total_score += total_score
            current_block = block_number

        # Print the total score for the last block
        if current_block is not None:
            c.drawString(margin, y_position, f"Block {current_block} Total Score: {block_total_score}")
            y_position -= 20

        c.save()  # Save the PDF file

   
    def restart_trial(self):
        # Reset variables
        self.current_block = 0
        self.current_position = 0
        self.user_inputs = []
        self.correct_score = 0
        self.incorrect_score = 0
        self.total_score = 0
        self.block_results.clear()
        
        # Update UI elements
        self.heading_label.config(text="")
        self.message_label.config(text="")
        self.canvas.delete("all")  # Clear main canvas
        self.left_canvas.delete("all")  # Clear left canvas
        self.right_canvas.delete("all")  # Clear right canvas
        
        if self.download_button is not None:
            self.download_button.pack_forget()  # Hide the download button
        
        self.start_trial_button.config(state=tk.NORMAL)  # Enable Start Trial button
        self.restart_trial_button.config(state=tk.DISABLED)  # Disable Restart Trial button
        
        self.footer_label.pack(side=tk.BOTTOM, pady=50)  # Show footer label

        # Start the first trial block
        self.start_trial()


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SerialReactionTimeTask(root)
    root.mainloop()
