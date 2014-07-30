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
        decks, h17, das, sur, rsa, spn, extras, doubles, counting_method = 6, True, True, 'None', True, 4, '', 'any', ''
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
            'late': "_surlate_",
            'early': "_surearly_",
        }
        for k, v in sur_str.items():
            if v in name:
                sur = k
                name = name.replace(v, '_')
                break

        method_str = '_method'
        if method_str in name:
            counting_method = name[name.index(method_str) + len(method_str):]
            counting_method = counting_method[0:counting_method.index('_')]
            name = name.replace(method_str + counting_method, '_')

        double_str = '_double'
        if double_str in name:
            doubles = name[name.index(double_str) + len(double_str):]
            doubles = doubles[0:doubles.index('_')]
            name = name.replace(double_str + doubles, '_')

        extras = name

        basic_filename = "basic_strategy_%(decks)dd_%(h17)s_%(das)s%(sur)s" % {'decks': decks, 'h17': 'h17' if h17 else 's17',
                                                                        'das': 'das' if das else 'nodas',
                                                                        'sur': "_sur" + sur if sur != 'None' else ''}
        s = basic_strategy(basic_filename)
        self.hard = s.hard
        self.hard = s.hard
        self.soft = s.soft
        self.split = s.split
        self.hard_double = s.hard_double
        self.soft_double = s.soft_double
        self.insurance = s.insurance
        if sur != 'None':
            self.surrender_split = s.surrender_split
            self.surrender_hard = s.surrender_hard
        self.decks, self.hit_soft_17, self.DaS, self.surrender_allowed, self.rsa, self.spn, self.extra, self.doubles, self.counting_method = decks, h17, das, sur, rsa, spn, extras, doubles, counting_method


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

    def surrenderSplitIndex(self, dealer, you, count):
        assert dealer in card_index
        dealer_index = card_index[dealer]
        you_index = card_index[str(you)]
        assert you_index >= 5 and you_index <= 6, "You are " + str(you_index)
        self.surrender_split[you_index - 5][dealer_index - 5] = str(count)

    def surrenderHardIndex(self, dealer, you, count):
        assert dealer in card_index, "Unable to find " + dealer + " in " + str(card_index) + " of type " + str(type(dealer))
        dealer_index = card_index[dealer]
        assert you >= 12 and you <= 17
        self.surrender_hard[you - 12][dealer_index - 5] = str(count)

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
            try:
                no_exception = False
                self.processText(self.current_text_tag.strip())
                no_exception = True
            finally:
                if not no_exception:
                    print ("Got exception for " + self.current_text_tag.strip())
        self.current_text_tag = ""

    def handle_data(self, data):
        # print("Encountered some data  :", data)
        self.current_text_tag += data

    def handle_charref(self, name):
        pass
        # print("Encountered some charref  :", name)

    def handle_entityref(self, name):
        # print("Encountered some entity  :", name)
        # s = str(self.unescape("&" + name + ";").encode('ascii', 'strict'))
        s = self.unescape("&" + name + ";")
        assert len(s) != 0
        self.current_text_tag += s

    def processText(self, text):
        text = text.strip()
        if text == '':
            return
        if text in ["", "Index", "Stand", "Hit", "Diff", "Double Down", "No Double Down", "Split",
                    "No Split", "Insure", "Don't Insure", '', b'', "b''", 'Surrender', 'Play']:
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
            if len(parts) == 4:
                if action == 'Stand':
                    self.strat.hardHitCount(dealer_hand, int(hard_hand), 'S')
                else:
                    assert action == 'Hit'
                    self.strat.hardHitCount(dealer_hand, int(hard_hand), 'H')
                return

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
                action = condition + ' ' + count
                if count == '-inf':
                    action = 'H'
                self.strat.softHitCount(dealer_hand, int(hard_value), action)
            return
        if text.startswith("Hard Double Down - "):
            text = text[len("Hard Double Down - "):]
            parts = text.split(" ")
            hard_hand = parts[0]
            assert (parts[1] == "vs.")
            dealer_hand = parts[2].strip(":")
            parts = [p.strip() for p in parts]
            action = parts[3]
            if len(parts) == 5 and parts[3] == 'Double' and parts[4] == 'Down':
                condition = ">"
                count = "-inf"
            elif (len(parts) == 4):
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
            if (len(parts) == 4) or (len(parts) == 5 and parts[3] == 'Double' and parts[4] == 'Down'):
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
            hard_value = hard_hand[0]
            assert (parts[1] == "vs.")
            dealer_hand = parts[2].strip(":")
            action = parts[3]
            if len(parts) == 4:
                if action == 'Split':
                    self.strat.splitIndex(dealer_hand, hard_value, 'P')
                else:
                    assert False, "Wha?"
                return
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
                self.strat.splitIndex(dealer_hand, hard_value, condition + " " + count)
            return
        text = text.replace('Insurance -  vs', 'Insurance - vs')
        if text.startswith("Insurance - vs. "):
            s = text.index("Insurance - vs. ")
            text = text[s + len("Insurance - vs. "):]
            text = text[text.index(" >= ") + len(" >= "):]
            count_to_insure = int(text)
            print("Insure >= " + str(count_to_insure))
            self.strat.insureIndex(count_to_insure)
            return

        if text.startswith("Surrender Table - "):
            text = text[len("Surrender Table - "):]
            parts = text.split(" ")
            action = 'Surrender'
            hand = parts[0]
            assert (parts[1] == 'vs.')
            dealer_hand = parts[2].replace(":", "")
            if parts[3] == 'Play':
                #Do play stuff
                condition = ">="
                count = "-inf"
                pass
            else:
                assert(len(parts) == 6)
                assert (parts[3] == 'Surrender')
                condition = parts[4]
                count = parts[5]
                #Surrender?
            print("Do " + action + " with " + hand + " against " + dealer_hand + " with " + "count " + condition + " " + count)
            if count != "-inf":
                if ',' in hand:
                    card = int(hand[0])
                    self.strat.surrenderSplitIndex(dealer_hand, card, condition + " " + count)
                else:
                    hand = int(hand)
                    self.strat.surrenderHardIndex(dealer_hand, hand, condition + " " + count)
            return


        raise Exception("for %s, Unknown text: %s " %(self.strat.counting_method, text))


dir_to_list = './indexgen'
directory_to_make = './json'
try:
    os.stat(directory_to_make)
except:
    os.mkdir(directory_to_make)

load_json = ""
for name in os.listdir(dir_to_list):
    print("Parsing " + name)
    strat = Strategy(name)

    strat.strategy = name

    with open(dir_to_list + '/' + name) as f:
        html = f.read()
        print("Looking at " + name)
        MyHTMLParser(strat).feed(html)

    base_name = name[0:name.index('.')]
    load_json += "add_chart_row('%s');\n" % base_name
    with open("./json/%s.json" % base_name, 'w') as f:
        json.dump(strat.__dict__, f, sort_keys=True)

with open("./show_each_deck.js", 'w') as f:
    f.write(load_json)