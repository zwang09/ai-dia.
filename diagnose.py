import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import requests
import openai
import webbrowser

# Set your OpenAI API key
openai.api_key = "OPENAI API KEY GOES HERE"

# Google API Key (replace with your actual Google API Key)
GOOGLE_API_KEY = "GOOGLE PLACE API KEY GOES HERE"

def send_to_chatgpt(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant, you will answer every question, and you will keep things short."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=200,
            temperature=0.7
        )
        chatgpt_reply = response['choices'][0]['message']['content'].strip()
        return chatgpt_reply
    except Exception as e:
        return f"Error: {e}"


def chat_with_gpt():
    user_message = chat_entry.get("1.0", tk.END).strip()
    if user_message == "":
        messagebox.showwarning("Input Error", "Please enter a message.")
        return

    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"You: {user_message}\n")
    chatgpt_reply = send_to_chatgpt(user_message)
    chat_display.insert(tk.END, f"ChatGPT: {chatgpt_reply}\n\n")
    chat_display.config(state=tk.DISABLED)
    chat_entry.delete("1.0", tk.END)


def show_chatgpt_window():
    chat_window = tk.Toplevel(window)
    chat_window.title("Chat with ChatGPT (GPT-4)")
    chat_window.geometry("500x600")
    chat_window.configure(bg="#F0F4C3")

    global chat_display
    chat_display = scrolledtext.ScrolledText(
        chat_window, wrap=tk.WORD, state=tk.DISABLED, width=60, height=25,
        font=("Arial", 12), bg="#FFF8E1", fg="#1A237E"
    )
    chat_display.pack(pady=10)

    global chat_entry
    chat_entry = tk.Text(
        chat_window, wrap=tk.WORD, height=3, font=("Arial", 12),
        bg="#FFF3E0", fg="#1A237E"
    )
    chat_entry.pack(pady=10)

    btn_send = tk.Button(
        chat_window, text="Send", command=chat_with_gpt, font=("Arial", 12),
        bg="#FFCC80", fg="white", activebackground="#FFB74D",
        activeforeground="white"
    )
    btn_send.pack(pady=10)


class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, bg="#F0F4C3")
        scrollbar = tk.Scrollbar(
            self, orient="vertical", command=canvas.yview
        )
        self.scrollable_frame = tk.Frame(canvas, bg="#F0F4C3")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


def find_nearest_therapist():
    location = simpledialog.askstring(
        "Location", "Enter your city or zip code:"
    )
    if not location:
        messagebox.showerror("Error", "Location input is required.")
        return

    search_url = (
        f"https://maps.googleapis.com/maps/api/place/textsearch/json"
        f"?query=therapist+in+{location.replace(' ', '+')}"
        f"&key={GOOGLE_API_KEY}"
    )
    response = requests.get(search_url)
    results = response.json().get("results", [])

    if not results:
        messagebox.showinfo("No Results", "No therapists found in your area.")
        return

  
    therapist_window = tk.Toplevel(window)
    therapist_window.title("Nearby Therapists")

    scrollable_frame = ScrollableFrame(therapist_window)
    scrollable_frame.pack(fill="both", expand=True)

    label_title = tk.Label(
        scrollable_frame.scrollable_frame, text="Nearby Therapists",
        font=("Arial", 16)
    )
    label_title.pack(pady=10)

    for therapist in results:
        name = therapist['name']
        address = therapist['formatted_address']
        label = tk.Label(
            scrollable_frame.scrollable_frame,
            text=f"{name} - {address}", font=("Arial", 12)
        )
        label.pack(pady=5)

        # Add button to view on Google Maps
        btn_open_map = tk.Button(
            scrollable_frame.scrollable_frame, text="View on Map",
            command=lambda t=name: open_in_google_maps(t)
        )
        btn_open_map.pack(pady=5)


def open_in_google_maps(therapist_name):
    query = f"https://www.google.com/maps/search/?api=1&query={therapist_name.replace(' ', '+')}"
    webbrowser.open(query)


