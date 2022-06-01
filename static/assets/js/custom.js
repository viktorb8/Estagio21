$(document).ready(function() {
	var max_fields      = 5; //maximum input boxes allowed
	var wrapper   		= $(".controls"); //Fields wrapper
	var add_button      = $(".add_field_button"); //Add button ID

	var x = 1; //initial text box count
	$(add_button).click(function(e){ //on add input button click
		e.preventDefault();
		if(x < max_fields){ //max input box allowed
			x++; //text box increment
			$(wrapper).append('<div class="input-group-append mb-3"><input type="text" name="colaborador_projeto_'+x+'" class="form-control col-8" maxlength="200"><div class="input-group-append col-4"><button class="btn-danger btn-lg add_field_button fas fas fa-minus-square fa-lg remove_field" type="button"></button></div></div>'); //add input box
		}
	});

	$(wrapper).on("click",".remove_field", function(e){ //user click on remove text
		e.preventDefault(); $(this).parent('div').parent('div').remove(); x--;
	})
});