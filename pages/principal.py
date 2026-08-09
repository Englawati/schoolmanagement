import streamlit as st
from database.supabase_client import supabase


def render_principal_dashboard():

    st.title("👨‍💼 Principal Dashboard")

    user = st.session_state.user

    st.success(
        f"Welcome Principal, {user.get('full_name', 'Principal')}"
    )

    st.divider()

    # Statistics
    col1, col2, col3, col4 = st.columns(4)

    try:
        students = supabase.table("students").select("*").execute()
        teachers = supabase.table("teachers").select("*").execute()
        attendance = supabase.table("attendance").select("*").execute()
        fees = supabase.table("fees").select("*").execute()

        student_count = len(students.data)
        teacher_count = len(teachers.data)
        attendance_count = len(attendance.data)
        fee_count = len(fees.data)

    except Exception:
        student_count = 0
        teacher_count = 0
        attendance_count = 0
        fee_count = 0

    col1.metric("Students", student_count)
    col2.metric("Teachers", teacher_count)
    col3.metric("Attendance Records", attendance_count)
    col4.metric("Fee Records", fee_count)

    st.divider()

    menu = st.selectbox(
        "Principal Menu",
        [
            "Dashboard",
            "Students",
            "Teachers",
            "Attendance",
            "Fees"
        ]
    )

    if menu == "Dashboard":

        st.subheader("School Overview")

        st.info(
            "Principal can manage students, teachers, attendance "
            "and financial information."
        )

    elif menu == "Students":

        st.subheader("Student Management")

        with st.form("add_student"):

            name = st.text_input("Student Name")
            email = st.text_input("Email")
            class_name = st.text_input("Class")
            phone = st.text_input("Phone")
            address = st.text_area("Address")

            submitted = st.form_submit_button(
                "Add Student"
            )

            if submitted:

                if not name:
                    st.error("Student name is required.")
                else:

                    try:

                        supabase.table("students").insert({
                            "name": name,
                            "email": email,
                            "class_name": class_name,
                            "phone": phone,
                            "address": address
                        }).execute()

                        st.success(
                            "Student added successfully."
                        )

                    except Exception as e:
                        st.error(str(e))

        st.subheader("All Students")

        try:

            data = (
                supabase
                .table("students")
                .select("*")
                .execute()
            )

            if data.data:
                st.dataframe(
                    data.data,
                    use_container_width=True
                )
            else:
                st.info("No students found.")

        except Exception as e:
            st.error(str(e))

    elif menu == "Teachers":

        st.subheader("Teacher Management")

        with st.form("add_teacher"):

            name = st.text_input("Teacher Name")
            email = st.text_input("Email")
            subject = st.text_input("Subject")
            phone = st.text_input("Phone")

            submitted = st.form_submit_button(
                "Add Teacher"
            )

            if submitted:

                try:

                    supabase.table("teachers").insert({
                        "name": name,
                        "email": email,
                        "subject": subject,
                        "phone": phone
                    }).execute()

                    st.success(
                        "Teacher added successfully."
                    )

                except Exception as e:
                    st.error(str(e))

        try:

            data = (
                supabase
                .table("teachers")
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

        st.subheader("Attendance Records")

        try:

            data = (
                supabase
                .table("attendance")
                .select("*")
                .execute()
            )

            st.dataframe(
                data.data,
                use_container_width=True
            )

        except Exception as e:
            st.error(str(e))

    elif menu == "Fees":

        st.subheader("Fee Records")

        try:

            data = (
                supabase
                .table("fees")
                .select("*")
                .execute()
            )

            st.dataframe(
                data.data,
                use_container_width=True
            )

        except Exception as e:
            st.error(str(e))