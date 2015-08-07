//Class for master api

function ApiRest(uri) {
}

ApiRest.prototype.listData = function(postData, jtParams) {
    return $.Deferred(function ($dfd) {
        if ("jtStartIndex" in jtParams && "jtPageSize" in jtParams) {
            pagingRest = "?skip=" + jtParams['jtStartIndex'] + "&top=" + jtParams['jtPageSize']; 
        } else {
            pagingRest = ""
        }
        if (window.idRest === undefined) {
            idRest="";
        }
        $.ajax({
             url: 'http://localhost:8080/' + uriRest + idRest + pagingRest,
             type: 'GET',
             dataType: 'json',
             success: function (data) {
                if ("jtStartIndex" in jtParams && "jtPageSize" in jtParams) {
                    dict_data = {
                                    Result: "OK",
                                    Records: data['values'],
                                    TotalRecordCount: data['count']
                                }
                } else {
                    dict_data = {
                                    Result: "OK",
                                    Records: data,
                                    TotalRecordCount: data['ecriture_count']
                                }
                }
                $dfd.resolve(dict_data);
             },
             error: function () {
                $dfd.reject();
             }
         });
    });
}

ApiRest.prototype.createData = function(postData) {
    //https://github.com/hikalkan/jtable/issues/64
    var jsonData = {};
    $.map(postData, function(n, i) {
                        jsonData[n['name']] = n['value'];
                    });
    return $.Deferred(function ($dfd) {
        $.ajax({
            url: 'http://localhost:8080/' + uriRest,
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify(jsonData)
            }).done(function(data, textStatus, jqXHR){
                if (jqXHR.status == 201) {
                    dict_data = {
                                    Result: "OK",
                                    Record: data
                                }
                    $dfd.resolve(dict_data);
                }
                else {
                    $dfd.reject();
                }
            }).fail(function(jqXHR, textStatus, errorThrown){
                $dfd.reject();
            });
        });
}

ApiRest.prototype.updateData = function(postData) {
    var jsonData = {};
    $.map(postData, function(n, i) {
                        jsonData[n['name']] = n['value'];
                    });
    return $.Deferred(function ($dfd) {
        $.ajax({
            url: 'http://localhost:8080/' + uriRest + '/' + jsonData['id'],
            type: 'PUT',
            dataType: 'json',
            data: JSON.stringify(jsonData),
            success: function (data) {
                dict_data = {
                                Result: "OK",
                            }
                $dfd.resolve(dict_data);
            },
            error: function () {
                $dfd.reject();
            }
            });
        });
}

ApiRest.prototype.deleteData = function(postData) {
    return $.Deferred(function ($dfd) {
        $.ajax({
            url: 'http://localhost:8080/' + uriRest + '/' + postData['id'],
            type: 'DELETE',
            dataType: 'json',
            success: function (data) {
                dict_data = {
                                Result: "OK",
                            }
                $dfd.resolve(dict_data);
            },
            error: function () {
                $dfd.reject();
            }
            });
        });
}

function ApiChildRest(uri) {
}

ApiChildRest.prototype.listData = function(postData, jtParams) {
    return $.Deferred(function ($dfd) {
        if (window.idRest === undefined) {
            idChildRest="";
        }
        $.ajax({
             url: 'http://localhost:8080/' + uriChildRest + '/' + idChildRest,
             type: 'GET',
             dataType: 'json',
             success: function (data) {
                dict_data = {
                                Result: "OK",
                                Records: data,
                                TotalRecordCount: data['ecriture_count']
                            }
                $dfd.resolve(dict_data);
             },
             error: function () {
                $dfd.reject();
             }
         });
    });
}
