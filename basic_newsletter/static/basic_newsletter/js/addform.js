
function updateElementIndex(el, prefix, ndx) {
   
	var id_regex = new RegExp('(' + prefix + '-\\d+)');
	var replacement = prefix + '-' + ndx;

	if (el.id) el.id = el.id.replace(id_regex, replacement);
	if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function weightUpdate(prefix){

    var section = $('#id_'+prefix + ' ul');
    
    $( section.children('li') ).each(function(count) { 
        $(this).find($(".story-weight input")).val( count );
    });
}

function idUpdate(prefix, btn, formCount){
    var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    var initialCount = parseInt($('#id_' + prefix + '-INITIAL_FORMS').val());

    var section = $('#id_'+prefix + ' ul');
    var count = initialCount;
   
    if(formCount >= initialCount){
       
        $( section.children('li') ).each(function(count) {
            console.log('count ' + count);
            if( $(this).find($("[id$='-id']")).val() == ''){
                console.log('here');
                updateElementIndex(this, prefix, count);
                    ($(this).children().children()).each(function() {
                    updateElementIndex(this, prefix, count);
                });
            }
        });
    }
  
    weightUpdate(prefix);
    
}

function addForm(btn, prefix) {
    var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    var row = ($('#id_' + prefix + ' .dynamic-form:first')).clone(true).get(0);
    
    $(row).insertAfter($('#id_' + prefix + ' .dynamic-form:visible:last'));

    $(row).children().each(function(){
        var elementClass = $(this).attr("class");

        if(elementClass == 'story-image-preview'){
            $(this).children().remove();
            $(this).prepend('<div class="image-spacer">Upload an image with a ratio of 260px by 100px</div>');
        }
        else if(elementClass == 'story-image'){
            $(this).children().remove();
            $(this).text('');
            $(this).append('<div class="error-message"></div><input id="id_secondary-3-image" name="secondary-3-image" type="file">');
        }
    });

    $(row).children().children().each(function() {
        $(this).val('');
    });

   idUpdate(prefix, row);

    $('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);
    return false;
}

function deleteForm(btn, prefix) {
    var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    var section = $('#id_'+prefix + ' ul');
    var items = $( section.children('li:visible') ).length;
    var row = $(btn).parents('#id_' + prefix + ' .dynamic-form');
    
    if(items == 1){
        var newRow = ($('#id_' + prefix + ' .dynamic-form')).clone(true).get(0);
        $(newRow).insertBefore(row);

        $(newRow).children().each(function(){
            
            var elementClass = $(this).attr("class");

            if(elementClass == 'story-image-preview'){
                $(this).children().remove();
                $(this).prepend('<div class="image-spacer">Upload an image with a ratio of 260px by 100px</div>');
            }
            else if(elementClass == 'story-image'){
                $(this).children().remove();
                $(this).text('');
                $(this).append('<div class="error-message"></div><input id="id_secondary-3-image" name="secondary-3-image" type="file">');
            }
        });

        $(newRow).children().children().each(function() {
            $(this).val('');
        });
        $(newRow).find($("[id$='-weight']")).val( 0 );
    }

    if(row.find($("[id$='-id']")).val() != ''){
        section.append(row);
        $(btn).parents('#id_' + prefix + ' .dynamic-form').hide();
        $(btn).next().attr('checked', true);
    }
    else{
        $(btn).parents('#id_' + prefix + ' .dynamic-form').remove();
        idUpdate(prefix);
        $('#id_' + prefix + '-TOTAL_FORMS').val(formCount - 1);
    }

    return false;
}


$(document).ready(function () {
  var sortables = $(".sortable");
  sortables.sortable({
    placeholder: "highlight",
    stop: function (event, ui) {
        var section = ($(this).parent().attr('id'));
        var prefix = section.slice(3);
        weightUpdate(prefix);
    }
  });

  sortables.disableSelection();

  $('.add-story').click(function () {
    var prefix = $(this).data('prefix');
    return addForm(this, prefix);
  });

  $('.delete-story').click(function () {
    var prefix = $(this).data('prefix');
    return deleteForm(this, prefix);
  });

});
