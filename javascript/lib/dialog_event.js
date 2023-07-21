const fs = require('fs');
// const yaml = require('js-yaml');

class DialogPacket {
    constructor(packet) {
        if (packet!=undefined) { 
            Object.assign(this,packet); 
        }
    }

    // Parse the JSON packet into elements of this class.
    load_json(s) {
        Object.assign(this,JSON.parse(s));
    }

    //Print the packet as a JSON string, pass through prettify arguments.
    dump_json() {
        //return JSON.stringify(this,arguments[0],arguments[1]);
        return JSON.stringify(this,null,4);
    }
}

class Span extends DialogPacket {
    constructor( {end_offset_msec=undefined,start_offset_msec=undefined} = {}) {
        if (end_offset_msec!=undefined) { 
            arguments[0].end_offset="PT"+(end_offset_msec/1000).toFixed(6);
            arguments[0].end_offset_msec=undefined
        }
        if (start_offset_msec!=undefined) { 
            arguments[0].start_offset="PT"+(start_offset_msec/1000).toFixed(6);
            arguments[0].start_offset_msec=undefined
        }
        super(arguments[0]);
    }
}

class DialogEvent extends DialogPacket {
    constructor() {
        super(arguments[0]);
        if (this.features==undefined) {
            this.features={};
        }
    }

    add_feature(feature_name,f) {
        this.features[feature_name]=f
        //Object.assign(this.features,f); 
    }
}

class Feature extends DialogPacket {
    constructor({mime_type=undefined,lang=undefined,encoding=undefined}={}) {
        super(arguments[0]);
        if (this.tokens==undefined) {
            this.tokens=[];
        }
    }

    add_token(t) {
        this.tokens.push(t)
    }
}

class Token extends DialogPacket {
    constructor() {
        super(arguments[0]);
    }
}

this.DialogPacket=DialogPacket
this.Span=Span
this.DialogEvent=DialogEvent
this.Feature=Feature