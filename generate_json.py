try:
    import html.parser
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser

import collections
import os
# import urllib2
import json

card_index = {'A': 9, 'X': 8}
for i in range(2, 11):
    card_index[str(i)] = i - 2


def basic_strategy(name):
    with open("./basic/%s.json" % name) as f:
        basic = json.load(f)
        basic_strat = collections.namedtuple("Strategy", basic.keys())(*basic.values())
        return basic_strat


class Strategy:
    def __init__(self, filename):
        name = filename[0:filename.rindex('.')]
        name = "_" + name + "_"
        name = name.lower()
        decks, h17, das, sur, rsa, spn, extras, doubles, method = 6, True, True, 'None', True, 4, '', 'any', ''
        deck_str = {
            1: "_1d_",
            2: "_2d_",
            6: "_2d_"}

        for k, v in deck_str.items():
            if v in name:
                decks = k
                name = name.replace(v, '_')
                break

        h17_str = {
            True: "_h17_",
            False: "_s17_"
        }
        for k, v in h17_str.items():
            if v in name:
                h17 = k
                name = name.replace(v, '_')
                break

        das_str = {
            True: "_das_",
            False: "_nodas_"
        }
        for k, v in das_str.items():
            if v in name:
                das = k
                name = name.replace(v, '_')
                break

        sur_str = {
            True: "_esur_",
            True: "_lsur_",
            False: "_s17_"
        }
        for k, v in sur_str.items():
            if v in name:
                sur = k
                name = name.replace(v, '_')
                break

        method_str = '_method'
        if method_str in name:
            method = name[name.indexof(method_str) + len(method_str):]
            method = method[0:method.indexof('_')]
            name = name.replace(method_str + method, '_')

        double_str = '_double'
        if double_str in name:
            doubles = name[name.indexof(double_str) + len(double_str):]
            doubles = doubles[0:doubles.indexof('_')]
            name = name.replace(double_str + doubles, '_')

        extras = name

        basic_filename = "basic_strategy_%(decks)dd_%(h17)s_%(das)s" % {'decks': decks, 'h17': 'h17' if h17 else 's17',
                                                                        'das': 'das' if das else 'nodas'}
        s = basic_strategy(basic_filename)
        self.hard = s.hard
        self.hard = s.hard
        self.soft = s.soft
        self.split = s.split
        self.hard_double = s.hard_double
        self.soft_double = s.soft_double
        self.insurance = s.insurance
        self.decks, self.hit_soft_17, self.DaS, self.surrender_allowed, self.rsa, self.spn, self.extra, self.doubles, self.method = decks, h17, das, sur, rsa, spn, extras, doubles, method


    def hardHitCount(self, dealer, you, count):
        assert dealer in card_index, "Unable to find " + dealer + " in " + str(card_index)
        dealer_index = card_index[dealer]
        assert you >= 12 and you <= 21
        self.hard[you - 12][dealer_index] = str(count)

    def softHitCount(self, dealer, you, count):
        assert dealer in card_index
        dealer_index = card_index[dealer]
        assert you >= 13 and you <= 21
        self.soft[you - 13][dealer_index] = str(count)

    def hardDouble(self, dealer, you, count):
        assert dealer in card_index
        dealer_index = card_index[dealer]
        assert you >= 5 and you <= 11
        self.hard_double[you - 5][dealer_index] = str(count)

    def softDouble(self, dealer, you, count):
        assert dealer in card_index
        dealer_index = card_index[dealer]
        assert you >= 13 and you <= 21
        self.soft_double[you - 13][dealer_index] = str(count)

    def splitIndex(self, dealer, you, count):
        assert dealer in card_index
        dealer_index = card_index[dealer]
        you_index = card_index[you]
        assert you_index >= 0 and you_index <= 11, "You are " + str(you_index)
        self.split[you_index][dealer_index] = str(count)

    def insureIndex(self, count):
        self.insurance = count


