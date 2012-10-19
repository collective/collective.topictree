$(function() {

    var displayError = function (data) {
        $('#errorBox')
            .html("An error occurred.")
            .addClass("errorbox");
    }

    $(".topictree").jstree({ 
        "core": {
            "animation": 100,
        },
		// List of active plugins
		"plugins" : [ 
			"themes", "ui", "crrm", "json_data", "types", "contextmenu" 
		],
        "json_data" : {
            "ajax" : { "url" : "@@treedata" },
        },
        "themes" : {
            "theme" : "default",
            "dots" : false,
            "icons" : false
        },
        "types" : {
            // Want only root nodes to be root nodes
            // This will prevent moving or creating any other type as a rootnode
            "valid_children" : [ "root" ],
            "types" : {
                "root" : {
                    // can have topics inside, but NOT other root nodes
                    "valid_children" : [ "default" ],
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
        "contextmenu":  {
            "items": {}
        }
    })
    .bind("create.jstree", function (e, data) {
        var node_uid = data.rslt.parent.attr("node_uid");
        $.ajax({
            url: "@@addtopic",
            data: {
                'context_uid': node_uid,
                'title': data.rslt.name
            },
            success: function(r) {
                $(data.rslt.obj).attr("node_uid", r.node_uid);
            },
            error: function(r) {
                $.jstree.rollback(data.rlbk);
                displayError(r);
            },
            dataType: "json",
        });

    })
    .bind("rename.jstree", function (e, data) {
        var node_uid = data.rslt.obj.attr("node_uid");
        $.ajax({
            url: "@@edittopic",
            data: {
                'topic_title': data.rslt.new_name,
                'node_uid': node_uid
            },
            error: function(r) {
                $.jstree.rollback(data.rlbk);
                displayError(r);
            },
            dataType: "json",
        });
    })
    .bind("remove.jstree", function (e, data) {
        var node_uid = data.rslt.obj.attr("node_uid");
        $.ajax({
            url: "@@deletetopic",
            data: {'node_uid': node_uid},
            error: function(r) {
                $.jstree.rollback(data.rlbk);
                displayError(r);
            },
            dataType: "json",
        });
    })
    .bind("move_node.jstree", function (e, data) {
        data.rslt.o.each(function (i) {
            var source_uid = $(this).attr('node_uid');
            var target_uid = $(data.rslt.r).attr('node_uid');
            $.ajax({
                async : false,
                url: "@@pastetopic",
                data: {
                    'source_uid' : source_uid,
                    'target_uid' : target_uid,
                    'is_copy' : data.rslt.cy
                },
                error: function(r) {
                    $.jstree.rollback(data.rlbk);
                    displayError(r);
                },
                dataType: "json",
            });
        });
    })

    .bind("dblclick.jstree", function(e) {
        $(this).jstree('toggle_node', e.target);
    });

});
