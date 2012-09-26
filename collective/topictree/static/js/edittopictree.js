$(document).ready(function() {

$(function () {
        $("#mmenu input").click(function () {
            switch(this.id) {
                case "add_topic":
                    $.ajax({
                            url: "@@addtopic",
                            //data: {
                            //      'context_node': 
                            //},
                            success: createNode,
                            error: displayError,
                            dataType: "json",
                            context: this
                    });
                    break;
                // uses crrm plugin rename function
                case "rename":
                   // start the rename action
                    $("#treeroot").jstree("rename");

                    break;
                // uses crrm plugin remove function
                case "remove":
                    var node_uid_to_delete = $('.jstree-clicked').parent()
                                              .attr('node_uid')
                    $.ajax({
                          url: "@@deletetopic",
                          data: {
                                 'node_uid': node_uid_to_delete
                                },
                          success: deleteNode,
                          error: displayError,
                          dataType: "json",
                          context: this
                    });
                    break;

                // uses crrm plugin cut function
                case "cut":
                    $("#treeroot").jstree("cut");
                    break;

                // uses crrm plugin copy function
                case "copy":
                    $("#treeroot").jstree("copy");
                    break;

                // uses crrm plugin paste function
                case "paste":
                    $("#treeroot").jstree("paste");
                    break;


//                default:
//                    $("#treeroot").jstree(this.id);
//                    break;
            }
        });
});

$("#treeroot")
	.jstree({ 
		// List of active plugins
		"plugins" : [ 
			"themes","ui","crrm","contextmenu","checkbox","json_data"//,"html_data",
		],
		"core" : { 
//			"initially_open" : [ "root2"  ] 
		},
//        "html_data" : {
//            "data" : "<li id='root'><a href='#'>Root node</a></li>"
//            "data" : "<ul><li id='root'><a href='#'>Root node</a>\
//                      <ul><li><a href='#'>Child node</a></li><li><a href='#'>Child node2</a></li></ul></li>\
//                      <li id='root2'><a href='#'>Another root node</a>\
//                      <ul><li><a href='#'>Child node</a></li></ul></li></ul>"
//        },
        "json_data" : {
                "data" : [
                    {
                        "data" : "A node",
                        "metadata" : { id : 23 },
                        "children" : [ "Child 1", "A Child 2" ]
                    },
                    {
                        "attr" : { "id" : "li.node.id1" },
                        "data" : {
                            "title" : "Long format demo",
                            "attr" : { "href" : "#" }
                        }
                    }
                ]
        },
        "checkbox" : {
            "two_state" : true
        },
        "themes" : {
                "theme" : "default-mod",
                "dots" : false,
                "icons" : false
        }
    })
    //this fires after an item is edited in the tree
    .bind("rename.jstree", function (e, data) {

        // get the selected node
        var node_uid = $('.jstree-clicked').parent().attr('node_uid')
        var edited_title = $('.jstree-clicked').text().trim()

        console.log("renamed");
        $.ajax({
                url: "@@edittopic",
                data: {
                       'topic_title': edited_title,
                       'node_uid': node_uid
                      },
                error: displayError,
                dataType: "json",
                context: this
        });

    })
    //this fires after an item is removed from the tree
    .bind("remove.jstree", function (e, data) {
       console.log("and its gone..");
    });

});

function createNode(data, textStatus, jqXHR) {

    var node_uid = data.node_uid;
    var path = data.path;

    $("#treeroot").bind("create.jstree", function (e, data) {
                       console.log("created a new node");
                       var topic_title = $('[node_uid="' + node_uid + '"] > a')
                                          .text().trim();
                       console.log(topic_title);
                       console.log(node_uid);
                       $.ajax({
                               url: "@@edittopic",
                               data: {
                                      'topic_title': topic_title,
                                      'node_uid': node_uid
                               },
                               //error: displayError,
                               dataType: "json",
                               context: this
                       });
                       // remove binding so this is called only once
                       // (not everytime another object is created)
                       $(this).unbind("create.jstree");

                  })
                  .jstree("create",
                           -1,
                           "last", 
                           { "attr" : { "rel" : 
                                        this.id.toString().replace("add_", ""),
                                        "node_uid" : node_uid,
                                        "path" : path
                                      },
                           "data" : "New node" // specify default new text
                           });

}

function deleteNode(data, textStatus, jqXHR) {
    // delete the node from the tree ( ajax delete was successfull)
    $("#treeroot").jstree("remove");
}

function displayError(jqXHR, textStatus, errorThrown) {
    alert(errorThrown);
    // XXX CHANGE THIS TO be embedded in the DOM with a message
}

