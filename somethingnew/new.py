import tkinter as tk
from PIL import Image, ImageTk
import cv2
import pyttsx3
import speech_recognition as sr

cap = None
camera_label = None

# Initialize the speech recognition and synthesis engines
r = sr.Recognizer()
engine = pyttsx3.init()

def toggle_mic():
    # Placeholder function for toggling microphone mute/unmute
    if mic_button.cget('text') == 'Mic':
        mic_button.config(text='Muted', image=muted_icon)
        mic_button.config(relief=tk.SUNKEN, bd=0)
    else:
        mic_button.config(text='Mic', image=mic_icon, bg='SystemButtonFace')
        mic_button.config(relief=tk.FLAT, bd=0)
    if input_box.winfo_ismapped():
        input_box.pack_forget()
    else:
        input_box.pack()

def toggle_sound():
    # Placeholder function for toggling sound on/off
    if sound_button.cget('text') == 'Sound':
        sound_button.config(text='Muted', image=muted_sound_icon)
        sound_button.config(relief=tk.SUNKEN, bd=0)
    else:
        sound_button.config(text='Sound', image=sound_icon,
                            bg='SystemButtonFace')
        sound_button.config(relief=tk.FLAT, bd=0)


def toggle_camera():
    # Placeholder function for toggling camera on/off
    if camera_button.cget('text') == 'Camera':
        camera_button.config(text='Off', image=off_camera_icon)
        camera_button.config(relief=tk.SUNKEN, bd=0)
        # Call function to display camera feed
        show_camera_feed()
    else:
        camera_button.config(
            text='Camera', image=camera_icon, bg='SystemButtonFace')
        camera_button.config(relief=tk.FLAT, bd=0)
        # Call function to stop displaying camera feed
        hide_camera_feed()


def show_camera_feed():
    global cap, camera_label
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        camera_window = tk.Toplevel(window)
        camera_window.title("Camera")
        camera_window.geometry("340x280")
        camera_label = tk.Label(camera_window)
        center_window(camera_window)
        camera_label.pack()
        update_camera_feed()
    else:
        debug_label.showerror("Error", "Failed to open camera.")


def hide_camera_feed():
    global cap, camera_label

    if cap is not None:
        cap.release()
        cap = None

    if camera_label is not None:
        camera_label.destroy()
        camera_label = None


def update_camera_feed():
    global cap, camera_label

    if cap is not None and camera_label is not None:
        ret, frame = cap.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            image = ImageTk.PhotoImage(image)
            camera_label.configure(image=image)
            camera_label.image = image

    camera_label.after(10, update_camera_feed)


def toggle_fullscreen():
    # Placeholder function for toggling full screen/half screen
    if fullscreen_button.cget('text') == 'Fullscreen':
        fullscreen_button.config(
            text='Half Screen', image=halfscreen_icon)
        fullscreen_button.config(relief=tk.SUNKEN, bd=0)
        window.attributes('-fullscreen', True)
        window.geometry(
            "{0}x{1}+0+0".format(int(window.winfo_screenwidth() / 2), window.winfo_screenheight()))
    else:
        fullscreen_button.config(
            text='Fullscreen', image=fullscreen_icon, bg='SystemButtonFace')
        fullscreen_button.config(relief=tk.FLAT, bd=0)
        window.attributes('-fullscreen', False)
        window.geometry("800x600")

