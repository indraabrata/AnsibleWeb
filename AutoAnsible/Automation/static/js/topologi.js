function tampil()
{

    var device = new vis.DataSet([
        {id:1, label:"router 1"},
        {id:2, label:"router 2"},
        {id:3, label:"router 3"},
        {id:4, label:"router 4"},
        {id:5, label:"router 5"},
        {id:6, label:"router 6"},
        {id:7, label:"router 7"},
    ]);

    var link = new vis.DataSet([
        {from:1, to:3},
        {from:1, to:2},
        {from:2, to:4},
        {from:2, to:6},
        {from:3, to:5},
        {from:3, to:7},
    ]);

    var myDiv = document.getElementById("topologi");

    var data = {
        nodes: device,
        edge: link
    }

    var options = {};

    var network = new vis.network(myDiv,data,options);
}