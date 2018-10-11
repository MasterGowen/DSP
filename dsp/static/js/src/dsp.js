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

function process_array_input(input) {
    parse_array = parseTextSignal(input.value);
    var message = "";
    if (parse_array.signal_valid) {
        if (parse_array.signal.length > 0) {
            message = "<span>Введенный " + $(input).data('arrayType') + " (" + parse_array.signal.length + " отсчётов):</span> <br /> <span class='signal-highlight'>" + parse_array.signal.join(" ") + "</span>";
        }
        else {
            message = "<span>Введите сигнал!</span>";
        }
    }
    else {
        message = "<span class='error-text'>Ошибка формата ввода " + $(input).data('arrayType') + "а!</span>";

    }
    $(input).parent().find(".validation-message").html(message)
}

function highlight_correctness(state) {
    Object.keys(state).forEach(function (item) {
        console.log(item);
        if (state[item] == true) {
            $("#input_student_" + item.split("_")[0]).addClass("dsp-correct-input");
        }
        else {
            $("#input_student_" + item.split("_")[0]).addClass("dsp-incorrect-input");
        }
    })
}

function show_graphic_error(element){
    var error_message = $('<div/>', {
        class: 'graphic-error',
        title: 'При построении графика произошла ошибка. Проверьте праввильность введенных данных.'
    }).appendTo(element.find('div'));


}

function example_data_lab_1() {
    var signal = "[1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]"
    var filter = "[1. 1. 1. 1. 1. 1. 1. 1. 1.]";
    var a = "1";
    var window = "hamming";

    $("textarea#input_student_signal").val(signal);
    $("textarea#input_student_filter").val(filter);
    $("#input_student_a").val(a);
    $('input:radio[name="input_student_window"]').filter('[value="' + window + '"]').attr('checked', true);
}
