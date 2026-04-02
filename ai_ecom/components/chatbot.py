import reflex as rx
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

from ..state.products_state import ProductsState

class ChatState(rx.State):
    is_open: bool = False
    messages: list[dict] = [
        {"role": "bot", "content": "Hello! I'm your AI Shopping Assistant. How can I help you today?"}
    ]
    input_text: str = ""

    def toggle_chat(self):
        self.is_open = not self.is_open

    def set_input_text(self, text: str):
        self.input_text = text

    async def send_message(self):
        if not self.input_text.strip():
            return

        user_msg = self.input_text
        self.messages.append({"role": "user", "content": user_msg})
        self.input_text = ""

        # Groq LLM integration
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            self.messages.append({
                "role": "bot", 
                "content": "I'm sorry, but the Groq API key is not configured. Please add GROQ_API_KEY to your .env file to enable the AI Chatbot."
            })
            return

        try:
            client = Groq(api_key=api_key)
            
            # Get products context from ProductsState
            products_state = await self.get_state(ProductsState)
            products_info = products_state.chatbot_context

            # Convert messages to Groq format
            groq_messages = [
                {"role": "system", "content": f"You are a helpful AI Shopping Assistant for 'AI Shop'. You help users find products, answer questions about shopping, and provide recommendations. \n\n{products_info}\n\nIMPORTANT: \n1. Always provide prices in Indian Rupees (₹). \n2. When suggesting a product from the list above, ALWAYS provide a markdown link to it in this format: [Product Name](/product/PRODUCT_ID). For example: [Wireless Headphones](/product/123). \n3. Be concise and friendly."}
            ]
            for msg in self.messages[-5:]: # Only send last 5 messages for context
                role = "assistant" if msg["role"] == "bot" else "user"
                groq_messages.append({"role": role, "content": msg["content"]})

            chat_completion = client.chat.completions.create(
                messages=groq_messages,
                model="llama-3.3-70b-versatile",
            )
            
            bot_response = chat_completion.choices[0].message.content
            self.messages.append({"role": "bot", "content": bot_response})
            
        except Exception as e:
            print(f"Error in Groq Chatbot: {e}")
            self.messages.append({
                "role": "bot", 
                "content": f"I'm having trouble connecting to my AI brain right now. Error: {str(e)}"
            })

def chatbot():
    return rx.box(
        # Floating Bubble
        rx.button(
            rx.icon("message_circle", size=24, color="white"),
            on_click=ChatState.toggle_chat,
            border_radius="full",
            width="60px",
            height="60px",
            background_color="#3b82f6",
            box_shadow="lg",
            _hover={"transform": "scale(1.1)", "background_color": "#2563eb"},
            transition="all 0.2s",
            position="fixed",
            bottom="24px",
            right="24px",
            z_index="2000",
        ),
        
        # Chat Window
        rx.cond(
            ChatState.is_open,
            rx.card(
                rx.vstack(
                    # Header
                    rx.hstack(
                        rx.heading("AI Assistant", size="5", color="white"),
                        rx.spacer(),
                        rx.icon("x", size=20, color="white", cursor="pointer", on_click=ChatState.toggle_chat),
                        width="100%",
                        padding="4",
                        background_color="#3b82f6",
                        border_radius="lg lg 0 0",
                    ),
                    
                    # Message History
                    rx.box(
                        rx.vstack(
                            rx.foreach(
                                ChatState.messages,
                                lambda msg: rx.box(
                                    rx.markdown(
                                        msg["content"],
                                        padding="3",
                                        border_radius="lg",
                                        background_color=rx.cond(msg["role"] == "user", "#eff6ff", "#f3f4f6"),
                                        color=rx.cond(msg["role"] == "user", "#1e40af", "#374151"),
                                        font_size="14px", # Markdown usually needs a specific font size
                                        width="fit-content",
                                        align_self=rx.cond(msg["role"] == "user", "flex-end", "flex-start"),
                                    ),
                                    width="100%",
                                    display="flex",
                                    justify_content=rx.cond(msg["role"] == "user", "flex-end", "flex-start"),
                                ),
                            ),
                            spacing="3",
                            padding="4",
                            overflow_y="auto",
                            height="350px",
                        ),
                        width="100%",
                    ),
                    
                    # Input
                    rx.hstack(
                        rx.input(
                            placeholder="Type your message...",
                            value=ChatState.input_text,
                            on_change=ChatState.set_input_text,
                            debounce_timeout=0,
                            on_key_down=lambda e: rx.cond(e == "Enter", ChatState.send_message(), rx.console_log("")),
                            width="100%",
                            border_radius="full",
                        ),
                        rx.button(
                            rx.icon("send", size=18),
                            on_click=ChatState.send_message,
                            color_scheme="blue",
                        ),
                        width="100%",
                        padding="4",
                        border_top="1px solid #f3f4f6",
                    ),
                    spacing="0",
                    width="100%",
                ),
                width="350px",
                height="500px",
                position="fixed",
                bottom="100px",
                right="24px",
                z_index="2000",
                padding="0",
                box_shadow="2xl",
                border_radius="xl",
            ),
        ),
    )
