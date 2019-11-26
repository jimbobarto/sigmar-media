$(document).ready(function() {	
	$(function() {
		$("li[name='menu-item']").on("click",function() {
			$("li[name='menu-item']").each( function(index, menuItem) {
				$(menuItem).removeClass('selected');
			});
			$(this).addClass('selected');

			payload = {'content': $(this).attr('content')};
			$.post($SCRIPT_ROOT + '/get_content', JSON.stringify(payload), function(data) {
		      	$("div[id='content-container']").html(data);
				initialiseDatePicker();
		  	});

		});
	});

});

function initialiseDatePicker() {
	$( "#scheduled_date" ).datetimepicker({hour: 17, dateFormat: 'dd/mm/yy'});
}

function setMaximumCharacters() {
	$("#body").keyup( function() {
		if ($("#maximum_characters").val() > 0) {
			var entered_characters = $("#body").val().length;
			$("#count-container").html(entered_characters + '/' + $("#maximum_characters").val());
		}
	});	
}

function addCascadingSelection() {
	$('input[in_channel_hierarchy="true"]').change(function() {
		var newValue = $(this).prop('checked');
		$(this).closest('div.parent').find('input[in_channel_hierarchy="true"]').each( function(index, channelCheckbox) {
			$(channelCheckbox).prop('checked', newValue);
		});
	});   
}

function renderCalendar() {
	var calendarElement = document.getElementById('calendar');

	if (calendarElement !== null) {
		var calendar = new FullCalendar.Calendar(calendarElement, {
			plugins: [ 'dayGrid', 'interaction' ],
			events: '/get_events',
			height: 700,
			eventTimeFormat: { // like '14:30:00'
				hour: '2-digit',
				minute: '2-digit',
				hour12: false
			},
			dateClick: function(info) {
				$( "#date_display" ).html(info.dateStr);
				$( "#calendar_dialog" ).dialog({position: {my: "center", at: "center", of: window}});
			},
			eventClick: function(info) {
				eventClick(info);
			}
		});

		calendar.render();
	}
};

function eventClick(info) {
	$.get($SCRIPT_ROOT + '/event', info.event.extendedProps, function(data) {
		populateEventDialog(data.message.title, data.message.body, data.dateTime, data.channels);
		$( "#event_dialog" ).dialog({
			buttons: [
				{
					text: "Delete",
					click: function() {
						var this_dialog = $(this);
						$.ajax({
						    url: $SCRIPT_ROOT + '/event?file=' + info.event.extendedProps.file,
						    type: 'DELETE',
						    success: function(result) {
						        this_dialog.dialog( "close" );
						        info.event.remove();
						    }
						});
					}
				}
			]
		});
	});
}

function populateEventDialog(title, message, timestamp, channels) {
	var channelHtml = "";
	$.each( channels, function( index, element ){
		channelHtml += element + "<br/>";
	});

	$('#event_title').html(title);
	$('#event_message').html(message);
	$('#event_timestamp').html(timestamp);
	$('#event_channels').html(channelHtml);
}

function getPayload(title, body, channelElementSelector) {
	var payload = {'channels': [], 'message': {'title': title, 'body': body}};
	$(channelElementSelector).each( function(index, channelCheckbox) {
		if ($(channelCheckbox).prop('checked') == true) {
			payload['channels'].push($(channelCheckbox).attr('path')); 
		}
	});

	return payload;
}

function channelSelected() {
	var channelsSelected = false
	$('input[in_channel_hierarchy="true"]').each( function() {
		if ($(this).prop('checked')) {
			channelsSelected = true;
		}
	});   
	return channelsSelected;
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

	var channelsSelected = channelSelected()
	if (!channelsSelected) {
		alert("No channels selected");
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
