import smtplib
from email.mime.text import MIMEText

def send_mail(customer, dealer, rating, comments):
	port = 2525
	smtp_server = 'smtp.mailtrap.io'
	login = '661cd906bb6621'
	password = 'b97011006e9013'
	message= f"<h3>New Feedback Submission</h3><ul><li>Customer:{customer}</li><li>Dealer:{dealer}</li><li>Rating:{rating}</li><li>Comments:{comments}</li>"

	sender_email="petiyou14@gmail.com"
	receiver_email="bolloubryan@gmail.com"
	msg = MIMEText(message, 'html')
	msg['Subject'] = 'Lexus Feedback'
	msg['From'] = sender_email
	msg['To'] = receiver_email

	with smtplib.SMTP(smtp_server, port) as server:
		server.login(login, password)
		server.sendmail(sender_email, receiver_email, msg.as_string())