jQuery(function($){
    $( "#select2-filterby" ).select2( { placeholder: "Select a category", maximumSelectionSize: 6 } );
    $( "#filterby" ).on( "click", function() {
        $( this ).parent().nextAll( "select" ).select2( "enable", this.checked );
    });
})
