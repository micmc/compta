// Initialisation du Document
// On efface toutes les lignes du tableau

var id_compte;

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
    id_compte = $(location).attr("search").replace("?id=","");
});

$('select[name="compte"]').ready(function(e) {
    $.ajax(
    {
        method: "GET",
        url: "http://localhost:8080/compte?filter=type:prs,archive:false",
        dataType: "json",
        success: function(data) {
            for(i=0; i< data.length; i++) {
                $('<option value="'+data[i].id+'">'+
                     data[i].nom+
                  '</option>'
                 ).appendTo('select[name="compte"]');
            }
            $('select[name="compte"]').change()
        },
    });
});

$('select[name="compte"]').change(function(e) {
    var compte_id = $(this).val();
    $("#ref_ecriture").attr("href", "liste_ecriture.html?id=" + compte_id);
    $.ajax(
    {
        method: "GET",
        url: "http://localhost:8080/compte/" + compte_id + "/ecriture/sum",
        dataType: "json",
        success: function(data) {
            $('#somme').text('Solde du compte : ' + data.somme + "€");
        },
    })
});


