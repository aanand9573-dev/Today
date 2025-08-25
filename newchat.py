import tkinter as tk
from tkinter import messagebox
import random
import datetime

class FreightNegotiationChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Freight Negotiation Chatbot 💬")
        
        self.root.geometry("750x650")
        self.root.configure(bg="#dbeafe")

        self.party_name = None
        self.weight = None
        self.cost = None
        self.original_cost = None
        self.min_price = None
        self.chat_log = []
        self.negotiation_rounds = 0

        # Heading
        heading_frame = tk.Frame(root, bg="#1E3A8A", height=60)
        heading_frame.pack(fill=tk.X)

        heading_label = tk.Label(
            heading_frame,
            text="🚚 Freight Price Negotiation Chatbot 🤖",
            font=("Arial", 17, "bold"),
            bg="#1E3A8A",
            fg="white",
            pady=12
        )
        heading_label.pack()

        # Chat area
        self.chat_area = tk.Canvas(root, bg="#f1f5f9", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(root, command=self.chat_area.yview)
        self.scrollable_frame = tk.Frame(self.chat_area, bg="#f1f5f9")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.chat_area.configure(scrollregion=self.chat_area.bbox("all"))
        )

        self.chat_area.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.chat_area.configure(yscrollcommand=self.scrollbar.set)

        self.chat_area.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        self.scrollbar.pack(side="right", fill="y")

        # Input + Buttons area (BOTTOM)
        self.entry_frame = tk.Frame(root, bg="#dbeafe")
        self.entry_frame.pack(side="bottom", fill=tk.X, padx=10, pady=5)

        self.entry = tk.Entry(self.entry_frame, font=("Arial", 13), bg="#f0f9ff", relief="flat")
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, ipady=7)
        self.entry.bind("<Return>", self.process_message)

        # Rounded Send button
        self.send_btn = tk.Button(
            self.entry_frame,
            text="Send ➡️",
            command=lambda: self.process_message(None),
            font=("Arial", 12, "bold"),
            bg="#2563EB",
            fg="white",
            relief="flat",
            bd=0
        )
        self.send_btn.pack(side=tk.LEFT, padx=5, ipadx=15, ipady=6)
        self.send_btn.config(highlightthickness=0)

        # Rounded Accept button
        self.accept_btn = tk.Button(
            self.entry_frame,
            text="Accept ✅",
            command=self.accept_offer,
            font=("Arial", 12, "bold"),
            bg="#22C55E",
            fg="white",
            relief="flat",
            bd=0
        )
        self.accept_btn.pack(side=tk.LEFT, padx=5, ipadx=15, ipady=6)
        self.accept_btn.config(highlightthickness=0)

        # Negotiation states
        self.state = "ASK_NAME"

        # Response banks
        self.adjust_responses = [
            "🤝 We cannot go that low, but let’s compromise a little.",
            "📉 That’s a tough cut, but here’s a small reduction.",
            "🙂 We’ve adjusted slightly to keep it fair.",
            "🙌 Not that low, but I can reduce a bit more.",
            "💡 Here’s a revised offer, but not much lower.",
            "🔄 I’ve reconsidered and can move just a little further.",
            "⏳ Let’s not drag this out, here’s my improved price.",
            "🧐 I see your point, I’ll reduce slightly again.",
            "🤔 I can stretch a little, but not too much.",
            "👍 Fine, I’ll lower it just a tiny bit more for you."
        ]

        self.accept_responses = [
            "✅ That’s fair enough! We’ll accept your offer.",
            "🎉 Deal finalized! Thank you for being reasonable.",
            "👍 Perfect, we agree at this price.",
            "🙌 Congratulations, deal closed at your offer.",
            "👏 Excellent, this works for us!"
        ]

        # Start conversation
        self.bot_message("👋 Hello! Welcome to the Freight Negotiation System.\nPlease tell me your Party Name:")

    def add_message(self, sender, text, bg_color, fg_color, side):
        frame = tk.Frame(self.scrollable_frame, bg="#f1f5f9")
        bubble = tk.Label(
            frame,
            text=text,
            bg=bg_color,
            fg=fg_color,
            wraplength=480,
            justify="left",
            font=("Arial", 11),
            padx=12,
            pady=8,
            relief="flat",
            bd=0
        )
        bubble.pack(anchor=side, pady=4, padx=10)
        bubble.configure(borderwidth=0, highlightthickness=0)
        bubble.config(relief="solid")
        bubble.config(borderwidth=0, highlightbackground=bg_color)

        # Rounded corners trick
        bubble.config(relief="solid")
        bubble.config(bd=0)
        bubble.config(highlightthickness=0)

        frame.pack(anchor=side, fill="x")
        self.chat_area.update_idletasks()
        self.chat_area.yview_moveto(1.0)
        self.chat_log.append(f"{sender}: {text}")

    def bot_message(self, text):
        self.add_message("Bot", text, bg_color="#2563EB", fg_color="white", side="w")

    def user_message(self, text):
        self.add_message("You", text, bg_color="#22C55E", fg_color="white", side="e")

    def process_message(self, event):
        user_input = self.entry.get().strip()
        if not user_input:
            return
        self.user_message(user_input)  # always show user reply
        self.entry.delete(0, tk.END)

        if self.state == "ASK_NAME":
            self.party_name = user_input
            self.state = "ASK_WEIGHT"
            self.bot_message(f"Nice to meet you, {self.party_name}! 🚚 Please enter the weight of the commodity (in kg).")

        elif self.state == "ASK_WEIGHT":
            try:
                self.weight = int(user_input)
                packets = self.weight // 10
                if self.weight % 10 != 0:
                    packets += 1
                self.cost = packets * random.randint(50, 150)
                self.original_cost = self.cost
                self.min_price = 0.93 * self.original_cost  # floor price = 93%
                self.state = "NEGOTIATION"
                self.bot_message(f"💰 The offered freight price is ₹{self.cost}.\nClick Accept ✅ or enter your counter-offer below.")
            except ValueError:
                self.bot_message("⚠️ Please enter a valid number for weight.")

        elif self.state == "NEGOTIATION":
            try:
                new_price = float(user_input.replace("₹", "").strip())
                self.negotiation_rounds += 1

                if new_price < self.min_price:
                    if self.cost > self.min_price:
                        reduction = 0.005 * self.original_cost
                        proposed = max(self.cost - reduction, self.min_price)
                        response = random.choice(self.adjust_responses)
                        self.bot_message(f"{response}\n👉 Our revised offer is ₹{proposed:.2f}. Do you accept?")
                        self.cost = proposed
                    else:
                        self.bot_message("⚠️ We cannot reduce any further. This is our final offer.")
                
                elif self.min_price <= new_price <= self.original_cost:
                    response = random.choice(self.accept_responses)
                    self.finalize_deal(new_price, extra=response)

                elif new_price > self.original_cost:
                    self.finalize_deal(new_price, extra="😃 Generous offer! Deal closed.")

            except ValueError:
                self.bot_message("⚠️ Please type a number for counter-offer or click Accept ✅.")

    def accept_offer(self):
        if self.state == "NEGOTIATION":
            self.user_message("Accept ✅")
            self.finalize_deal(self.cost)

    def finalize_deal(self, final_price, extra=""):
        msg = f"{extra}\n✅ Deal Finalized!\n\nParty: {self.party_name}\nWeight: {self.weight} kg\nFinal Price: ₹{final_price}"
        self.bot_message(msg)
        self.chat_log.append("DEAL CLOSED")
        self.save_log(final_price)
        messagebox.showinfo("Deal Closed", msg)
        self.state = "END"

    def save_log(self, final_price):
        filename = f"chat_log_{self.party_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"Party: {self.party_name}\nWeight: {self.weight} kg\nFinal Price: ₹{final_price}\n\nChat Log:\n")
            for line in self.chat_log:
                file.write(line + "\n")
        print(f"Negotiation saved in {filename}")


# Run app
root = tk.Tk()
app = FreightNegotiationChatbot(root)
root.mainloop()
