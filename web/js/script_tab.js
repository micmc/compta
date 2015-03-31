
 var data='';
 var pre_tr_id=false;
  var action = '';
  var savebutton = "<input type='button' class='ajaxsave' value='Save'>";
  var updatebutton = "<input type='button' class='ajaxupdate' value='Update'>";
  var cancel = "<input type='button' class='ajaxcancel' value='Cancel'>";
  var emailfilter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;	
   var pre_tds; 
var field_arr = new Array('text','text','text','text');
  var field_pre_text= new Array('Enter Firstname','Enter lastname','Enter technology domain','Enter Email Address');
  var field_name = new Array('fname','lname','domain','emailid'); 
 $(function(){
 $.ajax({
	     url:"DbManipulate.php",
                  type:"POST",
                  data:"actionfunction=showData",
        cache: false,
        success: function(response){
		 
		  $('#demoajax').html(response);
		  createInput();
		  
		}
		
	   });
 
  
 $('#demoajax').on('click','.ajaxsave',function(){
     
	   var fname =  $("input[name='"+field_name[0]+"']");
	   var lname = $("input[name='"+field_name[1]+"']");
	   var domain =$("input[name='"+field_name[2]+"']");
	   var email = $("input[name='"+field_name[3]+"']");
	   if(validate(fname,lname,domain,email)){
	   data = "fname="+fname.val()+"&lname="+lname.val()+"&domain="+domain.val()+"&email="+email.val()+"&actionfunction=saveData";
       $.ajax({
	     url:"DbManipulate.php",
                  type:"POST",
                  data:data,
        cache: false,
        success: function(response){
		   if(response!='error'){
		      $('#demoajax').html(response);
		  createInput();
		     }
		}
		
	   });
      }	
      else{
	   return;
	  }	  
	   });
 $('#demoajax').on('click','.ajaxedit',function(){
      var edittrid = $(this).parent().parent().attr('id');
        if(pre_tr_id){
	    alert("update or cancel previous one");
	    return false;
	}
	pre_tr_id = true;
    	var tds = $('#'+edittrid).children('td');
        var tdstr = '';
		var td = '';
		pre_tds = tds;
		
		for(var j=0;j<field_arr.length;j++){
		   
		     tdstr += "<td><input type='"+field_arr[j]+"' name='"+field_name[j]+"' value='"+$(tds[j]).html()+"' placeholder='"+field_pre_text[j]+"'></td>";
		  }
		  tdstr+="<td>"+updatebutton +" " + cancel+"</td>";
		  $('#createinput').remove();
		  $('#'+edittrid).html(tdstr);
	   });
	   
	   $('#demoajax').on('click','.ajaxupdate',function(){
       var edittrid = $(this).parent().parent().attr('id');
	   var fname =  $("input[name='"+field_name[0]+"']");
	   var lname = $("input[name='"+field_name[1]+"']");
	   var domain =$("input[name='"+field_name[2]+"']");
	   var email = $("input[name='"+field_name[3]+"']");
	   if(validate(fname,lname,domain,email)){
	   data = "fname="+fname.val()+"&lname="+lname.val()+"&domain="+domain.val()+"&email="+email.val()+"&editid="+edittrid+"&actionfunction=updateData";
       $.ajax({
	     url:"DbManipulate.php",
                  type:"POST",
                  data:data,
        cache: false,
        success: function(response){
		   if(response!='error'){
		      $('#demoajax').html(response);
		      pre_tr_id=false;
		  createInput();
		     }
		}
		
	   });
}
else{
return;
}	   
	   });
	   	   $('#demoajax').on('click','.ajaxdelete',function(){
       var edittrid = $(this).parent().parent().attr('id');
	   
	   data = "deleteid="+edittrid+"&actionfunction=deleteData";
       $.ajax({
	     url:"DbManipulate.php",
                  type:"POST",
                  data:data,
        cache: false,
        success: function(response){
		   if(response!='error'){
		      $('#demoajax').html(response);
		  createInput();
		     }
		}
		
	   });	   
	   });
 $('#demoajax').on('click','.ajaxcancel',function(){
      var edittrid = $(this).parent().parent().attr('id');
	  
        $('#'+edittrid).html(pre_tds);
		createInput();
		pre_tr_id=false;
	   });	   
	   });
	   
 function createInput(){
     
      
  var blankrow = "<tr id='createinput'>";   
  for(var i=0;i<field_arr.length;i++){
	  blankrow+= "<td class='ajaxreq'><input type='"+field_arr[i]+"' name='"+field_name[i]+"' placeholder='"+field_pre_text[i]+"' /></td>";
	}
	blankrow+="<td class='ajaxreq'>"+savebutton+"</td></tr>";
  $('#demoajax').append(blankrow);	
      
  }
function validate(fname,lname,domain,email){
var contact = jQuery('input[name=contact]');
		
		
		if (fname.val()=='') {
			fname.addClass('hightlight');
			return false;
		} else fname.removeClass('hightlight');
		if (lname.val()=='') {
			lname.addClass('hightlight');
			return false;
		} else lname.removeClass('hightlight');
		if (domain.val()=='') {
			domain.addClass('hightlight');
			return false;
		} else domain.removeClass('hightlight');
		
		if (email.val()=='') {
			email.addClass('hightlight');
			return false;
		}else if(!emailfilter.test(email.val())){
		   alert("not a valid email id");
		   email.addClass('hightlight');
		   return false;
		}else email.removeClass('hightlight');
		
		return true;
		
}
