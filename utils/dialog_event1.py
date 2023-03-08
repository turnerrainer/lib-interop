import yaml
import json

# standard element names
ELMNT_SPEAKER_ID='speaker-id'
ELMNT_ID='id'
ELMNT_PREV_ID='previous-id'
ELMNT_FEATURES='features'
ELMNT_FEATURE='feature'
ELMNT_MIME_TYPE='mime-type'
ELMNT_LANG='lang'
ELMNT_ENCODING='encoding'
ELMNT_TOKENS='tokens'
ELMNT_TOKEN_ARRAY='tokens'
ELMNT_VALUE='value'
ELMNT_TIME_LINK='time-link'
ELMNT_TOKEN_LINK='token-link'
ELMNT_CONFIDENCE='confidence'      
ELMNT_START='start'
ELMNT_END='end'

class DialogPacket1():
    '''Construct a packet'''
    def __init__(self,p={}):
        self._packet=p

    ### Getters and Setters ###
    # property: packet
    @property
    def packet(self):
        return self._packet

    @packet.setter
    def packet(self,p):
        self._packet=p

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
    
    '''Convert the packet to JSON and optionally save it to a file. Also takes optional arguments for json.dumps().'''
    def dump_json(self,file=None,**kwargs):
        kwargs.setdefault('default', str)
        kwargs.setdefault('indent', 4)
        
        s=json.dumps(self._packet,**kwargs)
        if file: file.write(s)
        return s

class DialogEvent(DialogPacket):
    ### Constructor ###
    '''Construct an empty dialog event'''
    def __init__(self,p):
       super().__init__(p)

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

    ### Add/Get Features ###
    def add_feature(self,feature_name,feature):
        if self.features is None:
            self.features={}
        
        self.features[feature_name]=feature.packet
        return feature

    def get_feature(self,feature_name):
        fpacket=self.features.get(feature_name,None)
        
        if fpacket is not None: 
            feature=self.feature_class(fpacket.get(ELMNT_MIME_TYPE,None))(fpacket)
            return feature
        else:
            return None

class Feature(DialogPacket):
    ### Constructor ###

    '''Construct a dialog event feature'''
    def __init__(self,p):
        super().__init__(p)        
        
        #Defaults (items that must be set)
        if self.tokens is None: self.tokens=[]
        if self.mime_type is None: self.mime_type='text/plain'

    def add_token_group(self):
        token_group=self.tokens.append([])
        return token_group

    def add_token(self, token):
        token_group=self.tokens[-1]
        token_group.append(token.packet)
        return token

    def get_token(self,token_ix=0,token_group=0):
        try:
            token=Token(self.tokens[token_group][token_ix])
        except:
            token=None
        return token

    ### Getters and Setters ###
    # property: packet
    @property
    def packet(self):
        return self._packet

    @packet.setter
    def packet(self,p):
        self._packet=p

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

    @tokens.setter
    def tokens(self,value):
        self._packet[ELMNT_TOKENS]=value     

class Token(DialogPacket):
    ### Constructor ###
    '''Construct a dialog event token.'''
    def __init__(self,s):
        super().__init__(s) 
        
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

class TimeLink(DialogPacket):
    ### Constructor ###
    def __init__(self,p):
        super().__init__(p)
        
    ### Getters and Setters ###
    ### TODO - Add time formatting to the setters and getters.
    @property
    def start(self):
        return self._packet.get(ELMNT_START,None)

    @start.setter
    def start(self,value):
        self._packet[ELMNT_START]=value   

    @property
    def end(self):
        return self._packet.get(ELMNT_END,None)

    @end.setter
    def end(self,value):
        self._packet[ELMNT_END]=value   

class TokenLink(DialogPacket):
    ### Constructor ###
    def __init__(self,p):
        super().__init__(p)
        
    ### Getters and Setters ###
    ### TODO - Add time formatting to the setters and getters.
    @property
    def feature(self):
        return self._packet.get(ELMNT_FEATURE,None)

    @feature.setter
    def feature(self,value):
        self._packet[ELMNT_FEATURE]=value   

    @property
    def tokens(self):
        return self._packet.get(ELMNT_TOKEN_ARRAY,None)

    @tokens.setter
    def tokens(self,value):
        self._packet[ELMNT_TOKEN_ARRAY]=value   
