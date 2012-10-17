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

        //empty errorbox of previous messages if any.
        $('#errorBox').html("")
            .removeClass("errorbox")
            .removeClass("infobox");

        switch(this.id) {
            case "add_topic":
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

                var target = $('.jstree-clicked').parent().attr('node_uid');
                var root_uid = $('#treeroot > ul > li').attr('node_uid');
                // everything but the root can be renamed.
                if ( target != root_uid ) {        
                    // start the rename action
                    $("#treeroot").jstree("rename");
                }
                else {
                    $('#errorBox')
                        .html("Tree root cannot be renamed here.")
                        .addClass("errorbox");
                }
                break;

            // uses crrm plugin remove function
            case "remove":
                // clear cut and copy flags if any exist in the system
                // to prevent client side pasting of deleted node
                $('[cut_node="set"]').removeAttr('cut_node')
                $('[copy_node="set"]').removeAttr('copy_node')

                var target = $('.jstree-clicked').parent().attr('node_uid');
                var root_uid = $('#treeroot > ul > li').attr('node_uid');
                // everything but the root can be removed/deleted.
                if ( target != root_uid ) {        
                    $.ajax({
                        url: "@@deletetopic",
                        data: {'node_uid': context_node_uid},
                        success: deleteNode,
                        error: displayError,
                        dataType: "json",
                        context: this
                    });
                }
                else {
                    $('#errorBox')
                        .html("Tree root cannot be removed.")
                        .addClass("errorbox");
                }
                break;

            case "cut":
                // clear cut and copy flags if any exist in the system
                $('[cut_node="set"]').removeAttr('cut_node')
                $('[copy_node="set"]').removeAttr('copy_node')

                var target = $('.jstree-clicked').parent().attr('node_uid');
                var root_uid = $('#treeroot > ul > li').attr('node_uid');
                // everything but the root can be cut.
                if ( target != root_uid ) {        
                    $('.jstree-clicked').attr('cut_node', 'set');
                    // uses crrm plugin cut function
                    $("#treeroot").jstree("cut");    
                }
                else {
                    $('#errorBox')
                        .html("Tree root cannot be cut.")
                        .addClass("errorbox");
                }
                break;

            case "copy":
                // clear cut and copy flags if any exist in the system
                $('[cut_node="set"]').removeAttr('cut_node')
                $('[copy_node="set"]').removeAttr('copy_node')

                var target = $('.jstree-clicked').parent().attr('node_uid');
                var root_uid = $('#treeroot > ul > li').attr('node_uid');
                // everything but the root can be copied.
                if ( target != root_uid ) {
                    $('.jstree-clicked').attr('copy_node', 'set');
                    // uses crrm plugin copy function
                    $("#treeroot").jstree("copy");
                }
                else {
                    $('#errorBox')
                    .html("Tree root cannot be copied.")
                    .addClass("errorbox");
                }
                break;

            case "paste":
                var paste_uid = $('.jstree-clicked').parent()
                    .attr('node_uid')
                var cut_source_uid = $('[cut_node="set"]').parent()
                    .attr('node_uid')
                var copy_source_uid = $('[copy_node="set"]').parent()
                    .attr('node_uid')

                if (( cut_source_uid == undefined ) &&
                    ( copy_source_uid == undefined )) {
                    $('#errorBox')
                        .html("Nothing to paste.")
                        .addClass("infobox");              
                }
                // paste location cannot be same as cut/copy location
                // if that is the case, paste does nothing.
                else if  ((cut_source_uid != paste_uid) &&
                          (copy_source_uid != paste_uid)) {
                    $.ajax({
                        url: "@@pastetopic",
                        data: {
                            'paste_uid' : paste_uid,
                            'cut_source_uid' : cut_source_uid,
                            'copy_source_uid' : copy_source_uid
                        },
                        success: pasteNode,
                        error: displayError,
                        dataType: "json",
                        context: this
                    });
                }
                else {
                    $('#errorBox')
                        .html("Paste location same as source.")
                        .addClass("infobox");              
                }
                break;  
        }
    });
});

$("#treeroot")
	.jstree({ 
		// List of active plugins
		"plugins" : [ 
			"themes","ui","crrm","json_data","types"//"dnd","contextmenu"
		],
        "json_data" : {
            "ajax" : { "url" : "@@treedata" },
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
    });

});

function createNode(data) {
    var node_uid = data.node_uid;
    $("#treeroot").bind("create.jstree", function (e, data) {
        var topic_title = $('[node_uid="' + node_uid + '"] > a').text().trim();
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
    .jstree("create", null, "last", 
        {"attr": {
            "rel" : this.id.toString().replace("add_", ""),
            "node_uid" : node_uid},
        "data" : "New node" // specify default new text
        });
}

function deleteNode(data) {
    // delete the node from the tree ( ajax delete was successfull)
    // uses crrm plugin remove function
    $("#treeroot").jstree("remove");
}

function pasteNode(data) {
    // paste into the tree ( ajax paste was successfull)
    // uses crrm plugin paste function
    $("#treeroot").jstree("paste");
    // clear the cut flag if cutting ( so that you dont paste
    // twice when using cut )
    $('[cut_node="set"]').removeAttr('cut_node');
}

function displayError(data) {
    $('#errorBox')
        .html("An error occurred.")
        .addClass("errorbox");
}

