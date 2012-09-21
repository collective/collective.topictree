$(document).ready(function() {


jq(function () {
        jq("#mmenu input").click(function () {
            switch(this.id) {
                case "add_topic":
                    jq.ajax({
                            url: "@@addtopic",
                            data: {
                                    'topic_title': 'test'
                            },
                            success: createNode,
                            error: displayError,
                            dataType: "json",
                            context: this
                    });

                    break;
                default:
                    jq("#treeroot").jstree(this.id);
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
		"core" : { 
//			"initially_open" : [ "root2"  ] 
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
        },
        "themes" : {
                "theme" : "default-mod",
                "dots" : false,
                "icons" : false
        }
	});

});

function createNode(data, textStatus, jqXHR) {

    var title = data.title;
    var node_uid = data.node_uid;
    var path = data.path;

    jq("#treeroot").jstree("create",
                           null,
                           "last", 
                           { "attr" : { "rel" : 
                                        this.id.toString().replace("add_", ""),
                                        "node_uid" : node_uid,
                                        "path" : path
                                      }
                           });
    li a 
}

function displayError(jqXHR, textStatus, errorThrown) {
    alert(errorThrown);
}



