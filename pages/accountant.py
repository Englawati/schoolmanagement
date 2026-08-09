import streamlit as st
import streamlit.components.v1 as components
from database.supabase_client import supabase


def render_thermal_receipt(student_name, amount, payment_date, record_id="N/A", status="Paid"):
    """
    Renders an HTML receipt optimized for standard and POS thermal printers (80mm width).
    Triggers window.print() when the accountant clicks 'Print Receipt'.
    """
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @media print {{
                body {{
                    width: 80mm;
                    margin: 0;
                    padding: 5px;
                    font-family: 'Courier New', Courier, monospace;
                    font-size: 12px;
                }}
                .no-print {{
                    display: none !important;
                }}
            }}
            body {{
                font-family: 'Courier New', Courier, monospace;
                width: 300px;
                margin: 0 auto;
                padding: 12px;
                border: 1px dashed #ccc;
                background-color: #ffffff;
                color: #000000;
            }}
            .text-center {{ text-align: center; }}
            .text-right {{ text-align: right; }}
            .line {{ border-bottom: 1px dashed #000; margin: 8px 0; }}
            .btn-print {{
                background-color: #28a745;
                color: white;
                border: none;
                padding: 10px 16px;
                font-size: 14px;
                font-weight: bold;
                cursor: pointer;
                border-radius: 4px;
                margin-bottom: 12px;
                width: 100%;
            }}
            .btn-print:hover {{
                background-color: #218838;
            }}
            table {{ width: 100%; border-collapse: collapse; }}
            td {{ padding: 3px 0; }}
        </style>
    </head>
    <body>
        <button class="btn-print no-print" onclick="window.print()">🖨️ Send to Printer</button>
        
        <div class="text-center">
            <h3 style="margin: 0;">SHREE JANTA SECONDARY SCHOOL BALUHAWA</h3>
            <p style="margin: 2px 0;">MAYADEVI -05 KAPILVASTU</p>
            <p style="margin: 2px 0;">Tel: +977 9806928278</p>
        </div>
        
        <div class="line"></div>
        
        <table>
            <tr><td><strong>Receipt #:</strong></td><td class="text-right">#{record_id}</td></tr>
            <tr><td><strong>Date:</strong></td><td class="text-right">{payment_date}</td></tr>
            <tr><td><strong>Student:</strong></td><td class="text-right">{student_name}</td></tr>
            <tr><td><strong>Status:</strong></td><td class="text-right">{status}</td></tr>
        </table>
        
        <div class="line"></div>
        
        <table>
            <tr>
                <td><strong>Description</strong></td>
                <td class="text-right"><strong>Amount</strong></td>
            </tr>
            <tr>
                <td>Academic Fee Payment</td>
                <td class="text-right">Rs. {float(amount):,.2f}</td>
            </tr>
        </table>
        
        <div class="line"></div>
        
        <table>
            <tr>
                <td><strong>TOTAL PAID:</strong></td>
                <td class="text-right"><strong>Rs. {float(amount):,.2f}</strong></td>
            </tr>
        </table>
        
        <div class="line"></div>
        
        <div class="text-center" style="margin-top: 15px;">
            <p style="margin: 0;">Thank you for your payment!</p>
            <p style="margin: 2px 0; font-size: 10px;">Computer Generated Receipt</p>
        </div>
    </body>
    </html>
    """
    components.html(html_content, height=450, scrolling=True)


def render_accountant_dashboard():

    st.title("💰 Accountant Dashboard")

    user = st.session_state.user

    st.success(
        f"Welcome Accountant, {user.get('full_name', 'Accountant')}"
    )

    st.divider()

    menu = st.selectbox(
        "Accountant Menu",
        [
            "Dashboard",
            "Add Fee",
            "Fee Records",
            "Print Receipt"
        ]
    )

    if menu == "Dashboard":

        st.subheader("Financial Overview")

        try:

            data = (
                supabase
                .table("fees")
                .select("*")
                .execute()
            )

            records = data.data

            total = sum(
                float(x.get("amount", 0))
                for x in records
            )

            paid = sum(
                float(x.get("amount", 0))
                for x in records
                if x.get("status") == "Paid"
            )

            pending = sum(
                float(x.get("amount", 0))
                for x in records
                if x.get("status") == "Pending"
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Total Fees",
                f"Rs. {total:,.2f}"
            )

            col2.metric(
                "Paid",
                f"Rs. {paid:,.2f}"
            )

            col3.metric(
                "Pending",
                f"Rs. {pending:,.2f}"
            )

        except Exception as e:
            st.error(str(e))
    
    elif menu == "Add Fee":

        st.subheader("Add Student Fee")

        with st.form("fee_form"):

            student_name = st.text_input(
                "Student Name"
            )

            amount = st.number_input(
                "Amount",
                min_value=0.0,
                step=100.0
            )

            status = st.selectbox(
                "Status",
                ["Paid", "Pending"]
            )

            payment_date = st.date_input(
                "Payment Date"
            )

            submitted = st.form_submit_button(
                "Save Fee"
            )

            if submitted:

                if not student_name:
                    st.error(
                        "Student name is required."
                    )

                elif amount <= 0:
                    st.error(
                        "Amount must be greater than 0."
                    )

                else:

                    try:

                        response = supabase.table(
                            "fees"
                        ).insert({
                            "student_name": student_name,
                            "amount": amount,
                            "status": status,
                            "payment_date": str(payment_date)
                        }).execute()

                        st.success(
                            "Fee record saved successfully."
                        )

                        # Store record details in session state for receipt printing
                        inserted_row = response.data[0] if response.data else {}
                        st.session_state["last_added_receipt"] = {
                            "id": inserted_row.get("id", "N/A"),
                            "student_name": student_name,
                            "amount": amount,
                            "status": status,
                            "payment_date": str(payment_date)
                        }

                    except Exception as e:
                        st.error(str(e))

        # Show print button right below form after entry
        if "last_added_receipt" in st.session_state:
            st.divider()
            st.subheader("🖨️ Quick Print New Receipt")
            rec = st.session_state["last_added_receipt"]
            render_thermal_receipt(
                student_name=rec["student_name"],
                amount=rec["amount"],
                payment_date=rec["payment_date"],
                record_id=rec["id"],
                status=rec["status"]
            )

    elif menu == "Fee Records":

        st.subheader("All Fee Records")

        try:

            data = (
                supabase
                .table("fees")
                .select("*")
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

    elif menu == "Print Receipt":

        st.subheader("🖨️ Search & Print Receipt")

        try:

            data = (
                supabase
                .table("fees")
                .select("*")
                .order("id", desc=True)
                .execute()
            )

            records = data.data

            if records:
                # Create dropdown search options: "ID - Student Name (Rs. Amount)"
                options = {
                    f"#{r.get('id')} - {r.get('student_name')} (Rs. {float(r.get('amount', 0)):,.2f})": r
                    for r in records
                }

                selected_label = st.selectbox(
                    "Select Student Record to Print:",
                    list(options.keys())
                )

                selected_record = options[selected_label]

                st.divider()
                st.write("**Receipt Preview:**")

                render_thermal_receipt(
                    student_name=selected_record.get("student_name", "N/A"),
                    amount=selected_record.get("amount", 0),
                    payment_date=selected_record.get("payment_date", "N/A"),
                    record_id=selected_record.get("id", "N/A"),
                    status=selected_record.get("status", "Paid")
                )

            else:
                st.info("No fee records available to print.")

        except Exception as e:
            st.error(str(e))