def start_minigame():
    game_window = tk.Toplevel(window)
    game_window.title("Ball Catch Game")
    game_window.geometry("500x600")
    canvas = tk.Canvas(game_window, width=400, height=500)
    canvas.pack()

    paddle = canvas.create_rectangle(160, 480, 240, 490, fill="blue")
    ball = canvas.create_oval(190, 10, 210, 30, fill="red")
    ball_speed_x, ball_speed_y = 3, 3

    def move_paddle(event):
        if event.keysym == "Left":
            canvas.move(paddle, -20, 0)
        elif event.keysym == "Right":
            canvas.move(paddle, 20, 0)

    def move_ball():
        nonlocal ball_speed_x, ball_speed_y
        canvas.move(ball, ball_speed_x, ball_speed_y)
        ball_pos, paddle_pos = canvas.coords(ball), canvas.coords(paddle)
        if ball_pos[0] <= 0 or ball_pos[2] >= 400:
            ball_speed_x = -ball_speed_x
        if ball_pos[1] <= 0 or (
            paddle_pos[0] < ball_pos[2] < paddle_pos[2] and
            paddle_pos[1] < ball_pos[3] < paddle_pos[3]
        ):
            ball_speed_y = -ball_speed_y
        if ball_pos[3] >= 500:
            canvas.delete(ball)
            canvas.create_text(
                200, 250, text="Game Over!", font=("Arial", 24), fill="red"
            )
        else:
            game_window.after(50, move_ball)

    game_window.bind("<Left>", move_paddle)
    game_window.bind("<Right>", move_paddle)
    move_ball()


def show_home_screen(username):
    for widget in window.winfo_children():
        widget.pack_forget()
        
  
    title_label = tk.Label(
        window, text="AI DIA.", font=("Arial", 20, "bold"),
        bg="#BBDEFB", fg="#0D47A1"
    )
    title_label.pack(pady=20)

    label_welcome = tk.Label(
        window, text=f"Welcome, {username}!", font=("Arial", 16),
        bg="#BBDEFB", fg="#0D47A1"
    )
    label_welcome.pack(pady=20)

    button_frame = tk.Frame(window)
    button_frame.pack(pady=20)

    btn_therapist = tk.Button(
        button_frame, text="Find Nearest Therapist",
        command=find_nearest_therapist, font=("Arial", 12),
        bg="#FFEB3B", fg="#0D47A1"
    )
    btn_therapist.grid(row=0, column=0, padx=10, pady=10)

    btn_chatgpt = tk.Button(
        button_frame, text="Chat with ChatGPT",
        command=show_chatgpt_window, font=("Arial", 12),
        bg="#FFCCBC", fg="#1B5E20"
    )
    btn_chatgpt.grid(row=0, column=1, padx=10, pady=10)

    btn_minigame = tk.Button(
        button_frame, text="Start Focus Minigame",
        command=start_minigame, font=("Arial", 12),
        bg="#FFEB3B", fg="#0D47A1"
    )
    btn_minigame.grid(row=1, column=0, padx=10, pady=10)

   
    label_dropdown = tk.Label(
        button_frame, text="Mental Health Diagnosis Tests:",
        font=("Arial", 12), bg="#BBDEFB", fg="#0D47A1"
    )
    label_dropdown.grid(row=2, column=0, padx=10, pady=10, sticky="e")

    test_options = ["ADHD Test", "Anxiety Test", "Depression Test", "PTSD Test"]
    selected_test = tk.StringVar()
    selected_test.set("Select Test")

    option_menu = tk.OptionMenu(
        button_frame, selected_test, *test_options
    )
    option_menu.config(font=("Arial", 12), bg="#F0F4C3", fg="#1A237E")
    option_menu.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    btn_start_test = tk.Button(
        button_frame, text="Start Test",
        command=lambda: start_selected_test(selected_test.get()),
        font=("Arial", 12), bg="#FFCC80", fg="white"
    )
    btn_start_test.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    btn_logout = tk.Button(
        button_frame, text="Logout", command=show_registration_screen,
        font=("Arial", 12), bg="#EF9A9A", fg="white"
    )
    btn_logout.grid(row=4, column=0, columnspan=2, padx=10, pady=10)


