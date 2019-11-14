jQuery(document).ready(function($){

var input_row = ('<div class="added-row"><input type="text" class="form-control students_names" placeholder="Nombre del alumno" required id="students_names"><input type="text" class="form-control students_ids" placeholder="Id del alumno" id="students_ids"><button class="del">Eliminar Alumno</button></div>')

$(document).on('click','.add', function(){
$(input_row).insertAfter('.main-row');
});
$(document).on('click','.del', function(){
$(this).parents('.added-row').remove();
});

});

$("form").submit(function(){
    $('form').css("display","none");
    $('.loading').css("display","block");
    var textVal = "";
    $('.students_names').each(function(i, obj) {
        if(i != $('.students_names').length-1)
        {
          textVal = textVal + $(this).val() + "#";
        }else{
          textVal = textVal + $(this).val();
        }
    });
    $("#students_names").val(textVal);
    var textVal = "";
    $('.students_ids').each(function(i, obj) {
      if(i != $('.students_ids').length-1)
      {
        textVal = textVal + $(this).val() + "#";
      }else{
        textVal = textVal + $(this).val();
      }
    });
    $("#students_ids").val(textVal);
});
