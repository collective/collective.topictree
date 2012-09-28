$(document).ready(function() {

$(function () {
        $("#mmenu input").click(function () {
            var context_node_uid = $('.jstree-clicked').parent().attr('node_uid');
            // select the root node if nothing is selected
            if (context_node_uid == undefined) {
                var treeroot = $('[rel="root"] > a');
                $(treeroot).click();
                context_node_uid = $(treeroot).parent().attr('node_uid');
            }

            switch(this.id) {
                case "add_topic":
                    console.log("ADDING");

                    $.ajax({
                            url: "@@addtopic",
                            data: {
                                  'context_node_uid': context_node_uid
                            },
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
                    $.ajax({
                          url: "@@deletetopic",
                          data: {
                                 'node_uid': context_node_uid
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
            }
        });
});

$("#treeroot")
	.jstree({ 
		// List of active plugins
		"plugins" : [ 
			"themes","ui","crrm","contextmenu","json_data","types"//"dnd"
		],
        "json_data" : {
                    "ajax" : { "url" : "@@stateoftree" },
        },
        "themes" : {
                "theme" : "default-mod",
                "dots" : false,
//                "icons" : false
        },
        "types" : {
            // Want only root nodes to be root nodes
            // This will prevent moving or creating any other type as a rootnode
            "valid_children" : [ "root" ],
            "types" : {
                "topic" : {
                    // can have topics inside, but NOT root nodes
                    "valid_children" : [ "topic" ],
                },
                "root" : {
                    // can have topics inside, but NOT other root nodes
                    "valid_children" : [ "topic" ],
                    // those prevent the functions with the same name to be used
                    // on root nodes internally the `before` event is used
                    "start_drag" : false,
                    "move_node" : false,
                    "delete_node" : false,
                    "remove" : false,
                    "rename_node" : false
                }
            }
        },
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
                           null,
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

