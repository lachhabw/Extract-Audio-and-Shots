import tkinter as tk
from tkinter import ttk, filedialog
from moviepy.editor import VideoFileClip
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import shutil
import threading
from tqdm import tqdm

class VideoProcessingApp:
    def __init__(self, master):
        self.master = master
        master.title("Extract Audio and Shots")
        self.source_folder_path = ""
        self.destination_folder_path = ""
        self.extract_audio_var = tk.BooleanVar()
        self.extract_shots_var = tk.BooleanVar()
        self.audio_format_var = tk.StringVar(value="mp3")
        self.image_format_var = tk.StringVar(value="jpg")
        self.num_workers_var = tk.IntVar(value=os.cpu_count())
        self.shots_per_minute_var = tk.IntVar(value=1)
        self.create_widgets()

    def create_widgets(self):
        self.master.geometry("800x600")  # Set initial size
        self.master.grid_rowconfigure(6, weight=1)
        # Configure grid column weights for centering
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(3, weight=1)

        # Source Folder
        self.source_label = tk.Label(self.master, text="Source Folder:")
        self.source_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.source_folder_entry = tk.Entry(self.master, width=40)
        self.source_folder_entry.grid(row=0, column=1, columnspan=2, pady=10, sticky="we")

        self.source_folder_button = tk.Button(self.master, text="Browse", command=self.select_source_folder)
        self.source_folder_button.grid(row=0, column=3, padx=10, pady=10, sticky="w")

        # Destination Folder
        self.destination_label = tk.Label(self.master, text="Destination Folder:")
        self.destination_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.destination_folder_entry = tk.Entry(self.master, width=40)
        self.destination_folder_entry.grid(row=1, column=1, columnspan=2, pady=10, sticky="we")

        self.destination_folder_button = tk.Button(self.master, text="Browse", command=self.select_destination_folder)
        self.destination_folder_button.grid(row=1, column=3, padx=10, pady=10, sticky="w")
        
        # Extraction Options
        self.extract_audio_checkbox = tk.Checkbutton(self.master, text="Extract Audio", variable=self.extract_audio_var)
        self.extract_audio_checkbox.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.extract_shots_checkbox = tk.Checkbutton(self.master, text="Extract Shots", variable=self.extract_shots_var)
        self.extract_shots_checkbox.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Format Options
        self.audio_format_label = tk.Label(self.master, text="Audio Format:")
        self.audio_format_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        self.audio_format_entry = tk.Entry(self.master, textvariable=self.audio_format_var, width=10)
        self.audio_format_entry.grid(row=3, column=1, pady=10, sticky="w")

        self.image_format_label = tk.Label(self.master, text="Image Format:")
        self.image_format_label.grid(row=3, column=2, padx=10, pady=10, sticky="e")

        self.image_format_entry = tk.Entry(self.master, textvariable=self.image_format_var, width=10)
        self.image_format_entry.grid(row=3, column=3, pady=10, sticky="w")

        # Workers and Shots Per Minute Options
        self.num_workers_label = tk.Label(self.master, text="Number of Workers:")
        self.num_workers_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")

        self.num_workers_entry = tk.Entry(self.master, textvariable=self.num_workers_var, width=5)
        self.num_workers_entry.grid(row=4, column=1, pady=10, sticky="w")

        self.shots_per_minute_label = tk.Label(self.master, text="Shots Per Minute:")
        self.shots_per_minute_label.grid(row=4, column=2, padx=10, pady=10, sticky="e")

        self.shots_per_minute_entry = tk.Entry(self.master, textvariable=self.shots_per_minute_var, width=5)
        self.shots_per_minute_entry.grid(row=4, column=3, pady=10, sticky="w")

        # Process Button
        self.process_button = tk.Button(self.master, text="Run Video Processing", command=self.run_video_processing_thread)
        self.process_button.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

        # Debug Text
        self.debug_text = tk.Text(self.master, wrap=tk.WORD, bg="black", fg="white", font=("Consolas", 10))
        self.debug_text.grid(row=6, column=0, columnspan=4, pady=10, sticky="nsew")

        # Configure tags for styling
        self.debug_text.tag_configure("success_message", foreground="green")
        self.debug_text.tag_configure("error_message", foreground="red")
        self.debug_text.tag_configure("finish_message", foreground="#00FFFF")

        # Make the debug text read-only and scrollable
        self.debug_text.config(state=tk.DISABLED)
        scrollbar = tk.Scrollbar(self.master, command=self.debug_text.yview)
        scrollbar.grid(row=6, column=4, sticky="nsew")
        self.debug_text.config(yscrollcommand=scrollbar.set)

    def select_source_folder(self):
        folder_path = filedialog.askdirectory()
        self.source_folder_entry.delete(0, tk.END)
        self.source_folder_entry.insert(0, folder_path)
        self.source_folder_path = folder_path

    def select_destination_folder(self):
        folder_path = filedialog.askdirectory()
        self.destination_folder_entry.delete(0, tk.END)
        self.destination_folder_entry.insert(0, folder_path)
        self.destination_folder_path = folder_path

    def process_single_video(self, video_name, source_folder_path, save_folder_path, extract_audio, extract_shots, shots_per_minute, extension_audio, extension_img):

        try: 
            # Load the video clip
            video_path = source_folder_path+"/"+video_name
            video_clip = VideoFileClip(video_path)

            # Create video save directory
            video_save_path = save_folder_path+"/"+video_name
            shutil.rmtree(video_save_path, ignore_errors=True)
            os.mkdir(video_save_path)

            # Extract audio
            if extract_audio:
                audio_path = f"{video_save_path}/{video_name}.{extension_audio.lower()}"
                video_clip.audio.write_audiofile(audio_path, codec=extension_audio.lower())

            # Extract shots
            if extract_shots:
                # Create shots save directory
                shots_save_path = video_save_path+"/"+"shots"
                os.mkdir(shots_save_path)
                # Calculate the time duration of each shot
                total_duration = video_clip.duration
                shot_per_sec = shots_per_minute*60
                n_shots = int(total_duration / shot_per_sec)+1
                # Save the shots
                for i in tqdm(range(n_shots), desc="Shots Extraction", unit="shot"):
                    video_clip.save_frame(f"{shots_save_path}/img {i}.{extension_img.lower()}", t=i*shot_per_sec)
                
            video_clip.close()
            # report name and status
            return video_name, True

        except Exception as e:
            return video_name, False
        
    def run_video_processing_thread(self):
        # Disable the RUN button
        self.process_button.config(state=tk.DISABLED)
        # Start a new thread for the processing
        new_thread = threading.Thread(target=self.run_video_processing)
        new_thread.start()

    def run_video_processing(self):
        # Get the working mode
        extract_audio = self.extract_audio_var.get()
        extract_shots = self.extract_shots_var.get()
        if not extract_audio and not extract_shots:
            self.debug_text.config(state=tk.NORMAL)
            self.debug_text.insert(tk.END, "Please select at least one extraction mode.\n", "error_message")
            self.debug_text.config(state=tk.DISABLED)
            self.process_button.config(state=tk.NORMAL)
            return 
        # Get parameters
        extension_audio = self.audio_format_var.get()
        extension_img = self.image_format_var.get()
        # Get folders paths
        source_folder_path = self.source_folder_entry.get()
        destination_folder_path = self.destination_folder_entry.get()
        progress_bar = None

        if not source_folder_path or not destination_folder_path:
            self.debug_text.config(state=tk.NORMAL)
            self.debug_text.insert(tk.END, "Please select both source and destination folders.\n", "error_message")
            self.debug_text.config(state=tk.DISABLED)
            self.process_button.config(state=tk.NORMAL)
            return
        
        try:
            # Multi-threading
            max_workers = self.num_workers_var.get()
            shots_per_minute = self.shots_per_minute_var.get()
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Check the existence of folders
                os.listdir(destination_folder_path)
                files = os.listdir(source_folder_path)
                n_files = len(files)
                # Set up progress bar
                progress_var = tk.DoubleVar(value=0)
                progress_bar = ttk.Progressbar(self.master, variable=progress_var, mode="determinate", maximum=100)
                progress_bar.grid(row=7, column=0, columnspan=4, padx=2, pady=5, sticky="nsew")
            
                # Start video processing
                futures = [
                    executor.submit(
                        lambda video_name: self.process_single_video(video_name, source_folder_path, destination_folder_path, extract_audio, extract_shots, shots_per_minute, extension_audio, extension_img),
                        file
                    ) for file in files
                ]

                for i, future in enumerate(as_completed(futures)):
                    name, status = future.result()
                    if not status:
                        self.debug_text.config(state=tk.NORMAL)
                        self.debug_text.insert(tk.END, "- Failure: ", "error_message")
                        self.debug_text.insert(tk.END, f"Unable to process the video '{name}'. Check if the video is valid, with a supported format (mp4, mkv, ts, are recommended). Check if the image format is valid (jpeg, jpg, png are recommended). Check if the audio format is valid (mp3, wav, aac are recommended).\n")
                        self.debug_text.config(state=tk.DISABLED)
                    else:
                        self.debug_text.config(state=tk.NORMAL)
                        self.debug_text.insert(tk.END, f"- Success: ", "success_message")
                        self.debug_text.insert(tk.END, f"Video '{name}' has been processed.\n")
                        self.debug_text.config(state=tk.DISABLED)

                    # Update progress bar
                    progress_value = (i + 1) / n_files * 100
                    progress_var.set(progress_value)
                    self.master.update_idletasks()

                # Add a green message indicating the process has finished
                self.debug_text.config(state=tk.NORMAL)
                self.debug_text.insert(tk.END, "Processing has finished.\n", "finish_message")
                self.debug_text.config(state=tk.DISABLED)

        except Exception as e:
            self.debug_text.config(state=tk.NORMAL)
            self.debug_text.insert(tk.END, f"Error: {e}\n", "error_message")
            self.debug_text.config(state=tk.DISABLED)

        finally:
            # Enable the process button after the process finishes
            self.process_button.config(state=tk.NORMAL)
            # Destroy progress bar if it exists
            if progress_bar:
                progress_bar.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoProcessingApp(root)
    root.mainloop()
