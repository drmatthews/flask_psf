$(document).ready(function() {
  console.log("ready!");

  // on form submission ...
  $('form').on('submit', function() {

    console.log("the form has beeen submitted");

    // grab values
    model = $('select[name="model"] :selected').text();
    microscope = $('select[name="microscope"] :selected').text();
    ex_wavelen = $('input[name="ex_wavelen"]').val();
    em_wavelen = $('input[name="em_wavelen"]').val();
    num_aperture = $('input[name="num_aperture"]').val();
	refr_index = $('input[name="refr_index"]').val();
    console.log(microscope, model, ex_wavelen, em_wavelen, num_aperture, refr_index)
	$('#psfimg').hide();
    $.ajax({
      type: "POST",
      url: "/get_psf",
      data : { 'model': model, 'microscope': microscope, 
			   'ex_wavelen': ex_wavelen, 'em_wavelen': em_wavelen, 
		       'num_aperture': num_aperture, 'refr_index': refr_index },
      success: function(results) {
        console.log(results)
	    /*setTimeout(function() {
	        $('#psfimg').attr('src', results.url);
			$('#psfimg').show();
	    }, 500);*/
        $('#psfimg').attr('src', results.url)
		$('#psfimg').show()	
		$('#scope').html(results.microscope)
        $('#sigmaz').html(results.sigmaz)
		$('#sigmar').html(results.sigmar)
        $('#nyquistxy').html(results.nyquistxy)
		$('#nyquistz').html(results.nyquistz)
		$('#psf').show()
		$('#nyquist').show()
      },
      error: function(error) {
        console.log(error)
      }
    });
/*	$('#psfimg').hide();
	$.ajax({
	  type: 'GET',
	  cache: false,
	  url: Flask.url_for("update_psf",{"filename":"psf.png"}), 
	  success: function(resp){
	    $('#psfimg').attr('src', resp.url);
		console.log(resp.url);
	  },
      error: function(error) {
        console.log(error)
      }
	});
	$('#psfimg').show();*/
  });
});
