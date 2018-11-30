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
		var s1 = 0;
		var s2 = 0;
		var value = $(this).val();
		if (value == "left") {
			s1 = 1;
			s2 = 0
		} else {
			s1 = 0;
			s2 = 1;
		};

		var postData = {
			s1: s1,
			s2: s2
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