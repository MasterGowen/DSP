/* Javascript for DSPXBlock. */

var max_arr_len = 1000;

function parseTextSignal(input) {
    var max_array_length = parseInt($(input).data('maxLength')) || max_arr_len;
    signal_string = $(input).val();
    var signal_array = signal_string.replace('[', '').replace(']', '').replace('(', '').replace(')', '').split(/[ ,\t\n]+/);
    var cleaned_array = signal_array.filter(function (item) {
        return item != "";
    });
    signal_valid = cleaned_array.every((item) => !isNaN(parseFloat(item)));
    if (signal_valid && cleaned_array.length < max_array_length) {
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
    var max_array_length = parseInt($(input).data('maxLength')) || max_arr_len;
    parse_array = parseTextSignal(input);
    var message = "";
    if (parse_array.signal_valid) {
        if (parse_array.signal.length > 0) {
            message = "<span>Введенный " + $(input).data('arrayType') + " (" + parse_array.signal.length + " " + counting_title(parse_array.signal.length) + "):</span> <br /> <p class='signal-highlight'>" + parse_array.signal.join(" ") + "</p>";
        }
        else {
            message = "<span class='error-text'>Введите " + $(input).data('arrayType') + "!</span>";
        }
    }
    else {
        message = "<span class='error-text'>Ошибка ввода " + $(input).data('arrayType') + "а!" + " Максимально допустимая длина " + $(input).data('arrayType') + "а составляет " + (max_array_length - 1) + " " +  counting_title(max_array_length - 1) + ".</span>";

    }
    $(input).parent().find(".validation-message").html(message)
}

function highlight_correctness(state) {
    Object.keys(state).forEach(function (item) {
        // console.log($("#input_student_" + item.split("_")[0]));
        // console.log(state[item], item);
        if (item.split("_")[item.split("_").length-1] == "correctness") {
            if (state[item] == true) {
                $("#input_student_" + item.split("_")[0]).removeClass("dsp-incorrect-input");
                $("#input_student_" + item.split("_")[0]).addClass("dsp-correct-input");
            }
            else {
                $("#input_student_" + item.split("_")[0]).removeClass("dsp-correct-input");
                $("#input_student_" + item.split("_")[0]).addClass("dsp-incorrect-input");
            }
        }

    })
}

function show_graphic_error(element) {
    var error_message = $('<div/>', {
        class: 'graphic-error',
        text: "При построении графика произошла ошибка.\nПроверьте правильность введенных данных.",
    });
    $(element).html(error_message)
}

function show_graphic_load(element) {
    var loading_message = $('<div/>', {
        class: 'graphic-loading',
        text: "Строим график ...",
    });
    $(element).html(loading_message)
}

function log_ajax_error(jqXHR, exception) {
    var msg = '';
    if (jqXHR.status === 0) {
        msg = 'Нет подключения к сети.\n Проверьте интернет-соединение.';
    } else if (jqXHR.status == 404) {
        msg = 'Запрашиваемый адрес не найден. Код ошибки: 404';
    } else if (jqXHR.status == 500) {
        msg = 'Внутренняя ошибка сервера. Код ошибки: 500';
    } else if (exception === 'parsererror') {
        msg = 'Requested JSON parse failed.';
    } else if (exception === 'timeout') {
        msg = 'Превышено время ожидания.';
    } else if (exception === 'abort') {
        msg = 'Ajax-соединение прервано.';
    } else {
        msg = 'Неизвестная ошибка.\n' + jqXHR.responseText;
    }
    console.error(msg);
}

function counting_title(number) {
    last_numeral = number.toString()[number.toString().length - 1];
    if ([11, 12, 13, 14].includes(number)){
        return "отсчётов";
    }

    if (["0", "5", "6", "7", "8", "9"].includes(last_numeral)) {
        return "отсчётов";
    }
    else if (["2", "3", "4"].includes(last_numeral)) {
        return "отсчёта";
    }
    else if (["1"].includes(last_numeral)) {
        return "отсчёт";
    }
    else {
        return "отсчётов";
    }
}


function example_data_lab_1() {
    var signal = "1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0";
    var filter = "1. 1. 1. 1. 1.";
    var a = "1";
    var p = "7";
    var ubl = "7";
    var window = "hamming";

    $("textarea#input_student_signal").val(signal);
    $("textarea#input_student_filter").val(filter);
    $("#input_student_a").val(a);
    $("#input_student_p").val(p);
    $("#input_student_ubl").val(ubl);
    $('input:radio[name="input_student_window"]').filter('[value="' + window + '"]').attr('checked', true);
}


function example_data_lab_3() {
    var signal = "[ 1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1. 1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]";
    var filter = "[ 1.  1.  1.  1.  1.  1.  1.  1.  1.  1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.]"
    $("textarea#input_student_signal").val(signal);
    $("textarea#input_student_filter").val(filter);

}


function example_data_lab_4() {
    var signal = "1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0";
    var filter = "1. 0.8";
    var b = "1";
    var F = "7";
    var Dp = "7";

    $("textarea#input_student_signal").val(signal);
    $("textarea#input_student_filter").val(filter);
    $("#input_student_b").val(b);
    $("#input_student_F").val(F);
    $("#input_student_Dp").val(Dp);
    // $('input:radio[name="input_student_window"]').filter('[value="' + window + '"]').attr('checked', true);
}

