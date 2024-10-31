import os
import streamlit as st
import pdfkit

# Function to create the report
def create_report(patient_info, symptoms, appointment_type, findings):
    image_path = os.path.abspath("icon.jpg")  # Path to the header logo
    footer_image_path = os.path.abspath("icon1.jpg")  # Path to the footer logo

    report_content = f"""
    <div style="display: flex; align-items: flex-start; justify-content: space-between;">
        <!-- Header with Logo on Left -->
        <div style="flex: 1; text-align: left;">
            <img src='file:///{image_path}' alt='Logo' style='width: 85px; height: 85px;'/>
        </div>
        
        <!-- Title in the Center -->
        <div style="flex: 2; text-align: center;">
            <h1 style="margin-bottom: 10px;">Medical Report</h1>
        </div>
        
        <!-- Dr. Abid Ali's Info on the Right -->
        <div style="flex: 1; text-align: right;">
            <p style="font-size: 14px; font-weight: bold; margin: 0;'>Dr. Abid Ali</p>
            <p style="font-size: 12px; margin: 0;'>Address: ABCDFERER</p>
        </div>
    </div>
    <hr/>

    <!-- Patient Information -->
    <h2>Patient Information</h2>
    <p>Patient Name: {patient_info['name']}</p>
    <p>Age: {patient_info['age']}</p>
    <p>Phone Number: {patient_info['phone']}</p>
    <p>Locality: {patient_info['locality']}</p>
    <p>City: {patient_info['city']}</p>
    <p>Country: {patient_info['country']}</p>
    <p>Sex: {patient_info['sex']}</p>
    <p>Address: {patient_info['address']}</p>
    <p>Email: {patient_info['email']}</p>

    <!-- Reason for Assessment -->
    <h2>Reason for Assessment</h2>
    <p>Symptoms: {symptoms}</p>
    <p>Appointment For: {appointment_type}</p>

    <h2>Findings</h2>
    <p>{findings}</p>

    <!-- Footer with resized icon1.jpg -->
    <div style="position: fixed; bottom: 0; left: 0; width: 100%; padding-left: 15px;">
        <img src='file:///{footer_image_path}' alt='Footer Logo' style='width: 100px; height: 100px;'/>
    </div>
    """
    return report_content

# Streamlit UI
st.set_page_config(page_title="Medical Assessment Chatbot", layout="wide")

# Display title
st.markdown("""
    <h2 style='text-align: center;'>
        Medical Assessment Chatbot
    </h2>
""", unsafe_allow_html=True)

# Sidebar for contact information
st.sidebar.header("Contact Information")
st.sidebar.text("Email: abidfareedi@medical.com")
st.sidebar.text("Contact #: 87989799887")

# Sidebar for logo
st.sidebar.image("test.jpg", use_column_width=True)  # Replace with your logo path

# Section 1: Medical Assessment Session
st.header("Medical Assessment Session")

# Collect Patient Personal Details
st.subheader("Patient Personal Details")
patient_info = {
    'name': st.text_input("Enter your Name"),
    'age': st.number_input("Enter your Age", min_value=1),
    'phone': st.text_input("Enter your Phone Number", value='87989799887'),
    'locality': st.text_input("Enter your Locality", value='Shah Faisal Town'),
    'city': st.text_input("Enter your City"),
    'country': st.text_input("Enter your Country"),
    'address': st.text_input("Enter your Address", value='Shah Faisal Town, Karachi'),
    'email': st.text_input("Enter your Email Address", value='shehzadahmed@medical.com'),
    'sex': st.selectbox("Select your Sex", options=["M", "F", "Other"])
}

# Collect Appointment Information (self or someone else)
appointment_for = st.selectbox("Is the appointment for yourself or someone else?", ["Yourself", "Someone else"])

# Section 2: Medical Diagnosis Session
st.header("Medical Diagnosis Session")

# Ask the user if they are feeling well
feeling_unwell = st.radio("MediBot: Are you feeling unwell?", options=["Yes", "No"])

if feeling_unwell == "Yes":
    # If the user says "Yes", ask for symptoms
    st.write("MediBot: Okey, can you tell me what is wrong and what are the symptoms you are feeling?")
    symptoms = st.text_input("Human: Please describe the symptoms you're experiencing:")

    if symptoms:
        st.write("MediBot: Thank you for sharing your symptoms.")
    
    # If the symptoms mention headache, ask about the type of headache
    if "headache" in symptoms.lower():
        st.write("MediBot: What kind of headache are you getting?")

        # Headache type selection using radio buttons
        headache_type = st.radio(
            "Select your type of headache:", 
            options=["Migraine Headache", "Cluster Headache", "Tension Headache", "Others"]
        )

        if headache_type == "Others":
            st.write("MediBot: Please describe any other type of headache you are experiencing.")
            other_headache = st.text_input("Human: Enter other type of headache")

else:
    # If the user says "No", suggest a general checkup
    st.write("MediBot: Okay, let's proceed with a general checkup.")

# Section 3: Medical Doctor Appointment
st.header("Medical Doctor Appointment")

# Collect specialized doctor appointment preferences with dropdown
doctor_options = [
    "Dr. Abid Ali Freedi (Specialist)",
    "Dr. Shehzad Ahmed (General)",
    "Dr. Jhon (Specialist)",
    "Fr Naz (Consult)"
]

doctor_specialty = st.selectbox("Please select the doctor you want to see:", doctor_options)
time_slot = st.selectbox("Please select a time slot:", 
                         ["09:00 A.M - 11:00 A.M", "11:00 A.M - 01:00 P.M", "02:00 P.M - 04:00 P.M"])

# Button to generate report
if st.button("Generate Medical Report"):
    findings = f"Symptoms: {symptoms}. Appointment for: {appointment_for}. Doctor: {doctor_specialty}. Time Slot: {time_slot}."

    report_content = create_report(patient_info, symptoms, appointment_for, findings)

    # Create PDF with local file access enabled
    pdf_path = "medical_report.pdf"
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')  # Update the path as needed
    options = {'enable-local-file-access': None}  # Allow local file access
    pdfkit.from_string(report_content, pdf_path, configuration=config, options=options)

    st.success("Medical Report generated successfully!")

    # Display the PDF in Streamlit
    with open(pdf_path, "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    st.download_button(label="Download Medical Report PDF", data=PDFbyte, file_name="medical_report.pdf", mime='application/pdf')

    st.subheader("Generated Medical Report")
    st.markdown(report_content, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    st.write("Interact with the medical chatbot!")
