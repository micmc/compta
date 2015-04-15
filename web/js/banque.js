// Initialisation du Document
// On efface toutes les lignes du tableau
$('document').ready(function(){
    //$("table.banque").load();
    //Na marche pas !!!
    //$("table tbody").find("tr:gt(0)").remove();
    //test = $("table tbody").find("tr:gt(0)");
    //alert(test.length);
    //$("table").selectable({ distance: 1, filter: "tr" });
    //$("table tbody tr").click(function(event) {
    //    alert("test");
    //});
});

function set_update(thisObj) {
    //$(thisObj).prepend("<form>");
    var attr_nom = $("td.nom", thisObj);
    attr_nom.html('<input type="text" value="' + attr_nom.text() + '">');
    //attr_nom.detach().appendTo("form", thisObj);
    var attr_adresse = $("td.adresse", thisObj);
    attr_adresse.html('<input type="text" value="' + attr_adresse.text() + '">');
    var attr_ville = $("td.ville", thisObj);
    attr_ville.html('<input type="text" value="' + attr_ville.text() + '">');
    var attr_cp = $("td.cp", thisObj);
    attr_cp.html('<input type="text" value="' + attr_cp.text() + '">');
    var attr_pays = $("td.pays", thisObj);
    attr_pays.html('<input type="text" value="' + attr_pays.text() + '">');
    var attr_cle = $("td.cle", thisObj);
    attr_cle.html('<input type="text" value="' + attr_cle.text() + '">');
    var attr_code_banque = $("td.code_banque", thisObj);
    attr_code_banque.html('<input type="text" value="' + attr_code_banque.text() + '">');
    var attr_code_guichet = $("td.code_guichet", thisObj);
    attr_code_guichet.html('<input type="text" value="' + attr_code_guichet.text() + '">');
    $("td.status", thisObj).html('<input type="button" value="OK">');
    $("td.status", thisObj).click(function(event) {
        banque_id = thisObj.attr("id").replace(/r_/,"");
        nom = $("#r_" + banque_id + " td.nom input").val();
        $.ajax(
        {
            method: "PUT",
            url: "http://localhost:8080/banque/" + banque_id,
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({
                    nom: $("#r_" + banque_id + " td.nom input").val(),
                    adresse: $("#r_" + banque_id + " td.adresse input").val()
                  }),
            success: function(data) {
                console.log("OK pour update", data);
            },
        });
    });
    $(thisObj).off('click');
    return 0;
}

function put_update(thisObj) {
    return 0;
}

function refresh_update(thisObj) {
    return 0;
}

$("table.banque").ready(function(e) {
    $.ajax(
    {
        method: "GET",
        url: "http://localhost:8080/banque",
        dataType: "json",
        success: function(data) {
            for(i=0; i< data.length; i++) {
                $('<tr id="r_'+data[i].id+'">'+
                  '<td class="nom">'+data[i].nom+'</td>'+
                  '<td class="adresse">'+data[i].adresse+'</td>'+
                  '<td class="ville">'+data[i].ville+'</td>'+
                  '<td class="cp">'+data[i].cp+'</td>'+
                  '<td class="pays">'+data[i].pays+'</td>'+
                  '<td class="cle">'+data[i].cle+'</td>'+
                  '<td class="code_banque">'+data[i].code_banque+'</td>'+
                  '<td class="code_guichet">'+data[i].code_guichet+'</td>'+
                  '<td class="status"></td>'+
                  '</tr>').appendTo("table.banque tbody");
                $("#r_" + data[i].id).click(function(event) {
                    set_update($(this));
                });
            }
        },
    });
});


