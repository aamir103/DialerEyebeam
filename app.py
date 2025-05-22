from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

SIP_DOMAIN = "access.xoiper.com"

def read_contacts(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    try:
        if ext == '.csv':
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, encoding='ISO-8859-1')
        elif ext in ['.xls', '.xlsx']:
            df = pd.read_excel(file_path)
        else:
            return []
        return df.to_dict('records')
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            session['filepath'] = filepath
            session['index'] = 0
            return redirect(url_for('dial'))
    return render_template('index.html')

@app.route('/dial')
def dial():
    filepath = session.get('filepath')
    index = session.get('index', 0)

    if not filepath or not os.path.exists(filepath):
        return redirect(url_for('index'))

    contacts = read_contacts(filepath)
    if index >= len(contacts):
        return redirect(url_for('index'))

    contact = contacts[index]

    # Safe conversions
    fname = str(contact.get('fname', '')).strip()
    lname = str(contact.get('lname', '')).strip()
    phone = str(contact.get('Phone', '')).strip()
    address = str(contact.get('address', '')).strip()
    comments = str(contact.get('comments', '')).strip()

    full_contact = {
        'fname': fname,
        'lname': lname,
        'Phone': phone,
        'address': address,
        'comments': comments
    }

    sip_uri = f'sip:{phone}@{SIP_DOMAIN}'

    return render_template('dial.html', contact=full_contact, sip_uri=sip_uri, index=index+1, total=len(contacts))

@app.route('/next')
def next_contact():
    session['index'] = session.get('index', 0) + 1
    return redirect(url_for('dial'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
