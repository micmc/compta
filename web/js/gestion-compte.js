function efface_formulaire_banque() {
    $('#id_banque-nom').val("");
    $('#id_banque-adresse').val("");
    $('#id_banque-ville').val("");
    $('#id_banque-cp').val("");
    $('#id_banque-pays').val("");
}

// Initialisation du Document
// On affiche uniquement les banques et aucun formulaire
$('document').ready(function(){
    $('#formulaire_banque').hide();
    $('#formulaire_compte').hide();
    //$('#id_update_banque').attr("disabled",true);
    $('#id_delete_banque').attr("disabled",true);
    //$('#id_update_compte').attr("disabled",true);
    $('#id_delete_compte').attr("disabled",true);
    $('#id_banque').change();
});

// Sélection des comptes pour une banque
// Initialise et affiche dans le tableau, la liste des comptes associées
// Requête AJAX sur lui-même.
// Affiche le formulaire des banques avec ces propriétés
// Cache le formulaire des comptes
// Active le bouton supprimer
//
$($('#id_banque').change(function(e) {
    $('#id_banque-id').remove();
    //$("#id_compte").find("tr:gt(0)").remove();
    $("#id_compte").empty();
    var banqueId = $('#id_banque').val();
    $.ajax(
    {
        type:"POST",
        data: { 
                id : banqueId,
                type : 'detail_banque',
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                //csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        url:"",
        success: function(data) {
            $("#id_compte").append('<option value="0">-</option>');
            $('#formulaire_compte :input[type!="submit"][type!="hidden"]').val('');
            for (var i=0; i < data.compte.length; i++) {
                 $("#id_compte").append('<option value="' + data.compte[i].id + '">'+data.compte[i].nom+'</option>');
                 //$('<tr for="'+data.compte[i].id+'"><td class="name">'+data.compte[i].nom+'</td></tr>').insertAfter("#id_compte tr:last");
            }
            $('<input type="hidden" name="banque-id" id="id_banque-id" value="' + banqueId + '" />').prependTo("#formulaire_banque");
            $('#id_banque-nom').val(data.nom);
            $('#id_banque-adresse').val(data.adresse);
            $('#id_banque-ville').val(data.ville);
            $('#id_banque-cp').val(data.cp);
            $('#id_banque-pays').val(data.pays);
            $('#id_banque-cle_controle').val(data.cle_controle);
        },
    });
    $('#formulaire_banque').show(1000);
    $('#formulaire_compte').hide(500);
    $('#id_delete_banque').attr("disabled",false);
    //$('#id_compte').change();
    e.preventDefault();
}));

// Clique sur la création d'une nouvelle banque
// Effet graphique et initialisation
// Affiche le formulaire
// Efface le tableau des comptes
// Désactive le formulaire des compte
$($('#id_create_banque').click(function() {
    //Partie banque
    $('#id_banque-id').remove();
    $('#formulaire_banque').show(1000);
    $('#formulaire_banque :input[type!="submit"][type!="hidden"]').val('');
    //$('#id_update_banque').attr("disabled",true);
    $('#id_delete_banque').attr("disabled",true);
    $('#id_save_banque').attr("disabled",false);
    //Partie Compte
    $("#id_compte").find("tr:gt(0)").remove();
    $('#formulaire_compte').hide();
}));

// Sauvegarde d'un nouvel enregistrement ou modification
// Récupère les champs les envoie
$($('#formulaire_banque').submit(function(e) {
    $.ajax(
        {
            type:"POST",
            data: $(this).serialize(),
            url:"",
            success: function(data) {
                // Si c'est un nouvel enregistrement l'id n'existe pas
                if ( $('#id_banque-id').length == 0 )
                {
                    $('.errors_div').html("Nouvel Enregistrement effectué");
                    $('<input type="hidden" name="banque-id" id="id_banque-id" value="' + data.id + '" />').prependTo("#formulaire_banque");
                    $("#id_banque").append('<option value="' + data.id + '" selected="selected">'+$('#id_banque-nom').val()+'</option>');
                } else {
                    $('.errors_div').html("Enregistrement modifié");
                }
            },
            error: function(jqXHR, textStatus, errorThrown){
                $('.errors_div').html("Erreur d'enregistrement");
            },
        });
   e.preventDefault();
}));

// Suppression d'un document
$($('#id_delete_banque').click(function(e) {
    var nom = $('#id_banque-nom').val();
    var banque_id = $('#id_banque-id').val();
    var conf = confirm("Voulez-vous supprimer l'enregistrement : " + nom);
    if (conf==false) {
        return false;
    } else {
        $.ajax(
            {
                type:"POST",
                data: { id : banque_id,
                        type : 'delete',
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    },
                url:"",
                success: function(data) {
                    $('.errors_div').html("Suppression effectuée");
                    $('#formulaire_banque').hide(500);
                    $("#id_banque option[value='"+banque_id+"']").remove();
                },
                error: function(jqXHR, textStatus, errorThrown){
                    $('.errors_div').html("Erreur de suppression");
                },
            });
        e.preventDefault();
    }
}));

$($('#id_compte').change(function(e) {
    $('#id_compte-id').remove();
    //$("#id_compte").find("tr:gt(0)").remove();
    var compteId = $('#id_compte').val();
    if ( compteId == 0 ) {
        $('#formulaire_compte').hide(500);
        return 0;
    }
    $.ajax(
    {
        type:"POST",
        data: {
                id : compteId,
                type : 'detail_compte',
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                //csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        url:"",
        success: function(data) {
            $('<input type="hidden" name="compte-id" id="id_compte-id" value="' + compteId + '" />').prependTo("#formulaire_compte");
            $('#id_compte-nom').val(data.nom);
            //$('#id_numero').val(data.numero);
            //$('#id_cle').val(data.cle);
            $('#id_compte-type').val(data.type);
            $('#id_compte-archive').prop("checked",data.archive); 
        },
    });
    $('#formulaire_compte').show(1000);
    $('#id_delete_banque').attr("disabled",false);
    e.preventDefault();
}));

// Clique sur la création d'un nouveau compte
// Effet graphique et initialisation
// Affiche le formulaire
$($('#id_create_compte').click(function() {
    //Partie compte
    $('#id_compte-id').remove();
    $('#formulaire_compte').show(1000);
    $('#formulaire_compte :input[type!="submit"][type!="hidden"]').val('');
    $('#id_delete_compte').attr("disabled",true);
    $('#id_save_compte').attr("disabled",false);
}));

// Affichage des détails d'un document
$($('#id_compte').on('click', 'tr', function(e) {
    $('#id_pk').remove();
    if ($(this).index() == 0) return;
    var compteId = $(this).attr("for");
    var trTmp=$(this)
    $.ajax(
        {
            type:"POST",
            data: { id : compteId,
                    type : 'detail',
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    //csrfmiddlewaretoken: '{{ csrf_token }}'
                },
            url:"",
            success: function(data) {
                $('#formulaire').show(1000);
                $('#id_nom').val(data.nom);
                $('#id_numero').val(data.numero);
                $('#id_cle').val(data.cle);
                $('#id_type').val(data.type);
                $('#id_archive').prop("checked",data.archive);
                $('<input type="hidden" name="id" id="id_pk" value="' + compteId + '" />').prependTo("#formulaire");
                $('tr').css("background-color","white");        
                trTmp.css("background-color","#FFFF99");
                //$('#id_update').attr("disabled",false);
                $('#id_delete').attr("disabled",false);
            },
            error: function(jqXHR, textStatus, errorThrown){
                $('.errors_div').html(jqXHR.responseText);
            },
        });
    e.preventDefault();
}));
