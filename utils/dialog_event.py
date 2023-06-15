import yaml
import json
import xml.etree.ElementTree as ET
from datetime import datetime

# standard element names
ELMNT_SPEAKER_ID='speaker-id'
ELMNT_ID='id'
ELMNT_PREV_ID='previous-id'
ELMNT_FEATURES='features'
ELMNT_MIME_TYPE='mime-type'
ELMNT_LANG='lang'
ELMNT_ENCODING='encoding'
ELMNT_TOKENS='tokens'
ELMNT_VALUE='value'
ELMNT_LINKS='links'
ELMNT_CONFIDENCE='confidence'
ELMNT_HISTORY='history'  
ELMNT_START='start-time'
ELMNT_START_OFFSET='start-offset'
ELMNT_END='end-time'
ELMNT_END_OFFSET='end-offset'
ELMNT_SPAN='span'

class DialogPacket():
    '''class variables'''
    _feature_class_map={}
    _value_class_map={}

    '''Construct a packet'''
    def __init__(self,p={}):
        #print(f'p: {p}')
        self._packet={}
        #print(f'A1: {self.packet}')

    ### Getters and Setters ###
    # property: packet
    @property
    def packet(self):
        return self._packet

    @packet.setter
    def packet(self,p):
        self._packet=p

    @classmethod
    # return the feature class for the mime-type
    def add_feature_class(cls,mime_type,feature_class):
        cls._feature_class_map['mime_type']=feature_class

    @classmethod
    def add_default_feature_classes(cls):
        cls.add_feature_class('text/plain',TextFeature)

    @classmethod
    # return the feature class for the mime-type
    def feature_class(cls,mime_type):
        try:
            return cls._feature_class_map['mime_type']
        except:
            return Feature    

    @classmethod
    # return the feature class for the mime-type
    def value_class(cls,mime_type):
        try:
            return cls._value_class_map['mime_type']
        except:
            return str  

    ### Built-Ins ###
    def __str__(self):
        return str(self._packet)

    def __repr__(self):
        return repr(self._packet)

    ### Convert to/from JSON and YML ###
    '''Load the packet from a string or file handle. Also takes optional arguments for yaml.safe_load().'''
    def load_yml(self,s,**kwargs):
        self._packet=yaml.safe_load(s,**kwargs) 

    '''Convert the packet to YML and optionally save it to a file. Returns a string containing the YML. Also takes optional arguments for yaml.safe_dump().'''
    def dump_yml(self,file=None,**kwargs):
        if file:
            return yaml.safe_dump(self._packet,file,**kwargs)
        else:
            return yaml.safe_dump(self._packet,**kwargs)

    '''Load the packet from a string or file handle. Also takes optional arguments for yaml.safe_load().'''
    def load_json(self,s,**kwargs):
        self._packet=json.load(s,**kwargs) 

    '''Convert the packet to JSON and optionally save it to a file. Also takes optional arguments for json.dumps().'''
    def dump_json(self,file=None,**kwargs):
        kwargs.setdefault('default', str)
        kwargs.setdefault('indent', 4)
        
        s=json.dumps(self._packet,**kwargs)
        if file: file.write(s)
        return s

class Span(DialogPacket):
    ### Constructor ###
    '''Construct an empty dialog event'''
    def __init__(self):
       super().__init__()

    # property: start
    @property
    def start(self):
        return self._packet.get(ELMNT_START,None)

    @start.setter
    def start(self,s):
        self._packet[ELMNT_START]=s

    # property: end
    @property
    def end(self):
        return self._packet.get(ELMNT_END,None)

    @end.setter
    def end(self,s):
        self._packet[ELMNT_END]=s

    # property: start-offset
    @property
    def start_offset(self):
        return self._packet.get(ELMNT_START_OFFSET,None)

    @start_offset.setter
    def start_offset(self,s):
        self._packet[ELMNT_START_OFFSET]=s

    # property: end-offset
    @property
    def end_offset(self):
        return self._packet.get(ELMNT_END_OFFSET,None)

    @end_offset.setter
    def end_offset(self,s):
        self._packet[ELMNT_END_OFFSET]=s

