from flask import Flask, request, redirect
from datetime import datetime

app = Flask(__name__)

notes = []

@app.route("/", methods=["GET", "POST"])
def home():
    global notes

    if request.method == "POST":
        if "delete" in request.form:
            index = int(request.form.get("delete"))
            if 0 <= index < len(notes):
                notes.pop(index)
            return redirect("/")

        note_text = request.form.get("note")
        if note_text:
            notes.append({
                "text": note_text,
                "time": datetime.now().strftime("%d %b %Y - %H:%M")
            })
        return redirect("/")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Smart Cloud Notes</title>
        <style>
            body {{
                font-family: Arial;
                margin: 0;
                background: #121212;
                color: white;
                transition: 0.3s;
            }}

            .light {{
                background: #f4f4f4;
                color: black;
            }}

            .container {{
                width: 85%;
                margin: 30px auto;
            }}

            h1 {{
                text-align: center;
            }}

            .top-bar {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }}

            input[type=text] {{
                padding: 10px;
                width: 60%;
                border-radius: 6px;
                border: none;
            }}

            button {{
                padding: 8px 14px;
                border-radius: 6px;
                border: none;
                cursor: pointer;
                font-weight: bold;
            }}

            .add-btn {{
                background: #00c896;
                color: white;
            }}

            .delete-btn {{
                background: #ff4d4d;
                color: white;
                font-size: 12px;
                padding: 4px 8px;
            }}

            .note-card {{
                background: rgba(255,255,255,0.1);
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 12px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                animation: fadeIn 0.5s ease;
            }}

            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}

            .time {{
                font-size: 11px;
                opacity: 0.7;
            }}

            .stats {{
                margin-bottom: 10px;
                font-size: 14px;
            }}

        </style>
    </head>
    <body>

        <div class="container">
            <h1> Smart Cloud TO DO  Dashboard</h1>

            <div class="top-bar">
                <div class="stats">
                    Total Task: <strong>{len(notes)}</strong>
                </div>
                <button onclick="toggleMode()">🌗 Toggle Mode</button>
            </div>

            <form method="POST">
                <input type="text" name="note" id="noteInput"
                       placeholder="Write something amazing..."
                       maxlength="100" required
                       oninput="countChars()">
                <button class="add-btn" type="submit">Add</button>
            </form>

            <div style="margin:8px 0;">
                Characters: <span id="charCount">0</span>/100
            </div>

            <input type="text" id="search"
                   placeholder="🔍 Search notes..."
                   onkeyup="searchNotes()"
                   style="width:100%; padding:8px; border-radius:6px; margin-bottom:15px;">

    """

    for i, note in enumerate(reversed(notes)):
        real_index = len(notes) - 1 - i
        html += f"""
            <div class="note-card">
                <div>
                    {note['text']}
                    <div class="time">{note['time']}</div>
                </div>
                <form method="POST" style="margin:0;">
                    <button class="delete-btn" name="delete" value="{real_index}">Delete</button>
                </form>
            </div>
        """

    html += """
        </div>

        <script>
            function countChars() {
                let input = document.getElementById("noteInput");
                document.getElementById("charCount").innerText = input.value.length;
            }

            function toggleMode() {
                document.body.classList.toggle("light");
            }

            function searchNotes() {
                let input = document.getElementById("search").value.toLowerCase();
                let cards = document.getElementsByClassName("note-card");
                for (let i = 0; i < cards.length; i++) {
                    let text = cards[i].innerText.toLowerCase();
                    cards[i].style.display = text.includes(input) ? "flex" : "none";
                }
            }
        </script>

    </body>
    </html>
    """

    return html


if __name__ == "__main__":
    app.run(debug=True)
