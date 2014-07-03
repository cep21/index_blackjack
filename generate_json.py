from HTMLParser import HTMLParser
import collections
import urllib2
import json
import sys

card_index = {'A': 9, 'X': 8}
for i in range(2, 11):
    card_index[str(i)] = i-2

class Strategy:
    def __init__(self, to_copy):
        self.decks = to_copy.decks
        self.DaS = to_copy.DaS
        self.surrender_allowed = to_copy.surrender_allowed
        self.hit_soft_17 = to_copy.hit_soft_17
        self.hard = to_copy.hard
        self.soft = to_copy.soft
        self.split = to_copy.split
        self.hard_double = to_copy.hard_double
        self.soft_double = to_copy.soft_double
        self.insurance = to_copy.insurance

    def hardHitCount(self, dealer, you, count):
        assert dealer in card_index, "Unable to find " + dealer + " in " + str(card_index)
        dealer_index = card_index[dealer]
        assert you >= 12 and you <= 21
        self.hard[you-12][dealer_index] = str(count)

    def softHitCount(self, dealer, you, count):
        assert dealer in card_index
        dealer_index = card_index[dealer]
        assert you >= 13 and you <= 21
        self.soft[you-13][dealer_index] = str(count)

    def hardDouble(self, dealer, you, count):
        assert dealer in card_index
        dealer_index = card_index[dealer]
        assert you >= 5 and you <= 11
        self.hard_double[you-5][dealer_index] = str(count)

    def softDouble(self, dealer, you, count):
        assert dealer in card_index
        dealer_index = card_index[dealer]
        assert you >= 13 and you <= 21
        self.soft_double[you-13][dealer_index] = str(count)

    def splitIndex(self, dealer, you, count):
        assert dealer in card_index
        dealer_index = card_index[dealer]
        you_index = card_index[you]
        assert you_index >= 0 and you_index <= 11, "You are " + str(you_index)
        self.split[you_index-2][dealer_index] = str(count)


class MyHTMLParser(HTMLParser):
    def __init__(self, strat):
        HTMLParser.__init__(self)
        self.current_text_tag = ""
        self.strat = strat

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
        if text in ["", "Index", "Stand", "Hit", "Diff", "Double Down", "No Double Down", "Split",
                    "No Split", "Insure", "Don't Insure"]:
            return
        try:
            float(text)
            return
        except ValueError:
            pass
        if ", 2014, " in text:
            # print "A date.  That's ok"
            return
        if text.startswith("Hard Hit/Stand Table - "):
            text = text[len("Hard Hit/Stand Table - "):]
            parts = text.split(" ")
            hard_hand = parts[0]
            assert (parts[1] == "vs.")
            dealer_hand = parts[2].strip(":")
            action = parts[3]
            condition = parts[4]
            count = parts[5]
            print "Do " + action + " with " + hard_hand + " against " + dealer_hand + " with " \
                                                                                      "count " + \
                  condition + " " + count
            if action == "Hit":
                self.strat.hardHitCount(dealer_hand, int(hard_hand), condition + " " + count)
            return
        if text.startswith("Soft Hit/Stand Table - "):
            text = text[len("Soft Hit/Stand Table - "):]
            parts = text.split(" ")
            hard_hand = parts[0]
            assert (parts[1] == "vs.")
            dealer_hand = parts[2].strip(":")
            action = parts[3]
            if (len(parts) == 4):
                condition = ">"
                count = "-inf"
            else:
                condition = parts[4]
                count = parts[5]
            print "Do " + action + " with " + hard_hand + " against " + dealer_hand + " with " \
                                                                                      "count " + \
                  condition + " " + count
            if action == "Hit":
                hard_value = int(hard_hand[1]) + 11
                self.strat.softHitCount(dealer_hand, int(hard_value), condition + " " + count)
            return
        if text.startswith("Hard Double Down - "):
            text = text[len("Hard Double Down - "):]
            parts = text.split(" ")
            hard_hand = parts[0]
            assert (parts[1] == "vs.")
            dealer_hand = parts[2].strip(":")
            action = parts[3]
            if (len(parts) == 4):
                condition = ">"
                count = "-inf"
            else:
                condition = parts[4]
                count = parts[5]
            if action == "No":
                action = "DD"
                count = "inf"
                condition = ">="
            print "Do " + action + " with " + hard_hand + " against " + dealer_hand + " with " \
                                                                                      "count " + \
                  condition + " " + count
            if action == "DD" and count != "inf":
                self.strat.hardDouble(dealer_hand, int(hard_hand), condition + " " + count)
            return
        if text.startswith("Soft Double Down - "):
            text = text[len("Soft Double Down - "):]
            parts = text.split(" ")
            hard_hand = parts[0]
            assert (parts[1] == "vs.")
            dealer_hand = parts[2].strip(":")
            action = parts[3]
            if (len(parts) == 4):
                condition = "<"
                count = "inf"
            else:
                condition = parts[4]
                count = parts[5]
            if action == "No":
                action = "DD"
                count = "inf"
                condition = ">="
            print "Do " + action + " with " + hard_hand + " against " + dealer_hand + " with " \
                                                                                      "count " + \
                  condition + " " + count
            if action == "DD" and count != "inf":
                hard_value = int(hard_hand[1]) + 11
                self.strat.softDouble(dealer_hand, int(hard_value), condition + " " + count)
            return
        if text.startswith("Splitting Pairs - "):
            text = text[len("Splitting Pairs - "):]
            parts = text.split(" ")
            hard_hand = parts[0]
            assert (parts[1] == "vs.")
            dealer_hand = parts[2].strip(":")
            action = parts[3]
            if (len(parts) == 5):
                condition = ">"
                count = "inf"
                action = "split"
            else:
                condition = parts[4]
                count = parts[5]
            print "Do " + action + " with " + hard_hand + " against " + dealer_hand + " with " \
                                                                                      "count " + \
                  condition + " " + count
            if count != "inf":
                hard_value = hard_hand[0]
                self.strat.splitIndex(dealer_hand, hard_value, condition + " " + count)
            return
        if text.startswith("Insurance -  vs. "):
            s = text.index("Insurance -  vs. ")
            text = text[s + len("Insurance -  vs. "):]
            text = text[text.index(" >= ") + len(" >= "):]
            count_to_insure = int(text)
            print "Insure >= " + str(count_to_insure)
            return

        raise Exception("Unknown text " + text)


def load_file(f, strat):
    contents = urllib2.urlopen(f)
    html = contents.read()
    MyHTMLParser(strat).feed(html)


# print "Hello"

togen = {
    "6d_hilow_s17_75pen_ra" : "basic_strategy_6d_s17"
}

for name, basic in togen.items():
    # load_file("http://cep21.net/2d_ao2_d10_nodas_h17_ra_75pen.htm")

    with open("%s.json" % basic) as f:
        basic = json.load(f)
        basic_strat = collections.namedtuple("Strategy", basic.keys())(*basic.values())
        strat = Strategy(basic_strat)

    strat.strategy = name

    load_file("http://cep21.net/%s.htm" % name, strat)

    contents = json.dumps(strat.__dict__, sort_keys=True)
    with open("%s.json" % name, 'w') as f:
        json.dump(strat.__dict__, f)
