$(document).ready(function() {

    console.log("Edit Topic Tree JS loaded");

jq("#treeroot")
	.jstree({ 
		// List of active plugins
		"plugins" : [ 
			"themes","ui","crrm","dnd","search","types","contextmenu","hotkeys","cookies"//,"json_data",
		],
		// UI & core - the nodes to initially select and open will be overwritten by the cookie plugin

		// the UI plugin - it handles selecting/deselecting/hovering nodes
		"ui" : {
			// this makes the node with ID node_4 selected onload
//			"initially_select" : [ "node_4" ]
		},
		// the core plugin - not many options here
		"core" : { 
			// just open those two nodes up
			// as this is an AJAX enabled tree, both will be downloaded from the server
//			"initially_open" : [ "node_2" , "node_3" ] 
		}
	});


    console.log("post tree debug message");

});

