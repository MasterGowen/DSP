/* Javascript for DSPXBlock. */

function parseTextSignal(signal_string) {
    var signal_array = signal_string.replace('[', '').replace(']', '').replace('(', '').replace(')', '').split(/[ ,]+/);
    var cleaned_array = signal_array.filter(function (item) {
        return item != "";
    });
    signal_valid = cleaned_array.every((item) => !isNaN(parseFloat(item)));
    if (signal_valid) {
        signal = cleaned_array.map(function (item) {
            return parseFloat(item)
        });
        return {"signal": signal, "signal_valid": signal_valid};
    }
    else {
        signal_valid = false;
        return {"signal": [], "signal_valid": signal_valid};
    }
}

function example_data() {
    var signal = "[1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]"
    var filter = "[1. 1. 1. 1. 1. 1. 1. 1. 1.]";
    var a = "1";
    var window = "hamming";

    $("textarea#input_student_signal").val(signal);
    $("textarea#input_student_filter").val(filter);
    $("#input_student_a").val(a);
    $('input:radio[name="input_student_window"]').filter('[value="' + window + '"]').attr('checked', true);
}

/*
function DSPXBlock(runtime, element) {

function updateCount(result) {
$('.count', element).text(result.count);
}

var handlerUrl = runtime.handlerUrl(element, 'increment_count');

$('p', element).click(function(eventObject) {
$.ajax({
    type: "POST",
    url: handlerUrl,
    data: JSON.stringify({"hello": "world"}),
    success: updateCount
});
});

$(function ($) {

});
}
*/