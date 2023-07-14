xxx
var fs = require('fs');

class DialogPacket {
    constructor() {
        this.packet={}
    }

    // Load the packet from a string
    load_json_string(s) {
        this.packet=JSON.parse(s)
        console.log(packet)
    }

    load_json_file(path) {
        fs.readFile(path, function (error, content) {
            var data = JSON.parse(content);
            console.log(data.collection.length);
        });
    }

    
    // Convert the packet to JSON and optionally save it to a file. 
    //dump_json(self,file=None,**kwargs):
    //    kwargs.setdefault('default', str)
    //    kwargs.setdefault('indent', 4)
    //    
    //    s=json.dumps(self._packet,**kwargs)
    //    if file: file.write(s)
    //    return s

}