import streamlit as st
import json
import os
from Chatbot import Chatbot

class StreamlitApp:
    def __init__(self):
        self.credentials_file = 'credentials.json'
        self.users_file = 'users.json'
        self.admin_credentials = self.load_admin_credentials()
        self.users = self.load_users()
        self.setup_session_state()
        self.chatbot = Chatbot()

    def load_admin_credentials(self):
        try:
            if os.path.exists(self.credentials_file):
                with open(self.credentials_file, 'r') as file:
                    return json.load(file)
        except (json.JSONDecodeError, IOError):
            return {}
        return {}

    def load_users(self):
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as file:
                    return json.load(file)
        except (json.JSONDecodeError, IOError):
            return {}
        return {}

    def save_admin_credentials(self):
        try:
            with open(self.credentials_file, 'w') as file:
                json.dump(self.admin_credentials, file, indent=2)
        except IOError:
            st.error("Error saving admin credentials")

    def save_users(self):
        try:
            with open(self.users_file, 'w') as file:
                json.dump(self.users, file, indent=2)
        except IOError:
            st.error("Error saving user data")

    def setup_session_state(self):
        defaults = {
            'user_type_selected': False,
            'selected_user_type': None,
            'logged_in': False,
            'username': None,
            'is_admin': False,
            'chat_history': [],
            'current_command': None,
            'awaiting_input': False
        }
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

    def user_type_selection_page(self):
        st.title('Welcome to A3GPT')
        st.subheader('Please select how you want to proceed:')
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button('👤 Proceed as User', use_container_width=True, type="primary"):
                st.session_state.user_type_selected = True
                st.session_state.selected_user_type = 'user'
                st.rerun()
        
        with col2:
            if st.button('👨‍💼 Proceed as Admin', use_container_width=True, type="secondary"):
                st.session_state.user_type_selected = True
                st.session_state.selected_user_type = 'admin'
                st.rerun()

    def chatbot_response(self, message):
        responses = {
            "hello": "Hi there! How can I help you today?",
            "how are you": "I'm doing great, thank you for asking!",
            "bye": "Goodbye! Have a nice day!"
        }
        return responses.get(message.lower(), "I'm not sure how to respond to that. Try a command or a simple greeting!")

    def login_page(self):
        user_type = st.session_state.selected_user_type
        st.title(f'{user_type.capitalize()} Login')
        
        if st.button('← Back to Selection'):
            st.session_state.user_type_selected = False
            st.session_state.selected_user_type = None
            st.rerun()
        
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')

        if st.button('Login'):
            # Check credentials based on user type
            if user_type == 'admin':
                # Check admin credentials from credentials.json
                if username in self.admin_credentials and self.admin_credentials[username] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.is_admin = True
                    st.success('Admin login successful')
                    st.rerun()
                    return True
                else:
                    st.error('Invalid admin credentials. Please try again.')
                    return False
            else:  # user_type == 'user'
                # Check user credentials from users.json
                if username in self.users and self.users[username] == password:
                    if username == "admin":
                        st.error('Admin account cannot login as user. Please select "Proceed as Admin".')
                        return False
                    else:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.is_admin = False
                        st.success('User login successful')
                        st.rerun()
                        return True
                else:
                    st.error('Invalid user credentials. Please try again.')
                    return False
        return False

    def registration_page(self):
        user_type = st.session_state.selected_user_type
        st.title(f'{user_type.capitalize()} Registration')
        
        if st.button('← Back to Selection'):
            st.session_state.user_type_selected = False
            st.session_state.selected_user_type = None
            st.rerun()
        
        new_username = st.text_input('New Username')
        new_password = st.text_input('New Password', type='password')

        if st.button('Register'):
            if user_type == 'admin':
                st.error('Admin registration is not allowed. Admin account must be created manually.')
                return
            
            if new_username == 'admin':
                st.error('Username "admin" is reserved.')
                return
            
            # Check if username exists in either file
            if new_username in self.users or new_username in self.admin_credentials:
                st.error('Username already exists.')
                return
            
            # Register new user in users.json
            self.users[new_username] = new_password
            self.save_users()
            st.success(f'User {new_username} registered successfully!')
            st.rerun()

    def render_chat_interface(self):
        st.markdown(
            """
            <style>
            .message-row {
                display: flex;
                margin-bottom: 10px;
                width: 100%;
            }
            .bot-message, .user-message {
                padding: 8px 12px;
                max-width: 70%;
                border-radius: 18px;
                margin: 4px 0;
                word-wrap: break-word;
            }
            .bot-message {
                background-color: #e5e5ea;
                margin-right: auto;
                text-align: left;
            }
            .user-message {
                background-color: #0078ff;
                color: white;
                margin-left: auto;
                text-align: right;
            }
            .stChatInput {
                background-color: #f0f0f0;
                border: 2px solid #0078ff;
                border-radius: 10px;
                padding: 5px;
            }
            .stChatInput input {
                color: #333333;
                background-color: transparent;
                border: none;
            }
            @media (prefers-color-scheme: dark) {
                .chat-container {
                    background-color: #1e1e1e;
                    border-color: #444;
                }
                .bot-message {
                    background-color: #333;
                    color: white;
                }
                .user-message {
                    background-color: #0062cc;
                }
                .stChatInput {
                    background-color: #2a2a2a;
                    border-color: #0062cc;
                }
                .stChatInput input {
                    color: white;
                }
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        chat_container = st.container()
        with chat_container:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for message in st.session_state.chat_history:
                st.markdown('<div class="message-row">', unsafe_allow_html=True)
                if message["role"] == "user":
                    st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    def admin_dashboard(self):
        st.title('Admin Dashboard')
        st.subheader('Student Management')
        
        if st.sidebar.button('Logout'):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.is_admin = False
            st.session_state.user_type_selected = False
            st.session_state.selected_user_type = None
            st.session_state.chat_history = []
            st.rerun()

        self.render_chat_interface()
        
        if prompt := st.chat_input("Type your message or command..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            command = prompt.strip().lower()
            response = ""

            if command == "add student" and not st.session_state.awaiting_input:
                st.session_state.current_command = "add student"
                st.session_state.awaiting_input = True
                response = "Please write the student's information in this format: name, age, grade, email"
            elif command == "get student with name" and not st.session_state.awaiting_input:
                st.session_state.current_command = "get student with name"
                st.session_state.awaiting_input = True
                response = "Please provide the student's name."
            elif command == "get student with grade" and not st.session_state.awaiting_input:
                st.session_state.current_command = "get student with grade"
                st.session_state.awaiting_input = True
                response = "Please provide the student's grade."
            elif command == "correct the student information" and not st.session_state.awaiting_input:
                st.session_state.current_command = "correct the student information"
                st.session_state.awaiting_input = True
                response = "Please provide the student's name and what information to correct (e.g., age, grade, or all information)."
            elif command == "delete all students" and not st.session_state.awaiting_input:
                st.session_state.current_command = "delete all students"
                st.session_state.awaiting_input = True
                response = "Are you sure you want to delete all students? Type 'yes' to confirm."
            elif st.session_state.awaiting_input:
                if st.session_state.current_command == "add student":
                    try:
                        name, age, grade, email = [x.strip() for x in prompt.split(',')]
                        response = self.chatbot.handle_command("add student", name, age, grade, email)
                        st.session_state.awaiting_input = False
                        st.session_state.current_command = None
                    except ValueError:
                        response = "Invalid format. Please use: name, age, grade, email"
                elif st.session_state.current_command == "get student with name":
                    response = self.chatbot.handle_command("get student with name", name=prompt)
                    st.session_state.awaiting_input = False
                    st.session_state.current_command = None
                elif st.session_state.current_command == "get student with grade":
                    response = self.chatbot.handle_command("get student with grade", grade=prompt)
                    st.session_state.awaiting_input = False
                    st.session_state.current_command = None
                elif st.session_state.current_command == "correct the student information":
                    try:
                        name, info, *values = [x.strip() for x in prompt.split(',')]
                        if info == "age":
                            age = values[0] if values else None
                            response = self.chatbot.handle_command("correct the student information", name=name, info=info, age=age)
                        elif info == "grade":
                            grade = values[0] if values else None
                            response = self.chatbot.handle_command("correct the student information", name=name, info=info, grade=grade)
                        elif info == "all information":
                            age = values[0] if len(values) > 0 else None
                            grade = values[1] if len(values) > 1 else None
                            response = self.chatbot.handle_command("correct the student information", name=name, info=info, age=age, grade=grade)
                        st.session_state.awaiting_input = False
                        st.session_state.current_command = None
                    except ValueError:
                        response = "Invalid format. Please use: name, info (age/grade/all information), new values"
                elif st.session_state.current_command == "delete all students":
                    if prompt.strip().lower() == "yes":
                        response = self.chatbot.handle_command("delete all students")
                        st.session_state.awaiting_input = False
                        st.session_state.current_command = None
                    else:
                        response = "Operation cancelled."
                        st.session_state.awaiting_input = False
                        st.session_state.current_command = None
                else:
                    response = self.chatbot_response(prompt)
            else:
                response = self.chatbot_response(prompt)

            if response:
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()

    def user_dashboard(self):
        st.title('Student Chatbot')
        st.subheader('A3GPT')
        
        if st.sidebar.button('Logout'):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.is_admin = False
            st.session_state.user_type_selected = False
            st.session_state.selected_user_type = None
            st.session_state.chat_history = []
            st.rerun()

        self.render_chat_interface()
        
        if prompt := st.chat_input("Type your message or command..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            command = prompt.strip().lower()
            response = ""

            if command == "add student" and not st.session_state.awaiting_input:
                st.session_state.current_command = "add student"
                st.session_state.awaiting_input = True
                response = "Please write the student's information in this format: name, age, grade, email"
            elif command == "correct the student information" and not st.session_state.awaiting_input:
                st.session_state.current_command = "correct the student information"
                st.session_state.awaiting_input = True
                response = "Please provide the student's name and what information to correct (e.g., age, grade, or all information)."
            elif st.session_state.awaiting_input:
                if st.session_state.current_command == "add student":
                    try:
                        name, age, grade, email = [x.strip() for x in prompt.split(',')]
                        response = self.chatbot.handle_command("add student", name, age, grade, email)
                        st.session_state.awaiting_input = False
                        st.session_state.current_command = None
                    except ValueError:
                        response = "Invalid format. Please use: name, age, grade, email"
                elif st.session_state.current_command == "correct the student information":
                    try:
                        name, info, *values = [x.strip() for x in prompt.split(',')]
                        if info == "age":
                            age = values[0] if values else None
                            response = self.chatbot.handle_command("correct the student information", name=name, info=info, age=age)
                        elif info == "grade":
                            grade = values[0] if values else None
                            response = self.chatbot.handle_command("correct the student information", name=name, info=info, grade=grade)
                        elif info == "all information":
                            age = values[0] if len(values) > 0 else None
                            grade = values[1] if len(values) > 1 else None
                            response = self.chatbot.handle_command("correct the student information", name=name, info=info, age=age, grade=grade)
                        st.session_state.awaiting_input = False
                        st.session_state.current_command = None
                    except ValueError:
                        response = "Invalid format. Please use: name, info (age/grade/all information), new values"
                else:
                    response = self.chatbot_response(prompt)
            else:
                response = self.chatbot_response(prompt)

            if response:
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()

    def main(self):
        st.set_page_config(page_title="A3GPT", layout="centered")
        
        if not st.session_state.user_type_selected:
            self.user_type_selection_page()
            return
        
        if st.session_state.logged_in:
            if st.session_state.is_admin:
                self.admin_dashboard()
            else:
                self.user_dashboard()
        else:
            menu = ["Login", "Register"]
            choice = st.sidebar.selectbox("Menu", menu)
            if choice == "Login":
                self.login_page()
            elif choice == "Register":
                self.registration_page()

if __name__ == "__main__":
    app = StreamlitApp()
    app.main()