def start_selected_test(test_name):
    if test_name == "ADHD Test":
        adhd_test()
    elif test_name == "Anxiety Test":
        anxiety_test()
    elif test_name == "Depression Test":
        depression_test()
    elif test_name == "PTSD Test":
        ptsd_test()
    else:
        messagebox.showwarning(
            "Selection Error", "Please select a test from the dropdown."
        )


def show_registration_screen():
    for widget in window.winfo_children():
        widget.pack_forget()

    label_name.pack(pady=10)
    entry_name.pack()
    label_email.pack(pady=10)
    entry_email.pack()
    label_password.pack(pady=10)
    entry_password.pack()
    btn_register.pack(pady=20)


def register_user():
    name, email, password = entry_name.get(), entry_email.get(), entry_password.get()
    if not (name and email and password):
        messagebox.showerror("Input Error", "All fields are required")
    else:
        messagebox.showinfo("Success", f"Registration successful for {name}")
        entry_name.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        show_home_screen(name)


def run_test(test_name, questions, options, point_values):
    for widget in window.winfo_children():
        widget.pack_forget()

    label_test = tk.Label(
        window, text=test_name, font=("Arial", 16),
        bg="#F0F4C3", fg="#1A237E"
    )
    label_test.pack(pady=10)

    scrollable_frame = ScrollableFrame(window)
    scrollable_frame.pack(fill="both", expand=True)

    user_answers = []

    def submit_answers():
        total_score = 0
        for answer_var in user_answers:
            total_score += point_values[answer_var.get()]

        result = interpret_score(test_name, total_score)
        messagebox.showinfo(f"{test_name} Result", result)
        show_home_screen("Player")

    for i, question in enumerate(questions):
        label_question = tk.Label(
            scrollable_frame.scrollable_frame, text=question,
            font=("Arial", 12), bg="#F0F4C3", fg="#1A237E"
        )
        label_question.pack(pady=10)

        answer_var = tk.IntVar()
        for j, option in enumerate(options):
            rb = tk.Radiobutton(
                scrollable_frame.scrollable_frame, text=option,
                variable=answer_var, value=j, bg="#F0F4C3", fg="#1A237E"
            )
            rb.pack(anchor="w")

        user_answers.append(answer_var)

    btn_submit = tk.Button(
        window, text="Submit Test", command=submit_answers,
        font=("Arial", 12), bg="#FFCC80", fg="white"
    )
    btn_submit.pack(pady=20)


def interpret_score(test_name, score):
    if test_name == "Depression Test":
        if score <= 10:
            return "Minimal symptoms of depression."
        elif score <= 20:
            return "Mild symptoms of depression."
        elif score <= 30:
            return "Moderate symptoms of depression."
        else:
            return "Severe symptoms of depression."
    elif test_name == "ADHD Test":
        if score <= 15:
            return "Minimal symptoms of ADHD."
        elif score <= 30:
            return "Mild symptoms of ADHD."
        elif score <= 45:
            return "Moderate symptoms of ADHD."
        else:
            return "Severe symptoms of ADHD."
    elif test_name == "PTSD Test":
        if score <= 10:
            return "Minimal symptoms of PTSD."
        elif score <= 20:
            return "Mild symptoms of PTSD."
        elif score <= 30:
            return "Moderate symptoms of PTSD."
        else:
            return "Severe symptoms of PTSD."
    elif test_name == "Anxiety Test":
        if score <= 10:
            return "Minimal symptoms of anxiety."
        elif score <= 20:
            return "Mild symptoms of anxiety."
        elif score <= 30:
            return "Moderate symptoms of anxiety."
        else:
            return "Severe symptoms of anxiety."


def depression_test():
    questions = [
        "Little interest or pleasure in doing things?",
        "Feeling down, depressed, or hopeless?",
        "Trouble sleeping or sleeping too much?",
        "Feeling tired or having little energy?",
        "Poor appetite or overeating?",
        "Feeling bad about yourself?",
        "Trouble concentrating on things?",
        "Moving or speaking so slowly or being fidgety?",
        "Thoughts of self-harm?",
        "Loss of interest in personal hygiene?",
        "Difficulty making decisions?",
        "Feelings of worthlessness?",
        "Social withdrawal or isolation?",
        "Inability to experience joy or happiness?",
        "Crying for no apparent reason?",
        "Feeling irritable?",
        "Feeling like you are a burden?",
        "Excessive guilt?",
        "Frequent mood swings?",
        "Difficulty managing everyday tasks?"
    ]
    options = ["Not at all", "Several days", "More than half the days", "Nearly every day"]
    point_values = [0, 1, 2, 3]
    run_test("Depression Test", questions, options, point_values)


