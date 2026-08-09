import streamlit as st
from database.supabase_client import supabase


def render_student_dashboard():

    st.title("🎓 Student Dashboard")

    user = st.session_state.user

    st.success(
        f"Welcome Student, {user.get('full_name', 'Student')}"
    )

    st.divider()

    menu = st.selectbox(
        "Student Menu",
        [
            "Dashboard",
            "Homework",
            "Attendance",
            "Fees"
        ]
    )

    if menu == "Dashboard":

        st.subheader("My School Portal")

        st.info(
            "From here you can view homework, "
            "attendance and fee information."
        )

    elif menu == "Homework":

        st.subheader("📚 Homework")

        try:

            data = (
                supabase
                .table("homework")
                .select("*")
                .execute()
            )

            if data.data:
                st.dataframe(
                    data.data,
                    use_container_width=True
                )
            else:
                st.info("No homework available.")

        except Exception as e:
            st.error(str(e))

    elif menu == "Attendance":

        st.subheader("📅 Attendance")

        try:

            data = (
                supabase
                .table("attendance")
                .select("*")
                .eq(
                    "student_name",
                    user.get("full_name")
                )
                .execute()
            )

            if data.data:
                st.dataframe(
                    data.data,
                    use_container_width=True
                )
            else:
                st.info("No attendance records.")

        except Exception as e:
            st.error(str(e))

    elif menu == "Fees":

        st.subheader("💰 My Fees")

        try:

            data = (
                supabase
                .table("fees")
                .select("*")
                .eq(
                    "student_name",
                    user.get("full_name")
                )
                .execute()
            )

            if data.data:
                st.dataframe(
                    data.data,
                    use_container_width=True
                )
            else:
                st.info("No fee records.")

        except Exception as e:
            st.error(str(e))