class DialogEvent(DialogPacket):
    ### Constructor ###
    '''Construct an empty dialog event'''
    def __init__(self):
       super().__init__()

    # property: speeaker_id
    @property
    def speaker_id(self):
        return self._packet.get(ELMNT_SPEAKER_ID,None)

    @speaker_id.setter
    def speaker_id(self,s):
        self._packet[ELMNT_SPEAKER_ID]=s

    # property: id
    @property
    def id(self):
        return self._packet.get(ELMNT_ID,None)

    @id.setter
    def id(self,s):
        self._packet[ELMNT_ID]=s

    # property: prevous_id
    @property
    def previous_id(self):
        return self._packet.get(ELMNT_PREV_ID,None)

    @previous_id.setter
    def previous_id(self,s):
        self._packet[ELMNT_PREV_ID]=s

    # property: features
    @property
    def features(self):
        return self._packet.get(ELMNT_FEATURES,None)

    @features.setter
    def features(self,s):
        self._packet[ELMNT_FEATURES]=s

    # property: span
    @property
    def span(self):
        return self._packet.get(ELMNT_SPAN,None)

    @span.setter
    def span(self,s):
        self._packet[ELMNT_SPAN]=s
        print(f'self._packet[ELMNT_SPAN]: {self._packet[ELMNT_SPAN]}')

    ### Add/Get span
    def add_span(self,span):
        if self.span is None:
            self.span={}    
        self.span=span.packet
        print(f'self.span:{self.span}')
        return span            

    ### Add/Get Features ###
    def add_feature(self,feature_name,feature):
        if self.features is None:
            self.features={}
        
        self.features[feature_name]=feature.packet
        return feature

    def get_feature(self,feature_name):
        fpacket=self.features.get(feature_name,None)
        
        if fpacket is not None: 
            feature=self.feature_class(fpacket.get(ELMNT_MIME_TYPE,None))()
            feature.packet=fpacket
            return feature
        else:
            return None

class Feature(DialogPacket):
    ### Constructor ###

    '''Construct a dialog event feature'''
    def __init__(self,mime_type=None,lang=None,encoding=None,p={},**kwargs):
        #print(f'Feature() kwargs: {kwargs}')
        super().__init__(**kwargs)        
        #print(f'A2: {self.packet}')
        self._token_class=Token
        
        if mime_type is not None: 
            self._packet[ELMNT_MIME_TYPE]=mime_type
        if lang is not None:
            self._packet[ELMNT_LANG]=lang
        if encoding is not None:
                self._packet[ELMNT_ENCODING]=encoding
        
        #Create the empty array of arrays for the tokens.
        self._packet[ELMNT_TOKENS]=[]

    def add_token(self, **kwargs):
        my_token=self._token_class(**kwargs)
        self.tokens.append(my_token.packet)
        return my_token

    def get_token(self,token_ix=0):
        try:
            token=self._token_class()
            token.packet=self.tokens[token_ix]
        except:
            token=None
        return token

    ### Getters and Setters ###
    # property: mime_type
    @property
    def mime_type(self):
        return self._packet.get(ELMNT_MIME_TYPE,None)

    # property: lang
    @property
    def lang(self):
        return self._packet.get(ELMNT_LANG,None)

    # property: encoding
    @property
    def encoding(self):
        return self._packet.get(ELMNT_ENCODING,None)

    # property: tokens
    @property
    def tokens(self):
        return self._packet.get(ELMNT_TOKENS,None)
    
#Note need to debug default argument overrides.
class TextFeature(Feature):
    def __init__(self,**kwargs):
        #print(f'Text Feature() kwargs: {kwargs}')
        super().__init__(mime_type='text/plain',**kwargs)
        #print(f'A3: {self.packet}')
        self._token_class=Token

class Token(DialogPacket):
    ### Constructor ###
    '''Construct a dialog event token.'''
    def __init__(self,value=None,links=None,confidence=None):
        super().__init__()

        if value is not None: 
            self.value=value
        if links is not None:
            self._packet[ELMNT_LINKS]=links
        if confidence is not None:
            self._packet[ELMNT_CONFIDENCE]=confidence            
        
    ### Getters and Setters ###
    @property
    def value(self):
        return self._packet.get(ELMNT_VALUE,None)

    @value.setter
    def value(self,value):
        self._packet[ELMNT_VALUE]=value   

    @property    
    def confidence(self):
        return self._packet.get(ELMNT_CONFIDENCE,None)

    @confidence.setter
    def confidence(self,confidence):
        self._packet[ELMNT_CONFIDENCE]=confidence  


