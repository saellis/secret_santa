import smtplib
import sys
import csv
from random import shuffle

def read_csv(filename):
	with open(filename, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		return [tuple(x) for x in reader]

def shift(list):
	return list[1:] + list[:1]

if __name__ == '__main__':
	try:
		emails = {x[0]: x[1] for x in read_csv(sys.argv[1])}
	except Exception, e:
		print 'Usage: > python secret_santa.py <filename> <gmail> <password> <$ per gift>'
		exit()
	santas = emails.keys()
	shuffle(santas)
	elves = shift(santas)
	pairs = zip(santas, elves)
	fromaddr = sys.argv[2]
	password = sys.argv[3]
	money = sys.argv[4]

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, password)

	subject = 'Secret Santa Assignment'
	body = """Hello {},

	This email is a notification to let you know that it is your responsiblity to buy {} a gift this year. Try to spend around ${} on it.
	Happy Holidays!

	NOTICE: This was an automatically generated email. Nobody knows who you are buying a gift for except you."""

	for santa, elf in pairs:
		recip = emails[santa]
		message = 'Subject: %s\n\n%s' % (subject, body.format(santa, elf, money))
		server.sendmail(fromaddr, recip, message)
	print 'Emails sent out successfully!'
	server.quit()








