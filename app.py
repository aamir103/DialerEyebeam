from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with a strong secret key

# Your existing functions here
# ...

def read_contacts(file_path):
    # Try reading Excel or CSV with fallback and handle empty cells
    try:
        if file_path.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_path, dtype=str)
        else:
            df = pd.read_csv(file_path, dtype=str, encoding='utf-8-sig')
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
    # Replace NaN with empty strings
    df.fillna('', inplace=True)
    contacts = df.to_dict(orient='records')
    return contacts

def call_contact(phone_number):
    SIP_DOMAIN = "access.xoiper.com"
    if phone_number:
        uri = f'sip:{phone_number}@{SIP_DOMAIN}'
        os.system(f'start {uri}')  # Works on Windows
    else:
        print("Empty phone number, skipping call.")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            filename = os.path.join('uploads', file.filename)
            os.makedirs('uploads', exist_ok=True)
            file.save(filename)
            contacts = read_contacts(filename)
            if not contacts:
                return render_template('index.html', error="Failed to read contacts file.")
            session['contacts'] = contacts
            session['current_index'] = 0
            return redirect(url_for('dial'))
        else:
            return render_template('index.html', error="Please upload a file.")
    return render_template('index.html')

@app.route('/dial', methods=['GET', 'POST'])
def dial():
    contacts = session.get('contacts', [])
    current_index = session.get('current_index', 0)

    if not contacts or current_index >= len(contacts):
        return redirect(url_for('index'))

    contact = contacts[current_index]

    if request.method == 'POST':
        # On clicking 'Next', increment index and call next contact
        phone = contact.get('Phone', '')
        phone = '' if pd.isna(phone) else str(phone).strip()
        call_contact(phone)
        current_index += 1
        session['current_index'] = current_index
        if current_index >= len(contacts):
            return redirect(url_for('index'))
        contact = contacts[current_index]

    return render_template('dial.html', contact=contact)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
