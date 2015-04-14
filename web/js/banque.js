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
                  '</tr>').appendTo("table.banque tbody");
                  $("#r_" + data[i].id).click(function(event) {
                      var attr_nom = $("td.nom", this);
                      attr_nom.html('<form><input type="text"></form>');
                      $(this).off('click');
                  });
            }
        },
    });    
});

