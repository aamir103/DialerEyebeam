# Flask SIP Dialer Web App

This is a simple Flask web application created by **Aamir Jiwani** that allows you to upload a CSV or Excel file containing contact details and dial phone numbers using a SIP client via `sip:` URIs.

## Features
- Upload CSV or Excel file with contacts (supports `.csv`, `.xls`, `.xlsx`)
- Displays one contact at a time with details
- Start and Next buttons to control dialing workflow
- Uses system command to open SIP URI (works on Windows with a compatible SIP client)
- Handles common CSV encoding issues and missing data gracefully

## CSV/Excel File Format

Your file should contain the following columns (case-sensitive):
- `fname` — First Name
- `lname` — Last Name
- `Phone` — Phone Number (digits only, no formatting)
- `address` — Address or Company
- `comments` — Any notes or comments

Example CSV:

```csv
fname,lname,Phone,address,comments
John,Doe,923001234567,Example Inc,Important client
Jane,Smith,923009876543,Another Co,Follow up next week

Usage
Upload your contacts file

Click Start Dialing

Click Next to dial next contact

Deployment
This app can be deployed on platforms like Railway, PythonAnywhere, or your own VPS with Gunicorn and NGINX.

License
MIT License

Created by Aamir Jiwani
