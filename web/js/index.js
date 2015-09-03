// Initialisation du Document
// On efface toutes les lignes du tableau

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
            if (compteId = getCookie('compte_id')) {
                $('select[name="compte"]').val(compteId);
            }
            $('select[name="compte"]').change()
        },
    });
});

$('select[name="compte"]').change(function(e) {
    var compte_id = $(this).val();
    $("#ref_ecriture").attr("href", "liste_ecriture.html?id=" + compte_id);
    setCookie('compte_id', compte_id);
    $.ajax(
    {
        method: "GET",
        url: "http://localhost:8080/compte/" + compte_id + "/ecriture/sum",
        dataType: "json",
        success: function(data) {
            $('#somme').text('Solde du compte : ' + data.somme + "€");
        },
    });
    $.ajax(
    {
        method: "GET",
        url: "http://localhost:8080/compte/" + compte_id + "/ecriture/month",
        dataType: "json",
        success: function(data) {
            console.log(data);      
            $.jqplot('graph_plot', data);
        },
    });
});
