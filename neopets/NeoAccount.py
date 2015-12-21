import cookielib
import gzip
import random
import string
import StringIO
import sys
import time
import urllib
import urllib2

from HideMyAssCLI import ChangeIP

class NeoAccount2:
    """ This is the HTTP wrapper for Neopets. Unknown original author, edited heavily by Jake """

    d = 'http://www.neopets.com'
    headers = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1'),
               ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
               ('Accept-Language', 'en-us,en;q=0.5'),
               ('Accept-Encoding', 'gzip, deflate')]

    def __init__(self, user, pw, bday, proxy = None):
        self.user    = user
        self.pw      = pw
        self.bday    = bday
        self.proxy   = proxy
        self.referer = ''
        self.cj      = cookielib.LWPCookieJar()
        self.cookie_handler = urllib2.HTTPCookieProcessor(self.cj)

        if proxy is not None:
            proxy_handler = urllib2.ProxyHandler({'http': 'http://' + proxy + '/'})
            self.opener = urllib2.build_opener(proxy_handler, self.cookie_handler)
        else:
            self.opener = urllib2.build_opener(self.cookie_handler)

    def __str__(self):
        return '%s:%s' % (self.user, self.pw)

    def get(self, url, referrer ='', readable = True):
        for j in range(1, 7):
            for i in range(1, 6):
                try:
                    if url[0] == '/':
                        url = self.d + url
                    if referrer == '':
                        referrer = self.referer
                    self.opener.addheaders = [('Referer', referrer)] + self.headers
                    res = self.opener.open(url)
                    self.referer = res.geturl()
                    if readable:
                        return self.readable(res)
                    else:
                        return res
                except:
                    time.sleep(15)
                    if i == 1:
                        print "\n    Error connecting to Neopets. Retrying " + str(i) + " / 5"
                    else:
                        print "    Error connecting to Neopets. Retrying " + str(i) + " / 5"
                    continue

            # Page load not successful, try changing IP
            if i <= 5:
                print "    Unable to connect. Changing IP attempt " + str(j) + " / 5\n"
            elif j == 5:
                print "    Pausing for one hour"
                time.sleep(3600)
            ChangeIP()
        print "Program unable to connect to Neopets."
        sys.exit()

    def post(self, url, data, referrer ='', readable = True):
        for j in range(1, 6):
            for i in range(1, 6):
                try:
                    if url[0] == '/':
                        url = self.d + url
                    if referrer == '':
                        referrer = self.referer
                    self.opener.addheaders = [('Content-Type', 'application/x-www-form-urlencoded'),
                                              ('Referer', referrer)] + self.headers
                    res = self.opener.open(url, urllib.urlencode(data))
                    self.referer = res.geturl()
                    if readable:
                        return self.readable(res)
                    else:
                        return res
                except:
                    time.sleep(15)
                    if i == 1:
                        print "\n    Error connecting to Neopets. Retrying " + str(i) + " / 5"
                    else:
                        print "    Error connecting to Neopets. Retrying " + str(i) + " / 5"
                    continue
                break

            # Page load not successful, try changing IP
            if i <= 5:
                print "    Unable to connect. Changing IP attempt " + str(j) + " / 5\n"
            elif j == 5:
                print "    Pausing for one hour"
                time.sleep(3600)
            ChangeIP()
        print "Program unable to connect to Neopets."
        sys.exit()

    def login(self):
        """  Logs into a neopets account - will bypass any restrictions """

        res = self.get('/index.phtml')
        html = self.post('/login.phtml', {'username': self.user,
                                          'password': self.pw,
                                          'destination': "/index.phtml"}, readable = True)
        if html.find("Invalid Password") != -1:
            return 1
        elif html.find("<b>Players Online:</b>") != -1:
            return 3
        elif html.find("http://images.neopets.com/images/neo_cop.gif") != -1:
            return 3
        elif html.find("<title>Neopets - Bad Password</title>") != -1:
            return 1
        elif html.find("please verify your birthday:") != -1:
            pos1 = html.find('<input type="hidden" name="destination" value="') + 47
            pos2 = html.find('"' , pos1)
            destination = html[pos1:pos2]
            bdayYear  = self.bday.split("-")[0]
            bdayMonth = self.bday.split("-")[1]
            bdayDay   = self.bday.split("-")[2]
            random_num1 = str(random.randrange(1, 30))
            random_num2 = str(random.randrange(1, 30))
            html = self.post('/login.phtml', {'destination': destination,
                                              'username': self.user,
                                              'password': self.pw,
                                              'x': random_num1,
                                              'y': random_num2,
                                              'dob_m': bdayMonth,
                                              'dob_d': bdayDay,
                                              'dob_y': bdayYear}, readable = True)
            if html.find('<title>Accept Privacy Policy and Terms of Use</title>') != -1:
                postdata = {}
                pos1 = html.find("<input type='hidden' name='destination' value=") + 47
                pos2 = html.find('"' , pos1)
                destination = html[pos1:pos2]
                postdata['destination'] = destination
                postdata['accept'] = '1'

                if html.find("Enter Your Email Address") != -1 or html.find("Enter Your Parent's Email Address") != -1:
                    random_num = random.randrange(1, 4)
                    if random_num == 1: ending = "@gmail.com";
                    elif random_num == 2: ending = "@hotmail.com";
                    else: ending = "@outlook.com";
                    email = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(12)) + ending
                    postdata['email1'] = email
                    postdata['email2'] = email
                if html.find("<select name='country' id='countrySelect'") != -1: postdata['country'] = 'US';
                if html.find("<select name='state' id='stateSelect'") != -1: postdata['state'] = 'CA';
                html = self.post('/accept_terms.phtml', postdata, readable = True)
                if html.find("<b>Players Online:</b>") != -1:
                    return 3
                elif html.find("http://images.neopets.com/images/neo_cop.gif") != -1:
                    return 3
                elif html.find("var species_arr") != -1:
                    postdata = {}
                    pet_name = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
                    random_num1 = random.randrange(1, 9)
                    random_num2 = random.randrange(1, 5)
                    random_num3 = random.randrange(1, 3)

                    if random_num1 == 1: postdata['selected_pet'] = 'zafara';
                    elif random_num1 == 2: postdata['selected_pet'] = 'wocky';
                    elif random_num1 == 3: postdata['selected_pet'] = 'korbat';
                    elif random_num1 == 4: postdata['selected_pet'] = 'xweetok';
                    elif random_num1 == 5: postdata['selected_pet'] = 'aisha';
                    elif random_num1 == 6: postdata['selected_pet'] = 'peophin';
                    elif random_num1 == 7: postdata['selected_pet'] = 'vandagyre';
                    else: postdata['selected_pet'] = 'moehog';
                    if random_num2 == 1: postdata['selected_pet_colour'] = 'red';
                    elif random_num2 == 2: postdata['selected_pet_colour'] = 'yellow';
                    elif random_num2 == 3: postdata['selected_pet_colour'] = 'green';
                    else: postdata['selected_pet_colour'] = 'blue';
                    if random_num3 == 1: postdata['gender'] = 'female';
                    else: postdata['gender'] = 'male';

                    postdata['neopet_name'] = pet_name
                    postdata['terrain'] = random.randrange(1, 6)
                    postdata['likes'] = random.randrange(1, 6)
                    postdata['meetothers'] = random.randrange(1, 6)
                    postdata['pet_stats_set'] = random.randrange(1, 4)

                    html = self.post('/reg/process_page6.phtml', postdata, readable = True)
                    html = self.get('/bank.phtml')
                    if html.find('<b>The National Neopian Bank</b>') != -1:
                        return 3
                    else:
                        return 4
                elif html.find('<title>Accept Privacy Policy and Terms of Use</title>') != -1:
                    return 4
                else:
                    return 4

            elif html.find("var species_arr") != -1:
                postdata = {}
                pet_name = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
                random_num1 = random.randrange(1, 9)
                random_num2 = random.randrange(1, 5)
                random_num3 = random.randrange(1, 3)

                if random_num1 == 1: postdata['selected_pet'] = 'zafara';
                elif random_num1 == 2: postdata['selected_pet'] = 'wocky';
                elif random_num1 == 3: postdata['selected_pet'] = 'korbat';
                elif random_num1 == 4: postdata['selected_pet'] = 'xweetok';
                elif random_num1 == 5: postdata['selected_pet'] = 'aisha';
                elif random_num1 == 6: postdata['selected_pet'] = 'peophin';
                elif random_num1 == 7: postdata['selected_pet'] = 'vandagyre';
                else: postdata['selected_pet'] = 'moehog';
                if random_num2 == 1: postdata['selected_pet_colour'] = 'red';
                elif random_num2 == 2: postdata['selected_pet_colour'] = 'yellow';
                elif random_num2 == 3: postdata['selected_pet_colour'] = 'green';
                else: postdata['selected_pet_colour'] = 'blue';
                if random_num3 == 1: postdata['gender'] = 'female';
                else: postdata['gender'] = 'male';

                postdata['neopet_name'] = pet_name
                postdata['terrain'] = random.randrange(1, 6)
                postdata['likes'] = random.randrange(1, 6)
                postdata['meetothers'] = random.randrange(1, 6)
                postdata['pet_stats_set'] = random.randrange(1, 4)

                html = self.post('/reg/process_page6.phtml', postdata, readable = True)
                html = self.get('/bank.phtml')
                if html.find('<b>The National Neopian Bank</b>') != -1:
                    return 3
                else:
                    return 4
            elif html.find("http://images.neopets.com/images/neo_cop.gif") != -1:
                return 3
            elif html.find("<b>Players Online:</b>") != -1:
                return 3
            elif html.find("please verify your birthday:") != -1:
                return 5
            else:
                return 4

        elif html.find('<title>Accept Privacy Policy and Terms of Use</title>') != -1:
            postdata = {}
            pos1 = html.find("<input type='hidden' name='destination' value=") + 47
            pos2 = html.find('"' , pos1)
            destination = html[pos1:pos2]
            postdata['destination'] = destination
            postdata['accept'] = '1'

            if html.find("Enter Your Email Address") != -1 or html.find("Enter Your Parent's Email Address") != -1:
                random_num = random.randrange(1, 4)
                if random_num == 1: ending = "@gmail.com";
                elif random_num == 2: ending = "@hotmail.com";
                else: ending = "@outlook.com";
                email = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(12)) + ending
                postdata['email1'] = email
                postdata['email2'] = email
            if html.find("<select name='country' id='countrySelect'") != -1: postdata['country'] = 'US';
            if html.find("<select name='state' id='stateSelect'") != -1: postdata['state'] = 'CA';
            html = self.post('/accept_terms.phtml', postdata, readable = True)

            if html.find("<b>Players Online:</b>") != -1:
                return 3
            elif html.find("http://images.neopets.com/images/neo_cop.gif") != -1:
                return 3
            elif html.find("var species_arr") != -1:
                postdata = {}
                pet_name = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
                random_num1 = random.randrange(1, 9)
                random_num2 = random.randrange(1, 5)
                random_num3 = random.randrange(1, 3)

                if random_num1 == 1: postdata['selected_pet'] = 'zafara';
                elif random_num1 == 2: postdata['selected_pet'] = 'wocky';
                elif random_num1 == 3: postdata['selected_pet'] = 'korbat';
                elif random_num1 == 4: postdata['selected_pet'] = 'xweetok';
                elif random_num1 == 5: postdata['selected_pet'] = 'aisha';
                elif random_num1 == 6: postdata['selected_pet'] = 'peophin';
                elif random_num1 == 7: postdata['selected_pet'] = 'vandagyre';
                else: postdata['selected_pet'] = 'moehog';
                if random_num2 == 1: postdata['selected_pet_colour'] = 'red';
                elif random_num2 == 2: postdata['selected_pet_colour'] = 'yellow';
                elif random_num2 == 3: postdata['selected_pet_colour'] = 'green';
                else: postdata['selected_pet_colour'] = 'blue';
                if random_num3 == 1: postdata['gender'] = 'female';
                else: postdata['gender'] = 'male';

                postdata['neopet_name'] = pet_name
                postdata['terrain'] = random.randrange(1, 6)
                postdata['likes'] = random.randrange(1, 6)
                postdata['meetothers'] = random.randrange(1, 6)
                postdata['pet_stats_set'] = random.randrange(1, 4)

                self.post('/reg/process_page6.phtml', postdata, readable = True)
                html = self.get('/bank.phtml')
                if html.find('<b>The National Neopian Bank</b>') != -1:
                    return 3
                else:
                    return 4
            elif html.find('<title>Accept Privacy Policy and Terms of Use</title>') != -1:
                return 4
            else:
                return 4

        elif html.find("var species_arr") != -1:
            postdata = {}
            pet_name = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
            random_num1 = random.randrange(1, 9)
            random_num2 = random.randrange(1, 5)
            random_num3 = random.randrange(1, 3)

            if random_num1 == 1: postdata['selected_pet'] = 'zafara';
            elif random_num1 == 2: postdata['selected_pet'] = 'wocky';
            elif random_num1 == 3: postdata['selected_pet'] = 'korbat';
            elif random_num1 == 4: postdata['selected_pet'] = 'xweetok';
            elif random_num1 == 5: postdata['selected_pet'] = 'aisha';
            elif random_num1 == 6: postdata['selected_pet'] = 'peophin';
            elif random_num1 == 7: postdata['selected_pet'] = 'vandagyre';
            else: postdata['selected_pet'] = 'moehog';
            if random_num2 == 1: postdata['selected_pet_colour'] = 'red';
            elif random_num2 == 2: postdata['selected_pet_colour'] = 'yellow';
            elif random_num2 == 3: postdata['selected_pet_colour'] = 'green';
            else: postdata['selected_pet_colour'] = 'blue';
            if random_num3 == 1: postdata['gender'] = 'female';
            else: postdata['gender'] = 'male';

            postdata['neopet_name'] = pet_name
            postdata['terrain'] = random.randrange(1, 6)
            postdata['likes'] = random.randrange(1, 6)
            postdata['meetothers'] = random.randrange(1, 6)
            postdata['pet_stats_set'] = random.randrange(1, 4)

            self.post('/reg/process_page6.phtml', postdata, readable = True)
            html = self.get('/bank.phtml')
            if html.find('<b>The National Neopian Bank</b>') != -1:
                return 3
            else:
                return 4
        else:
            return 4

    def readable(self, data):
        """ Not sure what this does, it was here originally """

        if 'gzip' in str(data.info()):
            return gzip.GzipFile(fileobj=StringIO.StringIO(data.read())).read()
        else:
            return data.read()
