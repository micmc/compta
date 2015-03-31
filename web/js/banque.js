// Initialisation du Document
// On efface toutes les lignes du tableau
$('document').ready(function(){
    //$("table.banque").load();
    //Na marche pas !!!
    $("table tbody").find("tr:gt(0)").remove();
    test = $("table tbody").find("tr:gt(0)");
    alert(test.length);
});

//$("table.banque").ready(function(e) {
//    $.ajax(
//    {
//        method: "GET",
//        url: "http://localhost:8080/banque",
//        dataType: "json", 
//        success: function(data) {
//            for(i=0; i< data.length; i++) {
//                $('<tr id="r_'+data[i].id+'">'+
//                  '<td>'+data[i].nom+'</td>'+
//                  '<td>'+data[i].adresse+'</td>'+
//                  '<td>'+data[i].ville+'</td>'+
//                  '<td>'+data[i].cp+'</td>'+
//                  '</tr>').appendTo("table.banque tbody");
//            }
//        },
//    });    
//});

// Ne marche pas aussi
$($("#banque").on("Click", "tr", function(e) {
    //var edittrid = $(this).attr('id');
    alert("test");
}));
