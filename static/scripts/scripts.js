


$( document ).ready(function() {


	var box = {select: '',price: ''};
	var stuff_1 = {select: '',price: ''};
	var stuff_2 = {select: '',price: ''};
	var stuff_bonus = {select: '',price: ''};
	var stuff_pockets = {select: '',price: ''};
	var delivery = {select: '',price: ''};
	var payment = {select: ''};

	$("input:radio").change(setInputRadio);
	$("input:checkbox").change(setInputCheckbox);


	function setInputRadio()
	{
		var name = $(this).attr("name");
		var id = $(this).attr("id");
		var value = $(this).attr("value");
		var price = $(this).siblings('span').text();

		selectRadioObj($(this), name, value, price);
	}

	function setInputCheckbox()
	{
		var name = $(this).attr("name");
		var id = $(this).attr("id");
		var value = $(this).attr("value");

		selectCheckboxObj($(this), name);
	}

	function selectRadioObj(obj, name, value, price)
	{
		$("#"+name+" .form-radio").removeClass('form-radio-active');
		obj.parent().addClass('form-radio-active');

		// console.log('#total #'+name+'_line b - '+value+';')
		// console.log('#total #'+name+'_line .price - '+value+';')
		$('#total #'+name+'_line b').text(value);
		$('#total #'+name+'_line .price').text(price);
	}

	function selectCheckboxObj(obj, name)
	{
		if (obj.parent().hasClass('form-checkbox-active'))
			$("#"+name+" .form-radio").removeClass('form-checkbox-active');	
		else
			obj.parent().addClass('form-checkbox-active');
	}





});

