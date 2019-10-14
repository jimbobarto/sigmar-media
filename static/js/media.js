$(document).ready(function() {
	$('input[in_channel_hierarchy="true"]').change(function() {
		var newValue = $(this).prop('checked');
		$(this).closest('div.parent').find('input[in_channel_hierarchy="true"]').each( function(index, channelCheckbox) {
			$(channelCheckbox).prop('checked', newValue);
		});
	});   
});

function submit() {
	var payload = {'channels': [], 'message': {'title': $("input[id='title']").val(), 'body': $("input[id='body']").val()}};
	$('input[channel="True"]').each( function(index, channelCheckbox) {
		if ($(channelCheckbox).prop('checked') == true) {
			payload['channels'].push($(channelCheckbox).attr('path')); 
		}
	});

	$.post($SCRIPT_ROOT + '/post_message', JSON.stringify(payload), function(data) {
      	alert(data);
  	});
}

