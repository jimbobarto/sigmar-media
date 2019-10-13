$(document).ready(function() {
	$('input[channel="channel"]').change(function() {
		var newValue = $(this).prop('checked');
		$(this).closest('div.parent').find('input[channel="channel"]').each( function(index, channelCheckbox) {
			$(channelCheckbox).prop('checked', newValue);
		});
	});   
});