class History(DialogPacket):
    ### Constructor ###
    '''Construct a dialog history object token.'''
    def __init__(self):
        super().__init__()
        
        #Create the empty array of dialog events
        self._packet[ELMNT_HISTORY]=[]

    def add_event(self, dialog_event):
        self._packet[ELMNT_HISTORY].append(dialog_event)
        return dialog_event

    def get_event(self,ix=0):
        try:
            event=DialogEvent()
            event.packet=self._packet[ELMNT_TOKENS][ix]
        except:
            event=None
        return event

#This is an experimental derivation of the DialogEvent adding stand-off XML interpretation.  
class DialogEventWithXML(DialogEvent):
    ### Stand-off synthesis ###
    '''Converts a feature of type text/x.ovn.xmlmarkup-1.0 into an XML string.'''
    def to_xml(self,xml_feature):
        #add the words to it
        _features=self._packet.get('features',None)
        _feature=_features.get(xml_feature,None)
        _feature_tokens=_feature.get('tokens',None)

        #root token is first token
        _root_token=_feature_tokens[0]
        _root_token_element=_root_token['value']['element']
        _root_token_link_feature=_root_token['token-link']['feature']
        _linked_feature=_features.get(_root_token_link_feature,None)
        _linked_feature_tokens=_linked_feature['tokens'][0]

        #print(str(_linked_feature_tokens))

        #build the root with the words
        root=ET.Element(_root_token_element)
        ix=0
        _linked_tokens=[]
        for t in _linked_feature_tokens:
            _linked_tokens.append(ET.SubElement(root, 'token',{'ix':f'{ix}'}))
            _linked_tokens[ix].text=t['value']
            ix+=1

        #Now add all the elements
        if (len(_feature_tokens)>1):
            for token in _feature_tokens[1:]:
                #get xpath of the first and last tokens
                _element=token['value'].get('element',None)
                _attributes=token['value'].get('attributes',None)                
                _token_link=token.get('token-link',None)
                if (_token_link is not None):
                    _token_link_feature=_token_link.get('feature',None)  
                    _token_link_tokens=_token_link.get('tokens',None)  
                    print(f'token-link feature:{_token_link_feature}, tokens: {_token_link_tokens}')
                    if (not _token_link_feature==_root_token_link_feature):
                        raise KeyError(f'The feature: {_token_link_feature} in element: {_element} is different to the root linked feature: {_root_token_link_feature}')
                    markup_element=ET.Element(_element)

                    #find the first word in the current tree
                    start_ix=int(_token_link_tokens[0]) if _token_link_tokens else 0
                    end_ix=int(_token_link_tokens[-1]) if _token_link_tokens else len(_linked_feature_tokens)-1
                    
                    #insert the new element just before the start token word.
                    self.print_iter_index(root)
                    start_child = root.find(f'.//*[@ix="{start_ix}"]')
                    start_root_index=self.get_iter_index(start_child,root)
                    end_child= root.find(f'.//*[@ix="{end_ix}"]')
                    end_root_index=self.get_iter_index(end_child,root)
                    print(f'start_ix:{start_ix} start_root_index: {start_root_index} end_ix: {end_ix} end_root_index: {end_root_index}')
                    root.insert(start_root_index,markup_element)
                    children=[root[i] for i in range(start_root_index+1,end_root_index+1)]
                    for c in children:
                        print(f'child: {c}')
                        root.remove(c)
                        markup_element.append(c)

        #return the xml
        return ET.ElementTree(self.indent(self.indent(root)))

    @staticmethod
    def print_iter_index(host_element):
        for p in host_element.getiterator():
            print(f'p: {p}')

    '''Returns the integer location of the find_element inside the host_element'''
    @staticmethod
    def get_iter_index(find_element,host_element):
        parent_map = {c: p for p in host_element.getiterator() for c in p}    
        
        for f,v in parent_map:
            print (f'f: {f} v: {v}')
        
        return list(parent_map[find_element]).index(find_element)

    @staticmethod
    def indent(elem, level=0):
        i = "\n" + level*"  "
        j = "\n" + (level-1)*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for subelem in elem:
                self.indent(subelem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = j
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = j
        return elem

#Define default feature classes
#DialogPacket.add_default_feature_classes()