# Send_my_IP

#    ___              _                  ___ ___ 
#   / __| ___ _ _  __| |___ _ __ _  _ __|_ _| _ |
#   \__ \/ -_) ' \/ _` |___| '  \ || |___| ||  _|
#   |___/\___|_||_\__,_|   |_|_|_\_, |  |___|_|  
#                                |__/           

 #   Authored by: r_panov on 07/2018           
 #  'momentary masters of a fraction of a dot' - Carl Sagan' 
 
 # The 'Send_my_IP' tool was created for system adminstrators, pen-testers, those with public facing web servers,
 # and any others who need to know their systems public facing IP address at a specific point in time.
 
 # The purpose of this tool is to send an email over SMTP which contains the users IP Address with a time stamp. 
 # The tool can be bundle in to a cron job in order to systematically send notifications of your web servers' 
 # internet location at a specific point in time.
 
# This project is coded in python3 and requires the following packages:
# subprocess   --> installation: pip3 install subprocess
# smtplib      --> installation: pip3 install smtplib

# Download and run Send_my_IP from command line:
# 1) git clone https://github.com/rpanov/Send_my_IP.git
# 2) Modify the 'gmail_params.txt' file with your gmail account credentials for authenitcation over SMTP
# 3) Modify the 'gmail_params.txt' file with the sending and recieving email addressed
# 4) Modify your gmail security settings by going to this link and allowing less secure apps. 
#      link: https://myaccount.google.com/lesssecureapps
#      It’s turned off by default so you have to turn it on.
#      Thats it! Your good to go and can start phoning home your web servers location through gmail SMTP and python3

# 5) Command line$ python3 Send_my_IP.py

# 6) Additionally, a text file called 'IPfile.txt' will be created and appended to every time the script is run and stored in the current
# working directory to keep a historical record of your IP Address + Date Time combination.

# Please feel free to give advice, ideas, and opinions on how it can be improved!

# Thanks.
 
 
 
 
