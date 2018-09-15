/* Javascript for DSPXBlock. */

function parseTextSignal(signal_string) {
    var signal_array = signal_string.replace('[', '').replace(']', '').replace('(', '').replace(')', '').split(/[ ,]+/);
    var cleaned_array = signal_array.filter(function (item) {
        return item != "";
    });
    signal_valid = cleaned_array.every((item) => !isNaN(parseFloat(item)));
    if (signal_valid && cleaned_array.length > 0) {
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