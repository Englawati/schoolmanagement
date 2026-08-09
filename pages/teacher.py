import streamlit as st
from database.supabase_client import supabase


def render_teacher_dashboard():

    st.title("👨‍🏫 Teacher Dashboard")

    user = st.session_state.user

    st.success(
        f"Welcome Teacher, {user.get('full_name', 'Teacher')}"
    )

    st.divider()

    menu = st.selectbox(
        "Teacher Menu",
        [
            "Dashboard",
            "Students",
            "Attendance",
            "Homework"
        ]
    )

    if menu == "Dashboard":

        st.subheader("Teacher Overview")

        col1, col2 = st.columns(2)

        try:

            students = (
                supabase
                .table("students")
                .select("*")
                .execute()
            )

            homework = (
                supabase
                .table("homework")
                .select("*")
                .execute()
            )

            col1.metric(
                "Total Students",
                len(students.data)
            )

            col2.metric(
                "Homework",
                len(homework.data)
            )

        except Exception as e:
            st.error(str(e))

    elif menu == "Students":

        st.subheader("Students")

        try:

            data = (
                supabase
                .table("students")
                .select("*")
                .execute()
            )

            st.dataframe(
                data.data,
                use_container_width=True
            )

        except Exception as e:
            st.error(str(e))

    elif menu == "Attendance":

        st.subheader("Mark Attendance")

        try:

            students = (
                supabase
                .table("students")
                .select("*")
                .execute()
            )

            if students.data:

                student_names = [
                    s["name"]
                    for s in students.data
                ]

                student = st.selectbox(
                    "Student",
                    student_names
                )

                status = st.selectbox(
                    "Attendance",
                    ["Present", "Absent", "Late"]
                )

                if st.button("Save Attendance"):

                    selected_student = next(
                        s for s in students.data
                        if s["name"] == student
                    )

                    supabase.table(
                        "attendance"
                    ).insert({
                        "student_name": selected_student["name"],
                        "class_name": selected_student["class_name"],
                        "status": status
                    }).execute()

                    st.success(
                        "Attendance saved."
                    )

            else:
                st.info("No students available.")

        except Exception as e:
            st.error(str(e))

    elif menu == "Homework":

        st.subheader("Create Homework")

        with st.form("homework_form"):

            subject = st.text_input("Subject")
            title = st.text_input("Homework Title")
            description = st.text_area(
                "Description"
            )
            teacher_name = user.get(
                "full_name",
                "Teacher"
            )
            due_date = st.date_input(
                "Due Date"
            )

            submitted = st.form_submit_button(
                "Create Homework"
            )

            if submitted:

                try:

                    supabase.table(
                        "homework"
                    ).insert({
                        "subject": subject,
                        "title": title,
                        "description": description,
                        "teacher_name": teacher_name,
                        "due_date": str(due_date)
                    }).execute()

                    st.success(
                        "Homework created successfully."
                    )

                except Exception as e:
                    st.error(str(e))

        st.subheader("Homework List")

        try:

            data = (
                supabase
                .table("homework")
                .select("*")
                .execute()
            )

            st.dataframe(
                data.data,
                use_container_width=True
            )

        except Exception as e:
            st.error(str(e))