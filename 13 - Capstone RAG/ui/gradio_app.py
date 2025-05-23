import base64
import os

from src import get_answer

import gradio as gr

current_script_dir = os.path.dirname(os.path.abspath(__file__))

app = gr.Blocks(css=os.path.join(current_script_dir, "..", "assets/style.css"))


def launch_ui():
    with app:
        gr.Markdown("<h2 style='text-align:center;'> PDF Assistant </h2>")

        chatbot = gr.HTML()
        user_input = gr.Textbox(placeholder="Enter your question here...", label="Your Question")
        submit_button = gr.Button("🚀 Ask")

        def submit(question):
            if not question.strip():
                return "<span style='color:red;'>Please enter valid question.</span>"
            answer, sources, found = get_answer(question)

            if not found:
                return f"""
                        <div class="error-box">
                          ❌ Information Not Found. Jira Ticket Created: 
                          <a target='_blank' href='{answer}'>{answer}</a>
                        </div>
                        """

            return f"""<b>Answer:</b><br>{answer}<br>
                     <small style='color:#888;'><b>Citations:</b> {sources}</small>"""

        submit_button.click(submit, inputs=[user_input], outputs=[chatbot])

    app.launch()
