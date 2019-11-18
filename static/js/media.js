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
		$("td.fc-day").on("click",function() {
			//renderCalendar()
		});
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

function submit() {
	var payload = {'channels': [], 'message': {'title': $("input[id='title']").val(), 'body': $("textarea[id='body']").val()}};
	$('input[channel="True"]').each( function(index, channelCheckbox) {
		if ($(channelCheckbox).prop('checked') == true) {
			payload['channels'].push($(channelCheckbox).attr('path')); 
		}
	});

	$.post($SCRIPT_ROOT + '/post_message', JSON.stringify(payload), function(data) {
      	$('div.results-container').prepend(data);
  	});
}
