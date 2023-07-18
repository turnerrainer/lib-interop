const fs = require('fs');
const yaml = require('js-yaml');

class DialogPacket {
    constructor() {
        this.packet={}
    }

    // Load the packet from a string
    load_json(s) {
        this.packet=JSON.parse(s)
    }

    dump_json() {
        return JSON.stringify(this.packet)
    }

    load_yml(s) {
        this.packet=yaml.load(s);
    }
    dump_yml() {
        return yaml.safeDump(data);
    }
}

this.DialogPacket=DialogPacket