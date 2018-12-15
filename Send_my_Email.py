import subprocess, argparse
import smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# banner
def PrintBanner():
    # 1. make banner
    banner = """
     ___              _                  ___ ___ 
    / __| ___ _ _  __| |___ _ __ _  _ __|_ _| _ |
    \__ \/ -_) ' \/ _` |___| '  \ || |___| ||  _|
    |___/\___|_||_\__,_|   |_|_|_\_, |  |___|_|  
                                 |__/           

    Authored by: r_panov on 07/2018           
    'momentary masters of a fraction of a dot' - Carl Sagan' 
     """
    # 2. print banner
    print(banner)


# Determine Public IP and date combination
def watsMyIP():
    # 1. import requests: HTTP for Human package
    import requests
    # 2. make get request to find public facing IP
    res = requests.get('https://dynamicdns.park-your-domain.com/getip')
    res = res.text
    # 3. run subprocess cal to get date
    date = subprocess.run(['date +%Y-%m-%d-%H:%M'], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')

    # 3. print results of get request and date call
    print(f'\nYour public facing IP Address + date combintation is: \n\t--->    {res} : {date}')

    ipWrite(res,date)


# Write the IP and Date combination to local file for historical purposes
def ipWrite(x,y):

    # 1. write IP : Date to text file
    f = open("IPfile.txt", "a+")
    f.write(f'{x} : {y}')
    f.close()

    # 2. Display the path of the file
    path = subprocess.run(['pwd'], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(f'IP + Date combination has been written to file:\n\t--->    {path.strip()}/IPfile.txt')

    sendMyIP(x)


# Send SMTP email using user defined parameters stored in gmail_params.txt file
def sendMyIP(x):

    # 1. Run subprocess for hostname to be used later in email
    hostname = subprocess.run(['hostname'], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

    # 2. Read gmail_UP.txt file from working directory to obtain username/password for smtp email below
    f = open('gmail_params.txt')
    data = f.read()
    uname = data.split('\n')[4].strip()      # read and strip username from file
    pwd = data.split('\n')[7].strip()        # read and strip password from file
    mailfrom = data.split('\n')[10].strip()  # read and strip sender from file
    mailto = data.split('\n')[13].strip()    # read and strip recipient from file
    f.close()                                # close the opened file 

    # 3. send mail over SMTP using gmail and credentials/variables stored above
    subject = "Send_my_IP Data"
    body = f"""\
    
    {hostname} has the following IP Addressed: {x}
    """
    sender_email = f'{mailfrom}'
    receiver_email = f'{mailto}'
    password = f'{pwd}'

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email         # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

    # 4. Print success message
    print('\nMail Sent!')
    print(f"\t--->\tSender:\t{mailfrom}\n\t--->\tRecipient:\t{mailto}\n")


def sendAttachment(file):

    try:
        # 1. Read gmail_UP.txt file from working directory to obtain username/password for smtp email below
        f = open('gmail_params.txt')
        data = f.read()
        uname = data.split('\n')[4].strip()  # read and strip username from file
        pwd = data.split('\n')[7].strip()  # read and strip password from file
        mailfrom = data.split('\n')[10].strip()  # read and strip sender from file
        mailto = data.split('\n')[13].strip()  # read and strip recipient from file
        f.close()

        # 2. Create email
        subject = "Send_My_Attachment Data"
        body = """\
    
        See attachment below:
        """
        sender_email = f'{mailfrom}'
        receiver_email = f'{mailto}'
        password = f'{pwd}'

        # 2.1 Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails

        # 2.2 Add body to email
        message.attach(MIMEText(body, "plain"))

        filename = f'{file}'  # In same directory as script

        # 2.3 Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # 2.4 Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # 2.5 Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # 3. Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)

        # 4. Print success message
        print('\nMail & Attachment Sent!')
        print(f"\t--->\tSender:\t{mailfrom}\n\t--->\tRecipient:\t{mailto}\n\t--->\tAttachment:\t{file}\n")

    except FileNotFoundError:
        print("Oops!  File note found.  Check spelling and retry...")


# Define order to run functions
def main():
    # 3.1. Argparse help menu: display help menu
    parser = argparse.ArgumentParser(description='Python mail utility. Send your current IP Address to gmail using '
                                                 'no CLI argument or send an attachment to your gmail using'
                                                 ' the --file CLI argument')
    # 3.2. define flags
    parser.add_argument('-f', '--file', help='Enter the file you want to email as an attachment', required=False)
    # 3.3. save input
    args = parser.parse_args()
    # 3.4. pass input to data function
    file = str(args.file)
    # function decision tree, based on input
    if file == 'None':
        PrintBanner()
        watsMyIP()
    else:
        PrintBanner()
        sendAttachment(file)


# Run main function
main()


