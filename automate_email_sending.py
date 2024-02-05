''' 
    You work at a company that sends daily reports to clients via email. The goal of this project is to automate the process of sending these reports via email.
    Here are the steps you can take to automate this process:

    Use the smtplib library to connect to the email server and send the emails.

    Use the email library to compose the email, including the recipient's email address, the subject, and the body of the email.

    Use the os library to access the report files that need to be sent.

    Use a for loop to iterate through the list of recipients and send the email and attachment.

    Use the schedule library to schedule the script to run daily at a specific time.

    You can also set up a log file to keep track of the emails that have been sent and any errors that may have occurred during the email sending process.
 '''

import smtplib, email,getpass, logging, schedule, time
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart

def sendEmail():
    host= "smtp-mail.outlook.com" # use the hotmail smtp server
    port = 587
    # sender = input("Enter the source email")
    sender = "oscobo@live.com" #you can enter your source
    #subj = input("Enter your subject: \n")
    subj = "do not be scared, not a scam"

    list_of_mails = ['nshimmiye@gmail.com','sabosco4@gmail.com'] #Enter the list of the recipients
    pswrd = getpass.getpass("Enter your password:\n")
    attachment = "training.pdf" # it has to be in same dir

    # msg = MIMEText("""
    #         Bosco is learnig how to send a msg with smtp lib with py.
    #         """)

    body = """Bosco is learnig how to send a msg with smtp lib with py."""

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["Subject"] = subj
    smtp = smtplib.SMTP(host, port)

    try:
        statCode, response = smtp.ehlo() # check the availability of the server
        print("Server is on. \n",statCode,response)

    except Exception as e:
        print(e)

    try:
        statCodeTls, responseTls = smtp.starttls() #putting the package in tls mode ( security)
        print("the TLS connections is:",statCodeTls, responseTls)
    except Exception as e:
        print(e)
    #Login
        
    try:
        statusLogin, responseLogin = smtp.login(sender,pswrd)
        print(f"Logging in: {statusLogin} {responseLogin}")

        msg.attach(MIMEText(body, "plain")) ## Add body to email

        with open(attachment, "rb") as fn: # Add file as application/octet-stream
            part = MIMEBase("application", "octet-stream")
            part.set_payload(fn.read())
            
        encoders.encode_base64(part) # Encode file in ASCII characters to send by email
        
        part.add_header( # Add header as key/value pair to attachment part
            "Content-Disposition",
            f"attachment; filename= {attachment}",
        )
        msg.attach(part)
        for ml in list_of_mails:
            pck = msg.as_string()
            smtp.sendmail(sender,ml,pck)
## LOGS
            logging.basicConfig(filename='logs.log', filemode='w',format='%(message)s - %(asctime)s -', level=logging.INFO)
            logging.info('email: %s was sent', ml)
        print("Message sent")
    except smtplib.SMTPResponseException as e:
        print(e)
        
    finally:
        smtp.quit

#Scheduled to run at 00:00
def schedule():
    schedule.every().day.at("00:00").do(sendEmail)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    sendEmail()


