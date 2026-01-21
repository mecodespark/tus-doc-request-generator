import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title="TUS Document Request Generator", layout="centered")

# ---------------- GDPR banner ----------------
st.warning(
    "🔒 GDPR Notice: This tool does NOT store, log, or transmit any personal data. "
    "All inputs are processed temporarily in memory and disappear when the page is refreshed. "
    "Only enter minimal applicant information (forename and programme)."
)

consent = st.checkbox(
    "I confirm I will only enter minimal applicant data and understand no data is stored."
)
if not consent:
    st.stop()

# ---------------- Config ----------------
DOCS = [
    "Individual semester wise marksheets",
    "Consolidated marksheets",
    "Statement of Purpose (SOP)",
    "Letter of Recommendation (LOR) - Professional Reference",
    "Work Experience Letter (WEL)",
    "Letter of Degree Completion / Provisional Degree Certificate",
    "Letter of Recommendation (LOR) - Academic Reference",
    "Official grading scale from your awarding institution",
    "Backlog Certificate (issued by your awarding institution)",
    "Submission of your portfolio (if any)",
]

st.title("Document Request Email Generator")
st.caption("Generate a standardised message to copy-paste into Prospect.")

# ---------------- Form ----------------
with st.form("generator"):
    col1, col2 = st.columns(2)

    with col1:
        forename = st.text_input(
            "Student Forename (free text)",
            placeholder="e.g., Rahul",
        )
    with col2:
        programme = st.text_input(
            "Programme Name (free text)",
            placeholder="e.g., MSc Data Analytics",
        )

    deadline_mode = st.selectbox(
        "Deadline",
        ["In 7 days", "In 14 days", "In 21 days", "Pick a date"],
        index=1
    )

    if deadline_mode == "Pick a date":
        deadline = st.date_input("Deadline Date", value=date.today() + timedelta(days=14))
    else:
        days = int(deadline_mode.split()[1])
        deadline = date.today() + timedelta(days=days)

    st.markdown("### Documents (tick to include)")
    selected_docs = st.multiselect("Required Documents", DOCS)

    st.markdown("### Optional Follow-Up Emails")
    enable_followups = st.checkbox("Include follow-up email templates")

    followup_1_selected = False
    followup_2_selected = False

    if enable_followups:
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            followup_1_selected = st.checkbox("Follow-Up Email 1 (Gentle Reminder)")
        with col_f2:
            followup_2_selected = st.checkbox("Follow-Up Email 2 (Final Check-In)")

    submitted = st.form_submit_button("Generate Email")

# ---------------- Output ----------------
if submitted:
    if not forename.strip() or not programme.strip():
        st.error("Please enter Student Forename and Programme Name.")
        st.stop()

    if not selected_docs:
        st.warning("Please select at least one document.")
        st.stop()

    doc_list = "\n".join([f"• {d}" for d in selected_docs])

    subject = f"[IMP] Additional Documents Required – {programme.strip()} @ TUS"

    body = f"""Hello {forename.strip()},

Thank you for your application to {programme.strip()} at Technological University of the Shannon (TUS).

To proceed with the assessment of your application, we kindly request you to upload the following document(s):

Required Documents:
{doc_list}

Please ensure that all documents are clear, complete, and issued by the relevant awarding or official authority.

Important Guidelines:
• Upload all documents in PDF format only.
• Each document should be clearly readable and not password protected.
• If a document is not yet available, please upload an official provisional letter or provide an expected availability date.
• Where applicable, documents must be issued on official institutional letterhead and include signature/stamp.

We also kindly request that you submit the required documents, or update us on your progress toward uploading them, by {deadline.strftime("%d %B %Y")}. This allows us to support you appropriately, especially if you are facing any delays or challenges. Please feel free to keep us informed; we are here to help.

You can also reply to this message with the documents you currently have available, and we will advise you on the next steps.

If you experience any difficulty uploading the documents or have any questions, simply reply to this message and our team will be happy to assist you.

Kind regards,
Admissions Team
Technological University of the Shannon
"""

    st.subheader("Subject (copy into Prospect)")
    st.code(subject)

    st.subheader("Email Body (copy into Prospect)")
    st.text_area("", value=body, height=420)

    # ---------------- Follow-Up Outputs ----------------
    if enable_followups and (followup_1_selected or followup_2_selected):
        st.divider()
        st.subheader("Follow-Up Email Templates")

        # ---- Follow-Up 1 ----
        if followup_1_selected:
            fu1_subject = f"Friendly Reminder – Documents for {programme.strip()} Application"

            fu1_body = f"""Hello {forename.strip()},

I hope you’re keeping well.

I just wanted to gently follow up regarding the documents requested for your application to {programme.strip()} at Technological University of the Shannon (TUS).

If you have already uploaded the documents, please feel free to ignore this message — thank you very much.

If you’re still in the process of gathering any documents or if you’re experiencing any difficulty uploading them, please don’t hesitate to let us know. We’re more than happy to support you in any way we can.

You can also reply to this message with the documents you currently have available, and we will advise you on the next steps.

Whenever convenient, we kindly ask that you submit the required documents or keep us informed of your progress.

Thank you again for your application, and we look forward to supporting you through the next steps.

Kind regards,
Admissions Team
Technological University of the Shannon
"""

            st.markdown("### 📩 Follow-Up Email 1")
            st.code(fu1_subject)
            st.text_area("Follow-Up 1 Body", value=fu1_body, height=300)

        # ---- Follow-Up 2 ----
        if followup_2_selected:
            fu2_subject = f"Checking In – Document Submission Support for {programme.strip()}"

            fu2_body = f"""Hello {forename.strip()},

I hope you are doing well.

We just wanted to check in once more regarding the outstanding documents for your application to {programme.strip()} at Technological University of the Shannon (TUS).

If you have already submitted the documents, thank you very much — we really appreciate it.

If you are facing any challenges obtaining or uploading the documents, or if you require additional time, please feel free to let us know. Our team is happy to assist or discuss any flexibility where possible.

You can also reply to this message with the documents you currently have available, and we will advise you on the next steps.

Your application remains important to us, and we want to ensure you have the support you need throughout the process.

Thank you again, and we look forward to hearing from you whenever convenient.

Kind regards,
Admissions Team
Technological University of the Shannon
"""

            st.markdown("### 📩 Follow-Up Email 2")
            st.code(fu2_subject)
            st.text_area("Follow-Up 2 Body", value=fu2_body, height=300)

st.caption(
    "Data Protection: This tool processes inputs in-memory only and does not retain or transmit personal information."
)
