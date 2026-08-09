import streamlit as st

from config import validate_config
from auth.auth_manager import (
    login_user,
    signup_user,
    logout_user
)
from utils.session import (
    init_session_state,
    login_session,
    clear_session
)

from pages.principal import (
    render_principal_dashboard
)

from pages.teacher import (
    render_teacher_dashboard
)

from pages.student import (
    render_student_dashboard
)

from pages.accountant import (
    render_accountant_dashboard
)


st.set_page_config(
    page_title="School Management System",
    page_icon="🏫",
    layout="wide"
)


init_session_state()


def show_login():

    st.title("🏫 School Management System")

    st.subheader("Login")

    with st.form("login_form"):

        email = st.text_input(
            "Email Address"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "🔐 Login"
        )

        if submitted:

            if not email or not password:

                st.error(
                    "Please enter email and password."
                )

            else:

                success, user, message = login_user(
                    email,
                    password
                )

                if success:

                    login_session(user)

                    st.success(
                        "Login successful!"
                    )

                    st.rerun()

                else:
                    st.error(message)


def show_signup():

    st.title("📝 Create Account")

    with st.form("signup_form"):

        full_name = st.text_input(
            "Full Name"
        )

        email = st.text_input(
            "Email Address"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        role = st.selectbox(
            "Role",
            [
                "principal",
                "teacher",
                "student",
                "accountant"
            ]
        )

        submitted = st.form_submit_button(
            "Create Account"
        )

        if submitted:

            if not full_name:
                st.error("Full name is required.")

            elif not email:
                st.error("Email is required.")

            elif len(password) < 6:
                st.error(
                    "Password must contain at least 6 characters."
                )

            elif password != confirm_password:
                st.error(
                    "Passwords do not match."
                )

            else:

                success, message = signup_user(
                    email,
                    password,
                    full_name,
                    role
                )

                if success:

                    st.success(message)

                    st.info(
                        "You can now login with your account."
                    )

                else:
                    st.error(message)


def show_dashboard():

    role = st.session_state.role
    user = st.session_state.user

    with st.sidebar:

        st.title("🏫 School Portal")

        st.write(
            f"**User:** {user.get('full_name')}"
        )

        st.write(
            f"**Role:** {role.title()}"
        )

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            logout_user()
            clear_session()
            st.rerun()

    if role == "principal":

        render_principal_dashboard()

    elif role == "teacher":

        render_teacher_dashboard()

    elif role == "student":

        render_student_dashboard()

    elif role == "accountant":

        render_accountant_dashboard()

    else:

        st.error(
            "Invalid user role."
        )


def main():

    config_ok, config_message = validate_config()

    if not config_ok:

        st.error(config_message)

        st.info(
            "Please create .env and add your Supabase URL and key."
        )

        st.stop()

    if st.session_state.authenticated:

        show_dashboard()

    else:

        login_tab, signup_tab = st.tabs(
            [
                "🔐 Login",
                "📝 Signup"
            ]
        )

        with login_tab:
            show_login()

        with signup_tab:
            show_signup()


if __name__ == "__main__":
    main()