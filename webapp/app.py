import os
import smtplib
import threading
import uuid
from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import qrcode
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, flash, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, validators

import webcam

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'BALENA_DOOR_DB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MYSQL
mysql = MySQL(app)


# Register Form Class
class RegisterForm(Form):
    firstName = StringField('First Name', [validators.Length(min=1, max=50)])
    lastName = StringField('Last Name', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.Length(min=6, max=50)])


def createQrCodeImage(generatedUUID):
    # Creating an instance of qrcode
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5)

    qr.add_data(str(generatedUUID))
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save('/home/pi/Desktop/imgRepository/qrcode_test2_2.png')

    return img


def isDuplicateEmail(email):
    # Create cursor
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM D_USER WHERE EMAIL = %s", [email])

    return (result) > 0


# User Register
@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():

        firstName = form.firstName.data
        lastName = form.lastName.data
        email = form.email.data

        print(firstName)
        print(lastName)
        print(email)

        if not isDuplicateEmail(email):

            generatedUUID = uuid.uuid1()

            img = createQrCodeImage(generatedUUID)

            # Create cursor
            cur = mysql.connection.cursor()

            # Execute query
            cur.execute(
                "INSERT INTO D_USER(FIRST_NAME, LAST_NAME, EMAIL, QR_CODE,CREATED_ON) VALUES(%s, %s, %s, %s, %s)",
                (firstName, lastName, email, str(generatedUUID), datetime.now()))

            # Commit to DB
            mysql.connection.commit()

            # Close connection
            cur.close()

            sendEmail(firstName, lastName, email, img)

            flash('You are now registered and can access ', 'success')

        else:

            flash('This email is already registered', 'error')

    return render_template('register.html', form=form)


def sendEmail(firstName, lastName, email, img):
    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login('doorlocklabs@gmail.com', '@Firewall1984@!')

    msg = MIMEMultipart()  # create a message

    # setup the parameters of the message
    msg['From'] = 'doorlocklabs@gmail.com'

    msg['To'] = email
    msg['Subject'] = "DoorLockQR"

    with open('/home/pi/Desktop/imgRepository/qrcode_test2_2.png', 'rb') as f:
        img_data = f.read()

    # add in the message body
    msg.attach(MIMEText('BalenaMainDoor', 'plain'))
    image = MIMEImage(img_data, name=os.path.basename('/home/pi/Desktop/imgRepository/qrcode_test2_2.png'))
    msg.attach(image)

    # send the message via the server set up earlier
    s.send_message(msg)

    del msg


def updateUser(user, newQrCode):
    # Create cursor
    cur = mysql.connection.cursor()

    now = datetime.now()

    # Execute query
    cur.execute("UPDATE D_USER SET QR_CODE = %s ,MODIFIED_ON = %s WHERE ID = %s", (newQrCode, now, user['ID']))

    # Commit to DB
    mysql.connection.commit()


def updateQrCodesForUsers():
    with app.app_context():

        # Create cursor
        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM D_USER")

        if (result) > 0:

            users = cur.fetchall()

            for user in users:
                generatedUUID = uuid.uuid1()

                updateUser(user, generatedUUID)

                img = createQrCodeImage(generatedUUID)

                sendEmail(user['FIRST_NAME'], user['LAST_NAME'], user['EMAIL'], img)


def runApp():
    app.secret_key = 'secret123'
    scheduler.start()
    app.run(host="0.0.0.0")


scheduler = BackgroundScheduler()
job = scheduler.add_job(updateQrCodesForUsers, 'cron', day_of_week='mon-sun', hour=00, minute=00)

if __name__ == '__main__':

    try:
        print(f'start first thread')
        t1 = threading.Thread(target=runApp).start()
        print(f'start second thread')
        t2 = threading.Thread(target=webcam.startCamera()).start()
    except Exception as e:
        print("Unexpected error:" + str(e))
