from HTMLParser import HTMLParser
import urllib2


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.current_text_tag = ""

    def handle_starttag(self, tag, attrs):
        # print "Encountered a start tag:", tag
        if tag == "p":
            self.current_text_tag = ""

    def handle_endtag(self, tag):
        # print "Encountered an end tag :", tag
        if tag == "p":
            self.processText(self.current_text_tag.strip())
        self.current_text_tag = ""

    def handle_data(self, data):
        # print "Encountered some data  :", data
        self.current_text_tag += data

    def handle_charref(self, name):
        pass
        # print "Encountered some charref  :", name

    def handle_entityref(self, name):
        # print "Encountered some entity  :", name
        self.current_text_tag += str(self.unescape("&" + name + ";").encode('ascii', 'ignore'))

    def processText(self, text):
        if text in ["", "Index", "Stand", "Hit", "Diff", "Double Down", "No Double Down", "Split", "No Split"]:
            return
        try:
            float(text)
            return
        except ValueError:
            pass
        if ", 2014, " in text:
            print "A date.  That's ok"
            return
        if text.startswith("Hard Hit/Stand Table - "):
            text = text[len("Hard Hit/Stand Table - "):]
            parts = text.split(" ")
            hard_hand = parts[0]
            assert(parts[1] == "vs.")
            dealer_hand = parts[2].strip(":")
            action = parts[3]
            condition = parts[4]
            count = parts[5]
            print "Do " + action + " with " + hard_hand + " against " + dealer_hand + " with count " + condition + " " + count
            return
        if text.startswith("Soft Hit/Stand Table - "):
            text = text[len("Soft Hit/Stand Table - "):]
            parts = text.split(" ")
            hard_hand = parts[0]
            assert(parts[1] == "vs.")
            dealer_hand = parts[2].strip(":")
            action = parts[3]
            if (len(parts) == 4):
                condition = ">"
                count = "-inf"
            else:
                condition = parts[4]
                count = parts[5]
            print "Do " + action + " with " + hard_hand + " against " + dealer_hand + " with count " + condition + " " + count
            return
        if text.startswith("Hard Double Down - "):
            text = text[len("Hard Double Down - "):]
            parts = text.split(" ")
            hard_hand = parts[0]
            assert(parts[1] == "vs.")
            dealer_hand = parts[2].strip(":")
            action = parts[3]
            if (len(parts) == 4):
                condition = ">"
                count = "-inf"
            else:
                condition = parts[4]
                count = parts[5]
            print "Do " + action + " with " + hard_hand + " against " + dealer_hand + " with count " + condition + " " + count
            return
        if text.startswith("Soft Double Down - "):
            text = text[len("Soft Double Down - "):]
            parts = text.split(" ")
            hard_hand = parts[0]
            assert(parts[1] == "vs.")
            dealer_hand = parts[2].strip(":")
            action = parts[3]
            if (len(parts) == 4):
                condition = ">"
                count = "-inf"
            else:
                condition = parts[4]
                count = parts[5]
            print "Do " + action + " with " + hard_hand + " against " + dealer_hand + " with count " + condition + " " + count
            return
        if text.startswith("Splitting Pairs - "):
            text = text[len("Splitting Pairs - "):]
            parts = text.split(" ")
            hard_hand = parts[0]
            assert(parts[1] == "vs.")
            dealer_hand = parts[2].strip(":")
            action = parts[3]
            if (len(parts) == 5):
                condition = ">"
                count = "-inf"
            else:
                condition = parts[4]
                count = parts[5]
            print "Do " + action + " with " + hard_hand + " against " + dealer_hand + " with count " + condition + " " + count
            return
        raise Exception("Unknown text " + text)


def load_file(file):
    contents = urllib2.urlopen(file)
    html = contents.read()
    MyHTMLParser().feed(html)


print "Hello"

load_file("http://cep21.net/2d_ao2_d10_nodas_h17_ra_75pen.htm")