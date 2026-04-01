import reflex as rx

class ChatState(rx.State):
    is_open: bool = False
    messages: list[dict] = [
        {"role": "bot", "content": "Hello! How can I help you today?"}
    ]
    input_text: str = ""

    def toggle_chat(self):
        self.is_open = not self.is_open

    def set_input_text(self, text: str):
        self.input_text = text

    def send_message(self):
        if self.input_text.strip():
            self.messages.append({"role": "user", "content": self.input_text})
            # Dummy bot response
            self.messages.append({"role": "bot", "content": "That's interesting! I'm here to help you find the best products."})
            self.input_text = ""

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
                                    rx.text(
                                        msg["content"],
                                        padding="3",
                                        border_radius="lg",
                                        background_color=rx.cond(msg["role"] == "user", "#eff6ff", "#f3f4f6"),
                                        color=rx.cond(msg["role"] == "user", "#1e40af", "#374151"),
                                        size="2",
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
                            placeholder="Type a message...",
                            value=ChatState.input_text,
                            on_change=ChatState.set_input_text,
                            on_key_down=lambda e: rx.cond(e == "Enter", ChatState.send_message(), rx.console_log("")),
                            size="3",
                            flex="1",
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
