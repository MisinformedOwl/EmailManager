import imaplib

try:
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('jaydean1311@gmail.com', 'vqvu ibvs qoip qgii')
    print("✅ Login successful")
except imaplib.IMAP4.error as e:
    print("❌ Login failed:", e)
