import os
import numpy as np
import pandas as pd
import matplotlib as plt
from datetime import datetime
import nltk
import json

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

    def merge(self, sender_b):
        if self.name == sender_b.name:
            self.messages = sender_b.messages
            self.participated += sender_b.participated
        else:
            raise ValueError()

# Number of messages to consider a chat worthy of parsing
CONVERSATION_THRESHOLD = 20

# Amount of group chats each user participated in with the host
part_freq = {}

# Amount of messages sent by each individual
message_freq = {}

for folder in os.listdir('inbox'):
    if not folder.startswith('.'):

        # total messages in this chat
        messages_total = 0
        # is this folder for a group chat
        is_group_parent = False

        for data in os.listdir('inbox/' + folder):
            if data.endswith('.json'):
                with open('inbox/' + folder + '/' + data) as f:

                    # load in JSON data from each file
                    json_data = json.load(f)

                    # name of the conversation
                    chat_name = json_data['title']

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
                                except:
                                    message_freq[current] = 1
                                messages_total += 1
                    is_group_parent = is_group
        if messages_total > 0:
            print(folder, messages_total)

frequent_participants = sorted(part_freq.items(), key=lambda x: x[1], reverse=True)

frequent_senders = sorted(message_freq.items(), key=lambda x: x[1], reverse=True)


# previous_amount = -1

# for user in frequent_participants:
#     if user[1] > 0:
#         if user[1] == previous_amount:
#             print(user[0], end=", ")
#         else:
#             print("\n{}\t{}".format(user[1],user[0]), end=", ")
#             previous_amount = user[1]

for user in frequent_senders:
    if user[1] > 1:
        print("{}\t{}".format(user[1],user[0]))