class MyHTMLParser(HTMLParser):
    def __init__(self, strat):
        HTMLParser.__init__(self)
        self.current_text_tag = ""
        self.strat = strat

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        if tag == "p":
            self.current_text_tag = ""

    def handle_endtag(self, tag):
        # print("Encountered an end tag :", tag)
        if tag == "p":
            self.processText(self.current_text_tag.strip())
        self.current_text_tag = ""

    def handle_data(self, data):
        # print("Encountered some data  :", data)
        self.current_text_tag += data

    def handle_charref(self, name):
        pass
        # print("Encountered some charref  :", name)

    def handle_entityref(self, name):
        # print("Encountered some entity  :", name)
        self.current_text_tag += str(self.unescape("&" + name + ";").encode('ascii', 'ignore'))

    def processText(self, text):
        text = text.strip()
        if text == '':
            return
        if text in ["", "Index", "Stand", "Hit", "Diff", "Double Down", "No Double Down", "Split",
                    "No Split", "Insure", "Don't Insure", '', b'', "b''"]:
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
            action = parts[3].strip()
            condition = parts[4]
            count = parts[5]
            print("Do " + action + " with " + hard_hand + " against " + dealer_hand + " with "
                                                                                      "count " +
                  condition + " " + count)
            if action == "Hit":
                self.strat.hardHitCount(dealer_hand, int(hard_hand), condition + " " + count)
            return
        if text.startswith("Soft Hit/Stand Table - "):
            text = text[len("Soft Hit/Stand Table - "):]
            parts = text.split(" ")
            hard_hand = parts[0]
            assert (parts[1] == "vs.")
            dealer_hand = parts[2].strip(":")
            action = parts[3].strip()
            if (len(parts) == 4):
                condition = ">"
                count = "-inf"
            else:
                condition = parts[4].strip()
                count = parts[5].strip()
            print("Do " + action + " with " + hard_hand + " against " + dealer_hand + " with "
                                                                                      "count " +
                  condition + " " + count)
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
                condition = parts[4].strip()
                count = parts[5]
            if action == "No":
                action = "DD"
                count = "inf"
                condition = ">="
            print("Do " + action + " with " + hard_hand + " against " + dealer_hand + " with "
                                                                                      "count " +
                  condition + " " + count)
            count = count.strip()
            condition = condition.strip()
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
            count = count.strip()
            condition = condition.strip()
            print("Do " + action + " with " + hard_hand + " against " + dealer_hand + " with "
                                                                                      "count " +
                  condition + " " + count)

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
            count = count.strip()
            condition = condition.strip()
            print("Do " + action + " with " + hard_hand + " against " + dealer_hand + " with "
                                                                                      "count " +
                  condition + " " + count)
            if count != "inf":
                hard_value = hard_hand[0]
                self.strat.splitIndex(dealer_hand, hard_value, condition + " " + count)
            return
        if text.startswith("Insurance -  vs. "):
            s = text.index("Insurance -  vs. ")
            text = text[s + len("Insurance -  vs. "):]
            text = text[text.index(" >= ") + len(" >= "):]
            count_to_insure = int(text)
            print("Insure >= " + str(count_to_insure))
            self.strat.insureIndex(count_to_insure)
            return

        raise Exception("Unknown text " + text)


# def load_file(f, strat):
# contents = urllib2.urlopen(f)
#     html = contents.read()
#     MyHTMLParser(strat).feed(html)


# togen = {
#     "6d_hilow_s17_75pen_ra" : "basic_strategy_6d_s17",
#     "1d_ao2_d10_s17_6rd_ra" : "basic_strategy_1d_s17",
#     "ao2_2d_ra_dany_s17" : "basic_strategy_2d_s17",
# }

dir_to_list = './indexgen'
for name in os.listdir(dir_to_list):
    print("Parsing " + name)
    strat = Strategy(name)

    strat.strategy = name

    with open(dir_to_list + '/' + name) as f:
        html = f.read()
        print("Looking at " + name)
        MyHTMLParser(strat).feed(html)

    contents = json.dumps(strat.__dict__, sort_keys=True)
    with open("./json/%s.json" % name, 'w') as f:
        json.dump(strat.__dict__, f)
