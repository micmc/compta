// Initialisation du Document
$('document').ready(function(){
    $('#formulaire').hide();
    $('#id_update').attr("disabled",true);
    $('#id_delete').attr("disabled",true);
});

// Création d'un document
$($('#id_create').click(function() {
    $('#id_pk').remove();
    $('tr').css("background-color","white");
    $('#formulaire').show(1000);
    $(':input[type!="submit"][type!="hidden"]').val('');
    $('#id_update').attr("disabled",true);
    $('#id_delete').attr("disabled",true);
    $('#id_save').attr("disabled",false);
}));

// Envoie du document pour création ou enregistrement
    $($('#formulaire').submit(function(e) {
    $.ajax(
       {
           type:"POST",
           data: $(this).serialize(),
           url:"",
           success: function(data) {
               $('.errors_div').html("");
               $('#formulaire').hide(1000);
               $('tr').css("background-color","white");
               if ($('tr[for='+data.id+']').length == 0) {
                    $('<tr for="'+data.id+'"><td class="name">'+data.nom+'</td></tr>').insertAfter("#id_banque tr:last");
               } else {
                    $('tr[for='+data.id+'] td').text(data.nom); 
               }
            },
            error: function(jqXHR, textStatus, errorThrown){
                $('.errors_div').html("Erreur d'enregistrement");
            },

       });
   e.preventDefault();
}));

// Suppression d'un document
$($('#id_delete').click(function(e) {
    var nom = $('#id_nom').val();
    var banqueId = $('#id_pk').val();
    var conf = confirm("Voulez-vous supprimer l'enregistrement : " + nom);
    if (conf==false) {
        return false;
    } else {
        $.ajax(
            {
                type:"POST",
                data: { id : banqueId,
                        type : 'delete',
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                        //csrfmiddlewaretoken: '{{ csrf_token }}',
                    },
                url:"",
                success: function(data) {
                    $('#formulaire').hide(1000);
                    $('tr').css("background-color","white");        
                    $('table tr[for='+banqueId+']').remove();
                    $('#id_pk').remove();
                },
            });
        e.preventDefault();
    }
}));

// Affichage des détails d'un document
$($('#id_banque').on('click', 'tr', function(e) {
    if ($(this).index() == 0) return;
    $('#id_pk').remove();
    var banqueId = $(this).attr("for");
    var trTmp=$(this)
    $.ajax(
        {
            type:"POST",
            data: { id : banqueId,
                    type : 'detail',
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    //csrfmiddlewaretoken: '{{ csrf_token }}'
                },
            url:"",
            success: function(data) {
                $('#formulaire').show(1000);
                $('#id_nom').val(data.nom);
                $('#id_adresse').val(data.adresse);
                $('#id_ville').val(data.ville);
                $('#id_cp').val(data.cp);
                $('#id_cle_controle').val(data.cle_controle);
                $('#id_code_guichet').val(data.code_guichet);
                $('#id_code_banque').val(data.code_banque);
                $('<input type="hidden" name="id" id="id_pk" value="' + banqueId + '" />').prependTo("#formulaire");
                $('tr').css("background-color","white");        
                trTmp.css("background-color","#FFFF99");
                $('#id_update').attr("disabled",false);
                $('#id_delete').attr("disabled",false);
            },
            error: function(jqXHR, textStatus, errorThrown){
                $('.errors_div').html(jqXHR.responseText);
            },
        });
    e.preventDefault();
}));

