from random_text import news_dict
import random
from tkinter import *
from tkinter import messagebox
import math

TIMER_START = 60
BACKGROUND_COLOR = "#a8d5ba"
timer_running = False
time_left = TIMER_START
has_started_typing = False
countdown_job = None

typing_list = [" "]
text_list = []

position = 0
start_index = "1.0"
end_index = ""

word_counts = 0
correct_counts = 0
incorrect_counts = 0

def start_type():
      global random_story, time_left, has_started_typing,start_index, \
          timer_running, countdown_job, typing_list,text_list, position, word_counts, correct_counts, incorrect_counts

      has_started_typing = False
      timer_running = False
      time_left = TIMER_START

      typing_list = []
      text_list = []

      start_index = "1.0"
      position = 0
      word_counts = 0
      correct_counts = 0
      incorrect_counts = 0

      if countdown_job is not None:
          # Cancels the job that would have run count_down(XX seconds)
          timer_canvas.after_cancel(countdown_job)
          countdown_job = None

      random_key = random.choice(list(news_dict.keys()))
      random_story = news_dict[random_key]

      # Clear the Text widget
      news_text.delete("1.0", END)
      news_text.insert(END, random_story)

      news_text.config(state="disabled")


      text_list = random_story.split(" ")

      text_entry.delete(0, END)
      text_entry.focus()
      show_timer(time_left)

      start_button.pack_forget()
      landing_message.pack_forget()
      news_frame.pack(anchor="w", fill=X, padx=50, pady=20)
      typing_frame.pack(anchor="w", fill=X, padx=50, pady=(0, 20))
      timer_frame.pack(anchor="w", fill=X, padx=50, pady=(0, 20))
      highlight_before_typing()

      news_text.tag_remove("correct", "1.0", END)
      news_text.tag_remove("incorrect", "1.0", END)

def highlight_before_typing():
    global start_index, end_index
    words = news_text.get("1.0", END).split()

    news_text.tag_remove("highlight", "1.0", END)

    news_text.tag_configure("highlight", background="yellow")
    first_word = words[0]
    end_index = f"{start_index}+{len(first_word)}c"
    news_text.tag_add("highlight", start_index, end_index)


def restart():
    start_type()


def show_timer(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec == 0:
        count_sec = "00"
    elif count_sec < 10:
        count_sec = "0" + str(count_sec)

    timer_canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

def count_down(count):
    global timer_running, countdown_job, word_counts, correct_counts, incorrect_counts
    show_timer(count)
    if count > 0:
        countdown_job = timer_canvas.after(1000, count_down, count - 1)
        # After 1s, call the function count_down() with the argument count - 1.
        # It returns a string ID (like "after#123456") that uniquely identifies this scheduled task.
    else:
        timer_running = False
        countdown_job = None
        messagebox.showinfo("Time's Up!",
                            f"WPM: {word_counts}\n"
                            f"Incorrect words: {incorrect_counts}\n"
                            f"Correct words: {correct_counts}\n")

        news_text.config(state="normal")


def start_countdown(event):
    global timer_running, has_started_typing

    # Only start if a real printable key is pressed (ignores Shift, Ctrl, etc.)
    if event.char.isprintable():
        if not has_started_typing and text_entry.get().strip():
            has_started_typing = True

        if has_started_typing and not timer_running:
            timer_running = True
            count_down(time_left)


def typing_words(event):
    global position, typing_list, text_list, word_counts
    if event.keysym in ["space", "Return"]:
        word = text_entry.get()
        typing_list.append(word)
        check_correct()
        position += 1
        word_counts += 1

        text_entry.delete(0, END)
        highlight_after_typing()


def highlight_after_typing():
    global position, start_index, end_index, typing_list, text_list
    words = news_text.get("1.0", END).split()

    news_text.tag_remove("highlight", "1.0", END)

    news_text.tag_configure("highlight", background="yellow")

    current_word = words[position]
    start_index = f"{end_index}+{1}c"
    end_index = f"{start_index}+{len(current_word)}c"
    news_text.tag_add("highlight", start_index, end_index)


def check_correct():
    global position, typing_list, text_list, start_index, end_index, correct_counts, incorrect_counts
    news_text.tag_configure("correct", foreground="blue")
    news_text.tag_configure("incorrect", foreground="red")

    if position < len(typing_list) and position < len(text_list):
        if typing_list[position].strip() == text_list[position]:
            correct_counts += 1
            news_text.tag_add("correct", start_index, end_index)
        else:
            incorrect_counts += 1
            news_text.tag_add("incorrect", start_index, end_index)


window = Tk()
window.title("Typing Speed Test")
window.geometry("900x800")

landing_frame = Frame(window, bg=BACKGROUND_COLOR)
landing_frame.pack(fill=BOTH, expand=True)

landing_message = Label(landing_frame, text="Test your typing speed!", bg=BACKGROUND_COLOR, font=("Arial", 30, "bold"))
landing_message.pack(side=TOP, fill=Y, padx=50, pady=100)

start_button = Button(landing_frame, text="Start", highlightthickness=0, font=("Arial", 16), command=start_type)
start_button.pack(side=TOP, fill=Y, padx=50, pady=50)

news_frame = Frame(landing_frame, height=500, width=800, bg="#fcfcf4")
news_frame.grid_propagate(False)

news_text = Text(news_frame, wrap=WORD, font=("Avenir", 20, "bold"), bg="#fcfcf4", bd=0, highlightthickness=0, height=14)
news_text.pack(fill=BOTH, expand=True, padx=5, pady=10)


typing_frame = Frame(landing_frame, bg=BACKGROUND_COLOR)

text_label = Label(typing_frame, text="Type the words here:", bg=BACKGROUND_COLOR, font=("Arial", 15, "bold"))
text_label.grid(row=1, column=0, sticky=W, pady=10, padx=(0, 10))

text_entry = Entry(typing_frame, width=25, bg="white", fg="black", font=("Arial", 14), bd=2)
text_entry.focus()
text_entry.grid(row=1, column=1, sticky=W, pady=10)

timer_frame = Frame(landing_frame, bg=BACKGROUND_COLOR)

time_label = Label(timer_frame, text="Time left:", bg=BACKGROUND_COLOR, font=("Arial", 15, "bold"))
time_label.grid(row=0, column=0, sticky=W, pady=10)

timer_canvas = Canvas(timer_frame, bg=BACKGROUND_COLOR, width=200, height=25, highlightthickness=0)
timer_canvas.grid(row=0, column=1, sticky=W, pady=10)

timer_text = timer_canvas.create_text(30, 13, text="", fill="black", font=("Arial", 15, "bold"))

restart_button = Button(timer_frame, text="Restart",highlightthickness=0, font=("Arial",16),command=restart)
restart_button.grid(row=1, column=0, sticky=W, pady=10)


text_entry.bind("<KeyRelease>", start_countdown)
text_entry.bind("<KeyRelease-space>", typing_words)
text_entry.bind("<KeyRelease-Return>", typing_words)

window.mainloop()