def adhd_test():
    questions = [
        "Difficulty paying attention to details?",
        "Easily distracted?",
        "Difficulty staying focused?",
        "Failing to follow through on instructions?",
        "Difficulty organizing tasks?",
        "Avoiding tasks that require mental effort?",
        "Losing items necessary for tasks?",
        "Easily forgetful?",
        "Restlessness or fidgeting?",
        "Trouble sitting still?",
        "Difficulty remaining quiet?",
        "Interrupting others' conversations?",
        "Impulsiveness?",
        "Difficulty waiting your turn?",
        "Acting without thinking?",
        "Trouble controlling emotions?",
        "Excessive talking?",
        "Often feeling restless?",
        "Difficulty relaxing?",
        "Difficulty staying on track with conversations?"
    ]
    options = ["Never", "Rarely", "Sometimes", "Often", "Very Often"]
    point_values = [0, 1, 2, 3, 4]
    run_test("ADHD Test", questions, options, point_values)


def ptsd_test():
    questions = [
        "Recurrent unwanted memories of trauma?",
        "Avoiding reminders of trauma?",
        "Nightmares or flashbacks?",
        "Feeling distant or cut off from others?",
        "Feeling emotionally numb?",
        "Trouble remembering parts of the trauma?",
        "Exaggerated startle response?",
        "Irritability or angry outbursts?",
        "Hypervigilance?",
        "Difficulty concentrating?",
        "Feeling detached from reality?",
        "Difficulty maintaining relationships?",
        "Avoiding places that remind you of the trauma?",
        "Negative changes in mood or thoughts?",
        "Feeling hopeless about the future?",
        "Loss of interest in activities?",
        "Feeling on guard constantly?",
        "Trouble falling asleep?",
        "Feeling easily startled?",
        "Feelings of guilt or blame?"
    ]
    options = ["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"]
    point_values = [0, 1, 2, 3, 4]
    run_test("PTSD Test", questions, options, point_values)


def anxiety_test():
    questions = [
        "Feeling nervous, anxious, or on edge?",
        "Not being able to stop worrying?",
        "Worrying too much about different things?",
        "Trouble relaxing?",
        "Being so restless it’s hard to sit still?",
        "Easily irritated?",
        "Feeling afraid something awful might happen?",
        "Difficulty controlling anxious thoughts?",
        "Fear of social situations?",
        "Avoiding anxiety-inducing situations?",
        "Experiencing panic attacks?",
        "Difficulty concentrating due to worry?",
        "Feeling weak or tired from anxiety?",
        "Experiencing trembling or shaking?",
        "Feeling out of control?",
        "Sweating excessively?",
        "Shortness of breath?",
        "Rapid heartbeat?",
        "Nausea or stomach distress?",
        "Dizziness or lightheadedness?"
    ]
    options = ["Not at all", "Several days", "More than half the days", "Nearly every day"]
    point_values = [0, 1, 2, 3]
    run_test("Anxiety Test", questions, options, point_values)


window = tk.Tk()
window.title("AI DIA.")
window.geometry("400x600")
window.configure(bg="#E3F2FD")


label_name = tk.Label(
    window, text="Name:", font=("Arial", 12),
    bg="#E3F2FD", fg="#0D47A1"
)
entry_name = tk.Entry(window, width=30)

label_email = tk.Label(
    window, text="Email:", font=("Arial", 12),
    bg="#E3F2FD", fg="#0D47A1"
)
entry_email = tk.Entry(window, width=30)

label_password = tk.Label(
    window, text="Password:", font=("Arial", 12),
    bg="#E3F2FD", fg="#0D47A1"
)
entry_password = tk.Entry(window, width=30, show="*")


btn_register = tk.Button(
    window, text="Register", command=register_user,
    font=("Arial", 12), bg="#64B5F6", fg="white"
)


show_registration_screen()


window.mainloop()
