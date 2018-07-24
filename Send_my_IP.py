import subprocess
import smtplib


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

    sendMyIP(x,y)


# Send SMTP email using user defined parameters stored in gmail_params.txt file
def sendMyIP(x,y): #TODO: add back x,y variables to function input
    # 1. Run subprocess for hostname to be used later in email
    hostname = subprocess.run(['hostname'], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')

    # 2. Read gmail_UP.txt file from working directory to obtain username/password for smtp email below
    f = open('gmail_params.txt')
    data = f.read()
    uname = data.split('\n')[4].strip()      # read and strip username from file
    pwd = data.split('\n')[7].strip()        # read and strip password from file
    mailfrom = data.split('\n')[10].strip()  # read and strip sender from file
    mailto = data.split('\n')[13].strip()    # read and strip recipient from file

    # 3. send mail over SMTP using gmail and credentials/variables stored above
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(uname, pwd)
    server.sendmail(
         mailfrom,
         mailto,
         f"\nSender:\t\t{hostname}\nDate:\t\t  {y}\nPublic IP:\t{x}")
    server.quit()

    # 4. Print success message
    print('\nMail Sent!')
    print(f"\t--->\tSender:\t{mailfrom}\n\t--->\tRecipient:\t{mailto}\n")


# Define order to run functions
def main():
    PrintBanner()
    watsMyIP()


# Run main function
main()


