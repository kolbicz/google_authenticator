# 2020 by Christoph Kolbicz
# creates scannable QR codes from recovered iOS keychain data for Google Authenticator
# supply the file in json fromat as command line argument
# png's with the QR's will be created in the same directory
# python requirements: pillow, qrcode

import sys
import json
import base64
import qrcode
import urllib.parse

if len(sys.argv) < 2:
	sys.exit('Usage: %s file_with_data_from_keychain' % sys.argv[0])
else:
	with open(sys.argv[1]) as f:
	  content = json.load(f)

	for item in content:
		account = item['Account'].split(':')
		data = item['Data']
		
		issuer=urllib.parse.quote(account[0])
		try:
			label=urllib.parse.quote(account[1])
		except IndexError:
			label=''

		code =  ('otpauth://totp/' + label + '?secret=' + base64.b32encode(base64.b64decode(data.encode())).decode("utf-8").replace("=", "") + '&issuer=' + issuer)

		qr = qrcode.QRCode(version=1,box_size=10,border=5)
		qr.add_data(code)
		qr.make(fit=True)
		img = qr.make_image(fill='black', back_color='white')
		img.save(urllib.parse.unquote(issuer) + '.png')
		print('[*] - created account '+ urllib.parse.unquote(issuer))