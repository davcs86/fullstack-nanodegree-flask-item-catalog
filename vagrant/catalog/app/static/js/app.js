jQuery(function($){
    // Index functions
    var cachedValues;
    $('#select2-filterby').select2({
        placeholder: 'Select any category',
        maximumSelectionSize: 6,
        width: '100%'
    });
    $('.goto-pagination').click(function(evt){
        evt.preventDefault();
        // update the page and submit the Form
        $('#page_field').val($(this).data('page'));
        $('#index_form').trigger('submit');
    });
    $('.form-delete').submit(function(evt){
        if (!confirm('Are you sure of delete this item?')){
            evt.preventDefault();
        }
    })
    // Create item functions
    window.tagSelSettings = {
        tags: true,
        maximumSelectionSize: 12,
        createTag: function (input) {
            var term = slugify(input.term);
            if (term === '') {
                return null;
            }
            return {
              id: '0|'+term, // create empty tag
              text: term
            };
        }
    };
    $('.select2-tags').select2(window.tagSelSettings).on('select2:selecting', function(evt){
        var data = evt.params.args.data;
        if (data.text.length < 3){
            alert('Categories must have 3 characters at least');
            $('.select2-tags').select2(window.tagSelSettings).trigger('close');
            return false;
        }
    }).on('select2:unselecting', function (e) {
        // Taken from http://stackoverflow.com/a/32336094/2423859
        if ($(e.params.args.originalEvent.currentTarget).hasClass('select2-results__option')){
            e.preventDefault();
            // close the dropdown
            $('.select2-tags').select2(window.tagSelSettings).trigger('close');
        }
    });

    function slugify(text) {
        // Taken from https://gist.github.com/mathewbyrne/1280286
        return text.toString().toLowerCase()
            .replace(/\s+/g, '-')           // Replace spaces with -
            .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
            .replace(/\-\-+/g, '-')         // Replace multiple - with single -
            .replace(/^-+/, '')             // Trim - from start of text
            .replace(/-+$/, '');            // Trim - from end of text
    }

    window.createPreviews = function(previewUrl) {
        var previewArr = [];
        if (typeof(previewUrl)!='undefined'){
            previewArr.push("<img src='"+previewUrl+"' class='file-preview-image' alt='Item picture' title='Item picture'>");
        }
        $('#item-picture').fileinput({
            'showUpload': false,
            'previewFileType': 'image',
            'allowedFileTypes': ['image'],
            'initialPreview': previewArr
        }).on('fileclear', function() {
            $('#picture_status').val(2); // remove the image
        }).on('fileimageloaded', function() {
            $('#picture_status').val(1); // modify the image
        });
    }

})
