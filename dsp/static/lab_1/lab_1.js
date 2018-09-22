function DSPXBlock(runtime, element, data) {

    var student_submit = runtime.handlerUrl(element, 'student_submit');
    var get_graphics = runtime.handlerUrl(element, 'get_graphics');

    function build_graphics() {
        $("#graphic_1", element).html("<div style='background: #f3f3f2;width: 100%;height:330px;'></div>");
        $("#graphic_2", element).html("<div style='background: #f3f3f2;width: 100%;height:330px;'></div>");
        $.ajax({
            type: "POST",
            url: get_graphics,
            data: JSON.stringify(generateAnswer()),
            success: function (result) {
                $("#graphic_1", element).html(result["graphics"][0]["html"]);
                $("#graphic_2", element).html(result["graphics"][1]["html"]);
            },
            contentType: 'application/json; charset=utf-8'
        });
    }

    $(document).on('input', ".answer-input", function () {
        $(this).removeClass("dsp-incorrect-input");
        $(this).removeClass("dsp-correct-input");
    });

    $('#check_answer', element).click(function (event) {
        $.ajax({
            type: "POST",
            url: student_submit,
            data: JSON.stringify(generateAnswer()),
            success: function (result) {
                $(element).find('me-span.points').html(result.score);
                // $('me-span.points', element).text(result.score + ' из ' + result.maximum_score);
                console.log(result.correctness);
                Object.keys(result.correctness).forEach(function (item) {
                    console.log(item);
                    if (result.correctness[item]) {
                        $("#input_student_" + item.split("_")[0]).addClass("dsp-correct-input");
                    }
                    else {
                        $("#input_student_" + item.split("_")[0]).addClass("dsp-incorrect-input");
                    }
                })

            },
            contentType: 'application/json; charset=utf-8'
        });
    });

    $('#calculate_graphics', element).click(function (event) {
        build_graphics();
    });

    function generateAnswer() {
        var student_data = {
            "student_signal": [],
            "student_filter": [],
            "student_a": "",
            "student_window": "rectangular",
            "student_ubl": "",
            "student_p": ""
        };
        student_data.student_signal = parseTextSignal($("#input_student_signal", element).val()).signal;
        student_data.student_filter = parseTextSignal($("#input_student_filter", element).val()).signal;
        student_data.student_a = $("#input_student_a", element).val();
        student_data.student_window = $('input[name=input_student_window]:checked', element).val();
        student_data.student_ubl = $("#input_student_ubl", element).val();
        student_data.student_p = $("#input_student_p", element).val();
        return student_data;
    }

    function build_lab_state(data) {
        $("textarea#input_student_signal", element).val(data.student_signal);
        $("textarea#input_student_filter", element).val(data.student_filter);
        $("#input_student_a", element).val(data.student_a);
        $('input:radio[name="input_student_window"]', element).filter('[value="' + data.student_window + '"]').attr('checked', true);
        $("#input_student_ubl", element).val(data.student_ubl);
        $("#input_student_p", element).val(data.student_p);
        build_graphics();
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
        console.log("Array is valid? :", parse_array.signal_valid);
        console.log("Validation result:", parse_array);
        console.log(generateAnswer());
        $(input).parent().find(".validation-message").html(message)
    }

    $(function ($) {
        console.log(data);
        if (!Object.keys(data["student_state"]).length == false) {
            build_lab_state(data["student_state"]);
            $("textarea.array-input", element).each(function (i) {
                process_array_input(this);
            });

        }

        $("textarea.array-input", element).each(function (i) {
            // var validation_array_message = $('<div/>', {
            //     class: 'validation-message'
            // });
            // $(this).after(validation_array_message);
            $(this).change(function () {
                console.log(this);
                process_array_input(this);
            });
        });


    });

}