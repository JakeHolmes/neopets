class Userlookup(object):

    def __init__(self, acc, username):
        self.acc = acc
        self.username = username

    def CheckUserlookup(username):
        html = acc.get("http://www.neopets.com/userlookup.phtml?user=" + self.username)
        print html


    def GetAvatars(self):
        pass