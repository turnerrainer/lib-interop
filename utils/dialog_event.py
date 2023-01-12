import yaml
import json
import xml.etree.ElementTree as ET

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
ELMNT_TIME_LINK='time-link'
ELMNT_TOKEN_LINK='token-link'
ELMNT_CONFIDENCE='confidence'      

class DialogEvent():
    ### Constructor ###

    '''Construct an empty dialog event'''
    def __init__(self):
        self._packet={}

    ### Getters and Setters ###
    # property: packet
    @property
    def packet(self):
        return self._packet

    @packet.setter
    def packet(self,p):
        self._packet=p

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
    def add_feature(self,feature_name,**kwargs):
        if self.features is None:
            self.features={}
        f=DialogEventFeature(**kwargs)
        self.features[feature_name]=f.packet
        return f

    def get_feature(self,feature):
        try:
            return DialogEventFeature(self.features[feature])
        except:
            return None

    ### Built-Ins ###
    def __str__(self):
        return str(self._packet)

    def __repr__(self):
        return repr(self._packet)

    ### Convert to/from JSON and YML ###
    '''Load the dialog event from a string or file handle. Also takes optional arguments for yaml.safe_load().'''
    def load_yml(self,s,**kwargs):
        self._packet=yaml.safe_load(s,**kwargs) 

    '''Convert the dialog event to YML and optionally save it to a file. Returns a string containing the YML. Also takes optional arguments for yaml.safe_dump().'''
    def dump_yml(self,file=None,**kwargs):
        if file:
            return yaml.safe_dump(self._packet,file,**kwargs)
        else:
            return yaml.safe_dump(self._packet,**kwargs)
    
    '''Convert the dialog event to JSON and optionally save it to a file. Also takes optional arguments for json.dumps().'''
    def dump_json(self,file=None,**kwargs):
        kwargs.setdefault('default', str)
        kwargs.setdefault('indent', 4)
        
        s=json.dumps(self._packet,**kwargs)
        if file: file.write(s)
        return s

    ### Create and Interrogate features


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

        print(str(_linked_feature_tokens))

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
                    print_iter_index(root)
                    start_child = root.find(f'.//*[@ix="{start_ix}"]')
                    start_root_index=get_iter_index(start_child,root)
                    end_child= root.find(f'.//*[@ix="{end_ix}"]')
                    end_root_index=get_iter_index(end_child,root)
                    print(f'start_ix:{start_ix} start_root_index: {start_root_index} end_ix: {end_ix} end_root_index: {end_root_index}')
                    root.insert(start_root_index,markup_element)
                    children=[root[i] for i in range(start_root_index+1,end_root_index+1)]
                    for c in children:
                        print(f'child: {c}')
                        root.remove(c)
                        markup_element.append(c)

        #return the xml
        return ET.ElementTree(indent(indent(root)))

def print_iter_index(host_element):
    for p in host_element.getiterator():
        print(f'p: {p}')

'''Returns the integer location of the find_element inside the host_element'''
def get_iter_index(find_element,host_element):
    parent_map = {c: p for p in host_element.getiterator() for c in p}    
    
    for f,v in parent_map:
        print (f'f: {f} v: {v}')
    
    return list(parent_map[find_element]).index(find_element)

def indent(elem, level=0):
    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem

class DialogEventFeature():
    ### Constructor ###

    '''Construct a dialog event feature'''
    def __init__(self,mime_type=None,lang=None,encoding=None):
        self._packet={}
        if mime_type is not None: 
            self._packet[ELMNT_MIME_TYPE]=mime_type
        if lang is not None:
            self._packet[ELMNT_LANG]=lang

        if encoding is not None:
                self._packet[ELMNT_ENCODING]=encoding
        
        #Create the empty array of arrays for the tokens.
        self._packet[ELMNT_TOKENS]=[]

    def add_token_group(self):
        token_group=self._packet[ELMNT_TOKENS].append([])
        return token_group

    def add_token(self, **kwargs,token_class=DialogEventToken):
        token_group=self._packet[ELMNT_TOKENS][-1]
        token=token_class(**kwargs)
        token_group.append(token.packet)
        return token

    ### Getters and Setters ###
    # property: packet
    @property
    def packet(self):
        return self._packet

    @packet.setter
    def packet(self,p):
        self._packet=p

class DialogEventToken():
    ### Constructor ###

    '''Construct a dialog event feature'''
    def __init__(self,value=None,time_link=None,token_link=None,token_ref=None,confidence=None):
        self._packet={}
        if value is not None: 
            self._packet[ELMNT_VALUE]=value
        if time_link is not None:
            self._packet[ELMNT_TIME_LINK]=time_link
        if token_link is not None:
            self._packet[ELMNT_TOKEN_LINK]=token_link
        if confidence is not None:
            self._packet[ELMNT_CONFIDENCE]=confidence            
        
    ### Getters and Setters ###
    # property: packet
    @property
    def packet(self):
        return self._packet

    @packet.setter
    def packet(self,p):
        self._packet=p 