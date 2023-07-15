import os
import sys
import datetime

scriptpath = "../../"
sys.path.append(os.path.abspath(scriptpath))
import utils.dialog_event as de
remote_assistants = ["test", "test1","test2"]


class Assistant:
    def __init__(self):
        self.input_message = ""
        self.output_message = ""
        print("starting")
	
    def invoke_assistant(self,transcription):
        print(transcription)
        # convert input to OVON
        self.input_message = self.convert_to_dialog_event(transcription)
        print(self.input_message)
        # handle locally?
        if self.handle_locally(transcription):
            final_result = self.decide_what_to_say(transcription)
        # if not handle locally:
        else:
            remote_assistant = self.identify_assistant(transcription)
            result = self.send_message_to_assistant(remote_assistant, self.input_message)
        # log result
        return("I heard" + transcription)

    # figure out if the local assistant can help	
    def handle_locally(self,transcription):
        return(True)
    
# if it can't be handled locally, find a remote assistant that can help
    def identify_assistant(self,transcription):
        return(remote_assistants[0])

    def send_message_to_assistant(self,remote_assistant,input_message):
        return("all done, thanks, " + remote_assistant)

    def decide_what_to_say(self,transcription):
        return(transcription)
    
    def convert_to_dialog_event(self,transcription):
        d=de.DialogEvent()
        d.id='user-utterance-45'
        d.speaker_id="user1234"
        d.previous_id='user-utterance-44'
        d.add_span(de.Span(start_time=datetime.datetime.now().isoformat(),end_offset_msec=1045))

        #   Add an Audio Feature
        f1=de.AudioWavFileFeature()
        d.add_feature('user-request-audio',f1)
        f1.add_token(value_url='http://localhost:8080/ab78h50ef.wav')

        #Now add a text feature
        f2=de.TextFeature(lang='en',encoding='utf-8')
        d.add_feature('user-request-text',f2)
        f2.add_token(value= transcription,confidence=0.99,start_offset_msec=8790,end_offset_msec=8845,links=["$.user-request-audio.tokens[0].value-url"])
   
        print(f'dialog packet: {d.packet}')

        #Now save the dialog event to YML and JSON
        #with open("../sample-json/utterance0.json", "w") as file: d.dump_json(file)
        #with open("../sample-yaml/utterance0.yml", "w")  as file: d.dump_yml(file)
        return(d.packet)
    
    def parse_dialog_event(self,event):
        #Now interrogate this object
        text1=d.get_feature('user-request-text').get_token().value
        confidence1=d.get_feature('user-request-text').get_token().confidence
        t2=d.get_feature('user-request-text').get_token(1)
        l1=d.get_feature('user-request-text').get_token().linked_values(d)

        #Look at some of the variables
        print(f'text packet: {f2.packet}')
        print(f'text1: {text1} confidence1: {confidence1}')
        print(f'text2: {t2.value} confidence1: {t2.confidence}')
        print(f'l1: {l1}')
    
    def get_input_message(self):
        print("here's the input" + str(self.input_message))
        return(self.input_message)
    
    def get_output_message(self):
        return(self.output_message)
        
        