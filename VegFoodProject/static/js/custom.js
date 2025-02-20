let autocomplete;

function initAutoComplete(){
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            //default in this app is "IN" - add your country code
            componentRestrictions: {'country': ['in']},
        })
    // function to specify what should happen when the prediction is clicked
    autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        // console.log('place name=>', place.name)
    }

    // get the address components and assign them to the fields
    // console.log(place);
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_address').value

    geocoder.geocode({'address': address}, function(results, status){
        // console.log('results=>', results)
        // console.log('status=>', status)
        if(status == google.maps.GeocoderStatus.OK){
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            // console.log('lat=>', latitude);
            // console.log('long=>', longitude);
            $('#id_latitude').val(latitude);
            $('#id_longitude').val(longitude);

            $('#id_address').val(address);
        }
    });

    // loop through the address components and assign other address data
    console.log(place.address_components);
    for(var i=0; i<place.address_components.length; i++){
        for(var j=0; j<place.address_components[i].types.length; j++){
            // get country
            if(place.address_components[i].types[j] == 'country'){
                $('#id_country').val(place.address_components[i].long_name);
            }
            // get state
            if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                $('#id_state').val(place.address_components[i].long_name);
            }
            // get city
            if(place.address_components[i].types[j] == 'locality'){
                $('#id_city').val(place.address_components[i].long_name);
            }
            // get pincode
            if(place.address_components[i].types[j] == 'postal_code'){
                $('#id_pin_code').val(place.address_components[i].long_name);
            }else{
                $('#id_pin_code').val("");
            }
        }
    }

}


//add to cart
$(document).ready(function () {
    $('.add_to_cart').on('click',function (e) {
        e.preventDefault();
        food_id=$(this).attr('data-id');
        url=$(this).attr('data-url');

        $.ajax({
            type:'GET',
            url:url,
       
            success:function (response) {
                if(response.status=='login_required'){
                    swal(response.message,'','info').then(function(){
                        window.location='/login'
                    })
                    
                }else if(response.status=='Failed'){
                    swal(response.message,'','error')
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(response.qty)
                    Totalamount(response.cart_amount['subtotal'],response.cart_amount['tax'],response.cart_amount['total'])
                }
            }
        });
        
    });


    // place cart item quantity on load
    $('.item_qty').each(function () {
        var item_id=$(this).attr('id');
        var qty=$(this).attr('data-qty');
        $('#'+item_id).html(qty);

    });
   
    //decrease cart   
    $(document).ready(function () {
        $('.decrease_cart').on('click',function (e) {
            e.preventDefault();
            food_id=$(this).attr('data-id');
            url=$(this).attr('data-url');
            cart_id=$(this).attr('id');

            $.ajax({
                type:'GET',
                url:url,
            
                success:function (response) {
                    if(response.status=='login_required'){
                        swal(response.message,'','info').then(function(){
                            window.location='/login'
                        })
                        
                    }else if(response.status=='Failed'){
                        swal(response.message,'','error')
                    }else{
                        $('#cart_counter').html(response.cart_counter['cart_count'])
                        $('#qty-'+food_id).html(response.qty)
                        
                        if(window.location.pathname=="/cart/"){
                            removeCartItem(response.qty,cart_id)
                            checkEmptycart()
                            Totalamount(response.cart_amount['subtotal'],response.cart_amount['tax'],response.cart_amount['total'])
                        }
                    }
                }
            });
            
        });
    });


    //Delete cart item   
    $(document).ready(function () {
        $('.delete_cart').on('click',function (e) {
            e.preventDefault();

            cart_id=$(this).attr('data-id');
            url=$(this).attr('data-url');

            $.ajax({
                type:'GET',
                url:url,
            
                success:function (response) {
                    if(response.status=='Failed'){
                        swal(response.message,'','error')
                    }else{
                        $('#cart_counter').html(response.cart_counter['cart_count'])
                        swal(response.status,response.message,"success")
                        removeCartItem(0,cart_id)
                        checkEmptycart()
                        Totalamount(response.cart_amount['subtotal'],response.cart_amount['tax'],response.cart_amount['total'])
                        
                    }
                }
            });
            
        });
    });

    //delete cart element if qty is 0

    function removeCartItem(cartitemqty,cart_id){
       
        if(cartitemqty<=0){
            document.getElementById("cart-item-"+cart_id).remove()
        }
    
    }

    //check empty cart
    function checkEmptycart(){
        var cartcounter=document.getElementById('cart_counter').innerHTML
        if(cartcounter==0){
            document.getElementById('empty-cart').style.display="block";
        }
    }

    function Totalamount(subtotal,tax,total){
        if(window.location.pathname=="/cart/"){
            $('#subtotal').html(subtotal)
            $('#tax').html(tax)
            $('#total').html(total)
        }

    }

    $('.add_hour').on('click',function(e){
        e.preventDefault();
        var day=document.getElementById("id_day").value
        var from_hour=document.getElementById("id_from_hour").value
        var to_hour=document.getElementById("id_to_hour").value
        var is_closed=document.getElementById("id_is_closed").checked
        var csrf_token=$('input[name=csrfmiddlewaretoken]').val()
        var url=document.getElementById("add_hour_url").value

        if(is_closed){
            is_closed='True'
            condition="day!=''"
        }else{
            is_closed='False'
            condition="day!='' && from_hour!='' && to_hour!=''"
        }
        if(eval(condition)){
            $.ajax({
                type:'POST',
                url:url,
                data:{
                    'day':day,
                    'from_hour':from_hour,
                    'to_hour':to_hour,
                    'is_closed':is_closed,
                    'csrfmiddlewaretoken':csrf_token
                },
                success:function(response){
                    if(response.status=="success"){
                        if(response.is_closed=="Closed"){
                            html='<tr id="hour-"'+response.id+'><td><b>'+response.day+'</b></td><td>Closed</td><td><a href="#" class="remove_hour" data-url="/vendor/opening_hour/remove/'+response.id+'/">Remove</a></td></tr>';
                        }
                        else{
                            html='<tr id="hour-"'+response.id+'><td><b>'+response.day+'</b></td><td>'+response.from_hour+' - '+response.to_hour+'</td><td><a href="#" class="remove_hour" data-url="/vendor/opening_hour/remove/'+response.id+'/">Remove</a></td></tr>';
                        }
                        
                        $(".opening_hours").append(html)
                        document.getElementById("opening_hours").reset();
                    }else{
                        swal(response.message,'','error')

                    }

                }
            })
        }else{
            swal("Please fill all fields",'','info')
        }

    })

    $('.remove_hour').on('click',function(e){
        e.preventDefault()
        url=$(this).attr('data-url')

        $.ajax({
            type:'GET',
            url:url,
            success:function(response){
                if(response.status=='success'){
                    document.getElementById('hour-'+response.id).remove()
                }

            }
        })
    
    })
});