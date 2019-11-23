$(document).ready(function() {
	$('input[in_channel_hierarchy="true"]').change(function() {
		var newValue = $(this).prop('checked');
		$(this).closest('div.parent').find('input[in_channel_hierarchy="true"]').each( function(index, channelCheckbox) {
			$(channelCheckbox).prop('checked', newValue);
		});
	});   

	$(function() {
		$("li[name='menu-item']").on("click",function() {
			$("li[name='menu-item']").each( function(index, menuItem) {
				$(menuItem).removeClass('selected');
			});
			$(this).addClass('selected');

			payload = {'content': $(this).attr('content')};
			$.post($SCRIPT_ROOT + '/get_content', JSON.stringify(payload), function(data) {
		      	$("div[id='content-container']").html(data);
		  	});

		});
	});

	$(function() {
		$( "#scheduled_date" ).datetimepicker({hour: 16});
	});

	$(function() {
		$("#body").keyup( function() {
			if ($("#maximum_characters").val() > 0) {
				var entered_characters = $("#body").val().length;
				$("#count-container").html(entered_characters + '/' + $("#maximum_characters").val());
			}
		});
	});


});

function renderCalendar() {
	var calendarElement = document.getElementById('calendar');

	if (calendarElement !== null) {
		var calendar = new FullCalendar.Calendar(calendarElement, {
			plugins: [ 'dayGrid', 'interaction' ],

			dateClick: function(info) {
				$( "#date_display" ).html(info.dateStr);
				$( "#calendar_dialog" ).dialog({position: {my: "center", at: "center", of: window}});
			}
		});


		calendar.render();
	}
};

function getPayload(title, body, channelElementSelector) {
	var payload = {'channels': [], 'message': {'title': title, 'body': body}};
	$(channelElementSelector).each( function(index, channelCheckbox) {
		if ($(channelCheckbox).prop('checked') == true) {
			payload['channels'].push($(channelCheckbox).attr('path')); 
		}
	});

	return payload;
}

function submit(title, body, channelElementSelector, submitDateTime, postImmediately) {
	if (postImmediately && submitDateTime.length > 0) {
		alert("You're trying to post immediately but you've specified a date/time");
		return;
	}

	if (!postImmediately && submitDateTime.length == 0) {
		alert("You're trying to schedule a post but you haven't specified a date/time");
		return;
	}


	var payload = getPayload(title, body, channelElementSelector);
	if (submitDateTime.length > 0) {
		payload['dateTime'] = submitDateTime;
	}

	if (postImmediately) {
		$.post($SCRIPT_ROOT + '/post_message', JSON.stringify(payload), function(data) {
	      	$('div.results-container').prepend(data);
	  	});
	}
	else {
		$.post($SCRIPT_ROOT + '/schedule_message', JSON.stringify(payload), function(data) {
	      	$('div.results-container').prepend(data);
	  	});
	}
}
