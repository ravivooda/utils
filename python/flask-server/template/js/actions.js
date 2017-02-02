var selectedPlace;

function addNewListing(){
    var error = false;

    var house_contras = $('textarea#house-cons').val();
    if (!house_contras) {
	error = true;
    }

    var house_pros = $('textarea#house-pros').val();
    if (!house_pros){
	error = true;
    }

    var house_cautions = $('textarea#house-cautions').val();
    // House Cautions can be empty

    var house_parking = $('textarea#house-parking').val();
    if (!house_parking) {
	error = true;
    }

    var house_p_transit = $('textarea#house-p-transport').val();
    if (!house_p_transit){
	error = true;
    }

    var house_amenities = $('textarea#house-amenities').val();
    if (!house_amenities){
	error = true;
    }

    var house_details = $('textarea#house-details').val();
    if (!house_details){
	error = true;
    }

    var house_memory = $('textarea#house-b-memory').val();
    if (!house_memory) {
	error = true;
    }

    if (selectedPlace == null){
	error = true;
    }

    if (error) {
	//alert("An error occurred");
    }

    $.ajax({
	url : "/add",
	type: "POST",
	data: {
	    'contras': house_contras,
	    'pros': house_pros,
	    'cautions': house_cautions,
	    'parking': house_parking,
	    'transit': house_p_transit,
	    'amenities': house_amenities,
	    'details': house_details,
	    'memory': house_memory
	},
	dataType: "json",
	success: function(result){
	    alert("Successfully posted!: " + result)
	},
	error: function(xhr, aOptions, error){
	    alert("Some error: " + xhr.status);
            alert(error);
	}
    })
}
