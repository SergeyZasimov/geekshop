window.onload = function() {

	$('.basket_list').on('change', 'input[type="number"]', function(){
		update_basket_list(event.target)
	});

    $('.basket_list').on('click', 'input[type="number"]', function(){
		update_basket_list(event.target)
	});

	function update_basket_list(target_href){
		// let target_href = event.target;
		if(target_href) {
			$.ajax({
				url: "/basket/edit/" + target_href.name + "/" + target_href.value + "/",
				success: function(data) {
					$('.basket_list').html(data.result);
					console.log('ajax done');
					},
				});
			};
		event.preventDefault();
	};
};
