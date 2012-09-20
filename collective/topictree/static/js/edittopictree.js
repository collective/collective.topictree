$(document).ready(function() {


jq(function () {
        $("#mmenu input").click(function () {
            switch(this.id) {
                case "add_topic":
                    $("#treeroot").jstree("create", null, "last", { "attr" : { "rel" : this.id.toString().replace("add_", "") } });
                    break;
                default:
                    $("#treeroot").jstree(this.id);
                    break;
            }
        });
});


jq("#treeroot")
	.jstree({ 
		// List of active plugins
		"plugins" : [ 
			"themes","ui","crrm","contextmenu","checkbox","html_data"//,"json_data",
		],
		// the core plugin - not many options here
		"core" : { 
			// just open those two nodes up
			// as this is an AJAX enabled tree, both will be downloaded from the server
			"initially_open" : [ "root2"  ] 
		},
        "html_data" : {
            "data" : "<li id='root'><a href='#'>Root node</a></li>"
//            "data" : "<ul><li id='root'><a href='#'>Root node</a>\
//                      <ul><li><a href='#'>Child node</a></li><li><a href='#'>Child node2</a></li></ul></li>\
//                      <li id='root2'><a href='#'>Another root node</a>\
//                      <ul><li><a href='#'>Child node</a></li></ul></li></ul>"

        },
        "checkbox" : {
            "two_state" : true
           // "override_ui" : true
        },
        "themes" : {
                "theme" : "default-mod",
                "dots" : false,
                "icons" : false
        }
	});

});

