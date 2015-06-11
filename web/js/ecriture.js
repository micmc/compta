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
    var attr_date = $("td.date", thisObj);
    attr_date.html('<input type="text" value="' + attr_date.text() + '">');
    var attr_nom = $("td.nom", thisObj);
    attr_nom.html('<input type="text" value="' + attr_nom.text() + '">');
    //attr_nom.detach().appendTo("form", thisObj);
    var attr_montant = $("td.montant", thisObj);
    attr_montant.html('<input type="text" value="' + attr_montant.text() + '">');
    var attr_type = $("td.type", thisObj);
    attr_type.html('<input type="text" value="' + attr_type.text() + '">');
    var attr_categorie = $("td.categorie", thisObj);
    attr_categorie.html('<input type="text" value="' + attr_categorie.text() + '">');
    var attr_description = $("td.description", thisObj);
    attr_description.html('<input type="text" value="' + attr_description.text() + '">');
    var attr_valide = $("td.valide", thisObj);
    attr_valide.html('<input type="text" value="' + attr_valide.text() + '">');
    $("td.status", thisObj).html('<input type="button" value="OK">');
    $("td.status", thisObj).click(function(event) {
        ecriture_id = thisObj.attr("id").replace(/r_/,"");
        data_ecriture = {
                date: $("#r_" + ecriture_id + " td.date input").val(),
                nom: $("#r_" + ecriture_id + " td.nom input").val(),
                montant: $("#r_" + ecriture_id + " td.montant input").val(),
                type: $("#r_" + ecriture_id + " td.type input").val(),
                categorie : $("#r_" + ecriture_id + " td.categorie input").val(),
                description : $("#r_" + ecriture_id + " td.description input").val(),
                valide : $("#r_" + ecriture_id + " td.valide input").val(),
               };
         $.ajax(
        {
            method: "PUT",
            url: "http://localhost:8080/compte/10/ecriture" + ecriture_id,
            dataType: "html",
            contentType: "application/json",
            data: JSON.stringify(data_ecriture),
            success: function(data) {
                console.log("OK pour update", data);
                $("#r_" + ecriture_id + " td.date input").remove();
                $("#r_" + ecriture_id + " td.date").text(data_ecriture["date"]);
                $("#r_" + ecriture_id + " td.nom input").remove();
                $("#r_" + ecriture_id + " td.nom").text(data_ecriture["nom"]);
                $("#r_" + ecriture_id + " td.montant input").remove();
                $("#r_" + ecriture_id + " td.montant").text(data_ecriture["montant"]);
                $("#r_" + ecriture_id + " td.type input").remove();
                $("#r_" + ecriture_id + " td.type").text(data_ecriture["type"]);
                $("#r_" + ecriture_id + " td.categorie input").remove();
                $("#r_" + ecriture_id + " td.categorie").text(data_ecriture["categorie"]);
                $("#r_" + ecriture_id + " td.description input").remove();
                $("#r_" + ecriture_id + " td.description").text(data_ecriture["description"]);
                $("#r_" + ecriture_id + " td.valide input").remove();
                $("#r_" + ecriture_id + " td.valide").text(data_ecriture["valide"]);
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

$("table.ecriture").ready(function(e) {
    $.ajax(
    {
        method: "GET",
        url: "http://localhost:8080/compte/10/ecriture?filter=10",
        dataType: "json",
        success: function(data) {
            for(i=0; i< data.length; i++) {
                $('<tr id="r_'+data[i].id+'">'+
                  '<td class="date">'+data[i].date+'</td>'+
                  '<td class="nom">'+data[i].nom+'</td>'+
                  '<td class="montant">'+data[i].montant+'</td>'+
                  '<td class="type">'+data[i].type+'</td>'+
                  '<td class="categorie">'+data[i].categorie+'</td>'+
                  '<td class="description">'+data[i].description+'</td>'+
                  '<td class="valide">'+data[i].valide+'</td>'+
                  '<td class="status"></td>'+
                  '</tr>').appendTo("table.ecriture tbody");
                $("#r_" + data[i].id).click(function(event) {
                    set_update($(this));
                });
            }
        },
    });
});


