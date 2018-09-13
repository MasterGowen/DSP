function DSPXBlock(runtime, element) {

    function updateCount(result) {
    $('.count', element).text(result.count);
    }

    var student_data = {
        "student_signal": [],
        "student_filter": [],
        "a": "",
        "student_window": ""

    };

    var handlerUrl = runtime.handlerUrl(element, 'increment_count');

    var get_graphics = runtime.handlerUrl(element, 'get_graphics');

    $('p', element).click(function(eventObject) {
    $.ajax({
        type: "POST",
        url: get_graphics,
        data: JSON.stringify({"hello": "world"}),
        success: updateCount
    });
    });

    function generateAnswer(){
       student_data.student_signal =  parseTextSignal($("#input_student_signal").val()).signal;
       student_data.student_filter =  parseTextSignal($("#input_student_filter").val()).signal;
       student_data.a = $("#input_student_a").val()
    }

    $(function ($) {
        $("textarea.array-input").each(function(i) {
            var validation_array_message = $('<div/>', {
                class: 'validation-message'
            });
            $(this).after(validation_array_message);
            $(this).change(function () {
                parse_array = parseTextSignal(this.value);
                var message = "";
                if (parse_array.signal_valid) {
                    message = "Введенный сигнал: [" + parse_array.signal.join(" ") + "]";
                }
                else {
                    message = "Ошибка формата ввода";

                }
                console.log("Array is valid? :", parse_array.signal_valid);
                console.log("Validation result:", parse_array);
                $(this).parent().find(".validation-message").html(message)
            });
        });


    });

}