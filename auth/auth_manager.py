from database.supabase_client import supabase


def signup_user(email, password, full_name, role):

    if supabase is None:
        return False, "Supabase is not configured."

    try:
        # Create Supabase authentication user
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        if not response.user:
            return False, "Signup failed."

        # Save user profile
        user_data = {
            "email": email,
            "full_name": full_name,
            "role": role
        }

        supabase.table("users").insert(user_data).execute()

        return True, "Account created successfully."

    except Exception as e:
        return False, str(e)


def login_user(email, password):

    if supabase is None:
        return False, None, "Supabase is not configured."

    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if not response.user:
            return False, None, "Invalid email or password."

        user_email = response.user.email

        profile = (
            supabase
            .table("users")
            .select("*")
            .eq("email", user_email)
            .execute()
        )

        if not profile.data:
            return False, None, "User profile not found."

        user = profile.data[0]

        return True, user, "Login successful."

    except Exception as e:
        return False, None, str(e)


def logout_user():

    if supabase is not None:
        try:
            supabase.auth.sign_out()
        except Exception:
            pass