def align_right(debug_window):
    debug_window.update_idletasks()
    width = debug_window.winfo_width()
    height = debug_window.winfo_height()
    x = debug_window.winfo_screenwidth() - width
    y = (debug_window.winfo_screenheight() // 2) - (height // 2)
    debug_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def toggle_debug_output():
    global debug_window, debug_label

    if debug_window is None:  # If debug window doesn't exist, create it
        debug_window = tk.Toplevel(window)
        debug_window.title("Debug Output")
        debug_window.geometry("250x600")
        # Position to the left of main window
        debug_label = tk.Label(debug_window, text="debug box", fg="green", font=(
            'Arial', 12), bd=1, relief=tk.SUNKEN)
        align_right(debug_window)
        debug_label.pack(fill=tk.BOTH, expand=True)
    else:  # If debug window exists, toggle its visibility
        if debug_window.winfo_ismapped():
            debug_window.withdraw()  # Hide the window
        else:
            debug_window.deiconify()  # Show the window


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def handle_voice_input():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        # Use the speech recognition engine to convert speech to text
        input_text = r.recognize_google(audio)
        input_box.insert(tk.END, input_text)
        process_user_input(input_text)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Error occurred while requesting results: {0}".format(e))


def process_user_input(input_text):
    response = "You said: " + input_text
    debug_label.config(text=response)  # Display user input in debug box

    if "what is your name" in input_text.lower():
        assistant_response = "My name is KIMI."
    elif "what is my name" in input_text.lower():
        assistant_response = "i sould know this your name is Rikesh dahal."
    else:
        assistant_response = "Sorry, I didn't understand that."

    debug_label.config(text=debug_label.cget("text") + "\nKIMI: " + assistant_response)  # Display assistant's response in debug box
    speak(assistant_response)



def speak(text):
    # Use the speech synthesis engine to speak the given text
    engine.say(text)
    engine.runAndWait()


# Create the main Tkinter window
window = tk.Tk()
window.title("KIMI the voice assistant❤️")
window.geometry("800x600")
debug_window = None
debug_label = None
center_window(window)
# Load and resize PNG icons
mic_image = Image.open('mic.png').resize((32, 32))
muted_image = Image.open('muted.png').resize((32, 32))
sound_image = Image.open('sound.png').resize((32, 32))
muted_sound_image = Image.open('muted_sound.png').resize((32, 32))
off_image = Image.open('off.png').resize((32, 32))
camera_image = Image.open('camera.png').resize((32, 32))
fullscreen_image = Image.open('fullscreen.png').resize((32, 32))
halfscreen_image = Image.open('halfscreen.png').resize((32, 32))
debug_image = Image.open('debug.png').resize((32, 32))
hide_image = Image.open('hide.png').resize((32, 32))

# Create PhotoImage objects for icons
mic_icon = ImageTk.PhotoImage(mic_image)
muted_icon = ImageTk.PhotoImage(muted_image)
sound_icon = ImageTk.PhotoImage(sound_image)
muted_sound_icon = ImageTk.PhotoImage(muted_sound_image)
off_camera_icon = ImageTk.PhotoImage(off_image)
camera_icon = ImageTk.PhotoImage(camera_image)
fullscreen_icon = ImageTk.PhotoImage(fullscreen_image)
halfscreen_icon = ImageTk.PhotoImage(halfscreen_image)
debug_icon = ImageTk.PhotoImage(debug_image)
hide_icon = ImageTk.PhotoImage(hide_image)

# Create buttons with initial icons
mic_button = tk.Button(window, text='Mic', image=mic_icon,
                       command=handle_voice_input, bd=0, relief=tk.FLAT)
sound_button = tk.Button(window, text='Sound', image=sound_icon,
                         command=toggle_sound, bd=0, relief=tk.FLAT)
camera_button = tk.Button(window, text='Camera', image=camera_icon,
                          command=toggle_camera, bd=0, relief=tk.FLAT)
fullscreen_button = tk.Button(window, text='Fullscreen', image=fullscreen_icon,
                              command=toggle_fullscreen, bd=0, relief=tk.FLAT)
debug_button = tk.Button(window, text='Debug', image=debug_icon,
                         command=toggle_debug_output, bd=0, relief=tk.FLAT)

# Configure the buttons to be circular
button_radius = 20
mic_button.config(width=2 * button_radius, height=2 *
                  button_radius, highlightthickness=0)
sound_button.config(width=2 * button_radius, height=2 *
                    button_radius, highlightthickness=0)
camera_button.config(width=2 * button_radius, height=2 *
                     button_radius, highlightthickness=0)
fullscreen_button.config(width=2 * button_radius,
                         height=2 * button_radius, highlightthickness=0)
debug_button.config(width=2 * button_radius, height=2 *
                    button_radius, highlightthickness=0)

# Add buttons to the window
camera_button.pack(side=tk.TOP, anchor='center', padx=10, pady=10)
fullscreen_button.pack(side=tk.TOP, anchor='w', padx=10, pady=100)
debug_button.pack(side=tk.TOP, anchor='e', padx=10, pady=10)
sound_button.pack(side=tk.TOP, anchor='sw', padx=10, pady=10)
mic_button.pack(side=tk.BOTTOM, anchor='center', padx=10, pady=10)

# Create the input box at the bottom center
input_box = tk.Entry(window, justify=tk.CENTER, font=('Arial', 12), bd=1)
input_box.pack(side="bottom")
input_box.pack_forget()  # Hide input box initially

# Initialize the speech recognition engine
r = sr.Recognizer()

# Initialize the speech synthesis engine
engine = pyttsx3.init()

# Start the Tkinter event loop
window.mainloop()
