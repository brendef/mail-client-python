# imports
import imaplib, email, os, time

# email credidentials
user = ''
password = ''
imap_url = ''

# becomes true when the user presses start
program_running = True

# sets up the authentication
def authenticate(user,password,imap_url):
    con = imaplib.IMAP4_SSL(imap_url)
    con.login(user,password)
    return con

# extracts the body from the email
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None,True)

# get the email that has been requested by its uid
def get_mail(mail_uid):
    result, data = con.uid('fetch',mail_uid,'(RFC822)')
    raw = email.message_from_string(data[0][1])
    print '#################################################################'
    print '#################################################################'
    print get_body(raw)

# find the uid of the last email sent
def get_last_uid():
    typ, ids = con.uid('search', None, 'ALL')
    ids = ids[0].decode().split()
    heighest_uid = ids[0]
    for id in ids:
        if id > heighest_uid:
            heighest_uid = id
    return heighest_uid

#get all the mail that hasn't been read
def fetch_unread_mail():
    typ, data = con.search(None,'UNSEEN')
    data = data[0].decode().split()
    for id in data:
        result, data = con.fetch(id, '(RFC822)')
        raw = email.message_from_string(data[0][1])
        print '#################################################################'
        print '#################################################################'
        print get_body(raw)

#program starts heren (technically)
con = authenticate(user,password,imap_url)
con.select('INBOX')
fetch_unread_mail()
last_uid = get_last_uid()

while program_running:
    result, data = con.uid('fetch',last_uid,'(RFC822)')
    if data != [None]:
        get_mail(last_uid)
        last_uid = int(last_uid) + 1
