import smtplib as s

def send_mail(sender_email, sender_password, recipient_email, subject, body, img=None, attachment=None):
    ob=s.SMTP("smtp.gmail.com",587)
    ob.ehlo()
    ob.starttls()
    ob.login(sender_email,sender_password)
    sub=subject
    msg=body
    message="Subject:{}\n\n{}".format(sub,msg)
    ob.sendmail("sender_email_id",recipient_email,message)
    print("send successfully")
    ob.quit()
    return True