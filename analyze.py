import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates
from datetime import datetime
import math
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import json
from unidecode import unidecode

class Chat:
    def __init__(self, name):
        self.name = name
        self.senders = []
    def add(self, sender):
        self.senders.append(sender)

class Message:
    def __init__(self, contents, timestamp):
        self.contents = contents
        self.timestamp = timestamp
        self.datetime = datetime.fromtimestamp(timestamp // 1000.0)

class Sender:
    def __init__(self, name):
        self.name = name
        self.messages = []
        self.participated = -1
    
    def add_fb_message(self, message):
        msg = Message(message["content"], message["timestamp_ms"])
        self.messages.append(msg)

    def sort_messages(self):
        self.messages = sorted(self.messages, key=lambda x: x.timestamp, reverse=True)

    def merge(self, sender_b):
        if self.name == sender_b.name:
            self.messages = sender_b.messages
            self.participated += sender_b.participated
        else:
            raise ValueError()

# number of messages to consider a chat worthy of parsing
CONVERSATION_THRESHOLD = 20

# list of all conversations
chats = []

# amount of group chats each user participated in with the host
part_freq = {}

# amount of messages sent by each individual
message_freq = {}

for folder in os.listdir('inbox'):
    if not folder.startswith('.'):

        current_chat = Chat("tmp")

        # list of all messages in the chat
        users = {}
        # is this folder for a group chat
        is_group_parent = False

        for data in os.listdir('inbox/' + folder):
            if data.endswith('.json'):
                with open('inbox/' + folder + '/' + data, encoding='utf-8') as f:

                    # load in JSON data from each file
                    json_data = json.load(f)

                    # name of the conversation
                    current_chat.name = json_data['title']

                    # list of messages for this chat
                    messages = json_data['messages']

                    # list of participants (by full name) for this chat
                    participants = json_data['participants']

                    # determines if this iteration is a group chat by seeing how many participants it has
                    # NOTE: this does NOT account for group chats where individuals have been removed leaving 2 others
                    is_group = not len(participants) < 3

                    for participant in participants:
                        current = participant['name']
                        try:
                            part_freq[current] += 1
                        except:
                            part_freq[current] = 0
                    
                    if not is_group and len(messages) > CONVERSATION_THRESHOLD:
                        for message in messages:
                            if message['type'] == 'Generic':
                                current = message['sender_name']
                                try:
                                    message_freq[current] += 1
                                    users[current].append(message)
                                except:
                                    message_freq[current] = 1
                                    users[current] = []
                                    users[current].append(message)
                    is_group_parent = is_group
        if len(users) > 0:
            # print("\u001b[37;1m" + current_chat.name + "\u001b[0m")
            for key in users:
                current_sender = Sender(key)
                for message in users[key]:
                    try:
                        current_sender.add_fb_message(message)
                    except:
                        pass
                current_sender.sort_messages()
                current_chat.add(current_sender)
            # for sender in current_chat.senders:
            #     print(sender.name)
            chats.append(current_chat)

frequent_participants = sorted(part_freq.items(), key=lambda x: x[1], reverse=True)

while True:
    UINDEX = -1

    query_term = input("\u001b[37;1mSearch for a user/conversation (or type '!q' to exit):\u001b[0m\n")

    if query_term == '!q':
        break

    for i in range(len(chats)):
        for sender in chats[i].senders:
            if query_term.lower() in sender.name.lower():
                UINDEX = i

    if UINDEX != -1:

        main_speaker_index = 0
        other_speaker_index = 1

        if frequent_participants[0][0] == chats[UINDEX].senders[main_speaker_index].name:
            main_speaker_index = 1
            other_speaker_index = 0

        # Percentage of chat

        speaker_one = chats[UINDEX].senders[main_speaker_index].name
        total_messages = (len(chats[UINDEX].senders[main_speaker_index].messages) + len(chats[UINDEX].senders[other_speaker_index].messages))
        speaker_one_percentage = len(chats[UINDEX].senders[main_speaker_index].messages)/total_messages * 100

        print()
        print("\u001b[37;1m{} sent {:.2f}% of {} messages\u001b[0m".format(speaker_one, speaker_one_percentage, total_messages))

        # Messages against Time plot

        time_one = []
        time_two = []

        for message in chats[UINDEX].senders[main_speaker_index].messages:
            time_one.append(message.datetime)
        for message in chats[UINDEX].senders[other_speaker_index].messages:
            time_two.append(message.datetime)

        first = time_one[len(time_one) - 1]
        last = time_one[0]

        bins = (last.year - first.year) * 12
        if bins < 12:
            bins = 12

        fig, ax = plt.subplots(1,1)

        ax.hist(time_one, bins=bins, color='r', alpha=0.6, range=(first, last), label=chats[UINDEX].senders[main_speaker_index].name)
        ax.hist(time_two, bins=bins, color='y', alpha=0.6, range=(first, last), label=chats[UINDEX].senders[other_speaker_index].name)

        ax.tick_params(labelsize=8)
        ax.set_ylabel("Messages")
        ax.set_xlabel("Time")
        plt.xticks(rotation=45)
        ax.legend()

        plt.show()

        fdist_list = []

        stop_words = set(stopwords.words('english'))
        stop_words.update(['like','u','ur','im','also','gonna','cuz','really','rly','actually','tho','y','ye','yea','yeah','yee','no','na','nah','nahh','would','should','bc','dont','go','get','much','kinda','want', 'one','r','c','cool','think','good','w','good','got','thats','could','pretty','1','2','3','4','5','6','7','8','9','0','know','right','lot','lol','thought',])
        stop_words.update(['itas','iam','donat','thatas','iall','didnat','canat','havenat'])

        for sender in chats[UINDEX].senders:
            
            all_messages = ""

            for msg in sender.messages:
                all_messages += msg.contents

            all_messages = unidecode(all_messages.lower())

            tokenizer = RegexpTokenizer(r'\w+')

            tokens = tokenizer.tokenize(all_messages)

            filtered_tokens = [w for w in tokens if not w in stop_words] 

            text = nltk.Text(filtered_tokens)
            fdist = nltk.FreqDist(text)
            print(sender.name + ": ", fdist.most_common(10))

        print()
    else:
        print("\nNo Results :(\n")
    
        
# def clean_content(split_list):
#     for item in split_list:
#         if ()

# previous_amount = -1

# for user in frequent_participants:
#     if user[1] > 0:
#         if user[1] == previous_amount:
#             print(user[0], end=", ")
#         else:
#             print("\n{}\t{}".format(user[1],user[0]), end=", ")
#             previous_amount = user[1]

# frequent_senders = sorted(message_freq.items(), key=lambda x: x[1], reverse=True)

# for user in frequent_senders:
#     if user[1] > 1:
#         print("{}\t{}".format(user[1],user[0]))