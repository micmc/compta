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

function put_update(thisObj) {
    return 0;
}

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
        data_banque = {
                nom: $("#r_" + banque_id + " td.nom input").val(),
                adresse: $("#r_" + banque_id + " td.adresse input").val(),
                ville: $("#r_" + banque_id + " td.ville input").val(),
                cp : $("#r_" + banque_id + " td.cp input").val(),
                pays : $("#r_" + banque_id + " td.pays input").val(),
                cle : $("#r_" + banque_id + " td.cle input").val(),
                code_banque: $("#r_" + banque_id + " td.code_banque input").val(),
                code_guichet: $("#r_" + banque_id + " td.pays input").val(),
               };
         $.ajax(
        {
            method: "PUT",
            url: "http://localhost:8080/banque/" + banque_id,
            dataType: "html",
            contentType: "application/json",
            data: JSON.stringify(data_banque),
            success: function(data) {
                console.log("OK pour update", data);
                $("#r_" + banque_id + " td.nom input").remove();
                $("#r_" + banque_id + " td.nom").text(data_banque["nom"]);
                $("#r_" + banque_id + " td.adresse input").remove();
                $("#r_" + banque_id + " td.adresse").text(data_banque["adresse"]);
                $("#r_" + banque_id + " td.ville input").remove();
                $("#r_" + banque_id + " td.ville").text(data_banque["ville"]);
                $("#r_" + banque_id + " td.cp input").remove();
                $("#r_" + banque_id + " td.cp").text(data_banque["cp"]);
                $("#r_" + banque_id + " td.pays input").remove();
                $("#r_" + banque_id + " td.pays").text(data_banque["pays"]);
                $("#r_" + banque_id + " td.cle input").remove();
                $("#r_" + banque_id + " td.cle").text(data_banque["cle"]);
                $("#r_" + banque_id + " td.code_banque input").remove();
                $("#r_" + banque_id + " td.code_banque").text(data_banque["code_banque"]);
                $("#r_" + banque_id + " td.code_guichet input").remove();
                $("#r_" + banque_id + " td.code_guichet").text(data_banque["code_guichet"]);
                $("#r_" + banque_id + " td.status input").remove()
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log("Error", jqXHR);
            },
        });
    });
    $(thisObj).off('click');
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


