from flask import Flask, render_template, request
import os
import csv
from mail import send_mail

app = Flask(__name__)

# Define the directory to store uploaded files
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def read_emails_from_csv(csv_path):
#     emails = []
#     with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
#         reader = csv.reader(csvfile)
#         for row in reader:
#             emails.extend(row)
#     return emails

def read_emails_from_csv(csv_path):
# Initialize an empty list to store the emails
    emails = []

    # Open the CSV file
    with open(csv_path, 'r') as file:
        # Create a CSV reader object
        reader = csv.reader(file)

        # Loop through each row in the CSV
        for row in reader:
            # Append the email to the list
            emails.append(row[0])  # Assuming the email is in the first column

    # Print the list of emails
    return emails

@app.route('/')
def index():
    return render_template('index.html')





@app.route('/upload', methods=['POST'])
def upload():
    if 'csv_file' not in request.files:
        return "No file part"

    csv_file = request.files['csv_file']

    if csv_file.filename == '':
        return "No selected file"

    # Save CSV file to the specified directory
    csv_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp.csv')
    csv_file.save(csv_file_path)

    # Handle other form fields
    email_body = request.form.get('email_body')
    email_subject = request.form.get('email_subject')
    sender_email = request.form.get('sender_email')
    sender_password = request.form.get('sender_password')
    attachment = request.files.get('attachment')
    attachment_content = None

    # # Save attachment if provided
    # if attachment:
    #     attachment_path = os.path.join(app.config['UPLOAD_FOLDER'], attachment.filename)
    #     attachment.save(attachment_path)
    #     with open(attachment_path, 'rb') as attachment_file:
    #         attachment_content = attachment_file.read()

    # Read recipient emails from CSV
    recipient_emails = read_emails_from_csv(csv_file_path)
    print(recipient_emails)
    # Now you have all the form data and recipient emails, you can proceed with sending emails
    if send_mail(sender_email, sender_password, recipient_emails, email_subject, email_body, attachment_content):
        os.remove(csv_file_path)
        

    # Optionally, delete the uploaded files here
    
    # if attachment_path:
    #     os.remove(attachment_path)

    return render_template('success.html', message='Emails sent successfully!')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/how')
def how():
    return render_template('how.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

if __name__ == '__main__':
    app.run(debug=True)
