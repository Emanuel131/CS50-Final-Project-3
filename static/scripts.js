/*
function imageChange(value) {

	// Deal if nothing is choosen
	if (value == "") {
		return;
	}

	// Create new AJAX object
	var ajax = new XMLHttpRequest();
	
	ajax.onreadystatechange = function() {
		if (ajax.readyState == 4 && ajax.status == 200) {
			$("#img_row").html(ajax.responseText);
		}
	};	

	ajax.open("GET", '/' + value, true);
	ajax.send();
}
*/

$(document).ready(function() {
	$("button").click(function(event) {
		event.preventDefault();
		var value = $(this).val();
		var postData = {
			id: value
		}

		$.ajax({
			url: '/',
			type: 'POST',
			contentType: "application/json; charset=UTF-8",
			data: JSON.stringify(postData),
			success: function(response) {
				alert(value);
				//$('#left_pic').attr('src', '/static/Jobs2.jpg');
				//$('#right_pic').attr('src', '/static/Jobs.jpg');
				window.location.href = "/";
			},
			error: function(response) {
				alert("error");
			}
		});
	});
});