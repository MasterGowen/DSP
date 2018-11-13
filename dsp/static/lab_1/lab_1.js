function DSPXBlock(runtime, element, data) {

    var student_submit = runtime.handlerUrl(element, 'student_submit');
    var save_answer = runtime.handlerUrl(element, 'save_answer');
    var get_graphics = runtime.handlerUrl(element, 'lab_1_get_graphics');
    var reset_task = runtime.handlerUrl(element, 'reset_task');
    var highlight_correct = true;

    function build_graphics() {
        disable($('#calculate_graphics', element));
        show_graphic_load($('#graphic_1', element));
        show_graphic_load($('#graphic_2', element));
        $.ajax({
            type: "POST",
            url: get_graphics,
            data: JSON.stringify(generateAnswer()),
            success: function (result) {
                $("#graphic_1", element).html(result["graphics"][0]["html"]);
                $("#graphic_2", element).html(result["graphics"][1]["html"]);
                enable($('#calculate_graphics', element));
            },
            error: function (jqXHR, exception) {
                show_graphic_error($('#graphic_1', element));
                show_graphic_error($('#graphic_2', element));
                log_ajax_error(jqXHR, exception);
                enable($('#calculate_graphics', element));
            },
            contentType: 'application/json; charset=utf-8'
        });
    }


    $('#save_answer', element).click(function (event) {
        disable($('#save_answer button'), element);
        $.ajax({
            type: "POST",
            url: save_answer,
            data: JSON.stringify(generateAnswer()),
            success: function (result) {
                actions_bottom_notification("save", $('.dsp-notification', element));
                enable($('#save_answer button'), element);
            },
            error: function (jqXHR){
                error_bottom_notification(jqXHR, "При сохранении ответа произошла ошибка", $('.dsp-notification', element));
                enable($('#save_answer button'), element);
            },
            contentType: 'application/json; charset=utf-8'
        });
    });

    $('#check_answer', element).click(function (event) {
        disable($('#check_answer'), element);
        $.ajax({
            type: "POST",
            url: student_submit,
            data: JSON.stringify(generateAnswer()),
            success: function (result) {
                $(element).find('me-span.points').html(result.score);
                $(element).find('.weight').html('Набрано баллов: <me-span class="points"></span>');
                $('.points', element).text(result.score + ' из ' + data.maximum_score);
                if (highlight_correct) highlight_correctness(result.correctness);
                is_success_bottom_notification(result.is_success, result.score, result.maximum_score, $('.dsp-notification', element));
                $('.attempts', element).text(result.attempts);
                if (result.max_attempts && result.max_attempts <= result.attempts) {
                    data.answer_opportunity = false;
                }
                else{
                    enable($('#check_answer'), element);
                }
            },
            error: function (jqXHR){
                check_error_bottom_notification(jqXHR, $('.dsp-notification', element));
                enable($('#check_answer'), element);
            },
            contentType: 'application/json; charset=utf-8'
        });
    });

    $('#reset_task', element).click(function (event) {
        disable($('#reset_task button'), element);
        $.ajax({
            type: "GET",
            url: reset_task,
            success: function (result) {
                // actions_bottom_notification("save", $('.dsp-notification', element));
                enable($('#reset_task button'), element);
                window.location.reload(true);
            },
            error: function (jqXHR){
                error_bottom_notification(jqXHR, "При сбросе задания произошла ошибка", $('.dsp-notification', element));
                enable($('#reset_task button'), element);
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
            //"student_window": "rectangular",
            "student_ubl": "",
            "student_p": ""
        };
        student_data.student_signal = parseTextSignal($("#input_student_signal", element)).signal;
        student_data.student_filter = parseTextSignal($("#input_student_filter", element)).signal;
        student_data.student_a = $("#input_student_a", element).val();
        student_data.student_ubl = $("#input_student_ubl", element).val();
        student_data.student_p = $("#input_student_p", element).val();
        return student_data;
    }

    function build_lab_state(data) {
        $("textarea#input_student_signal", element).val(data.answer.student_signal);
        $("textarea#input_student_filter", element).val(data.answer.student_filter);
        $("#input_student_a", element).val(data.answer.student_a);
        $("#input_student_ubl", element).val(data.answer.student_ubl);
        $("#input_student_p", element).val(data.answer.student_p);
        build_graphics();
    }

    function buttons_disable() {
        var student_data = generateAnswer();
        if (student_data.student_filter.length > 0 && student_data.student_signal.length > 0 && parseFloat(student_data.student_a)) {
            $("#calculate_graphics", element).removeAttr("disabled");
            if (parseFloat(student_data.student_p) && parseFloat(student_data.student_ubl)) {
                $("#check_answer", element).removeAttr("disabled");
            }
            else {
                $("#check_answer", element).attr('disabled', 'disabled');
            }
        }
        else {
            $("#calculate_graphics", element).attr('disabled', 'disabled');
            $("#check_answer", element).attr('disabled', 'disabled');
        }
    }

    $(function ($) {
        console.log(data);
        if (data.student_state.answer) {
            build_lab_state(data["student_state"]);
            $("textarea.array-input", element).each(function (i) {
                process_array_input(this);
            });
            if (data.student_state.correctness && highlight_correct) {
                highlight_correctness(data["student_state"]["correctness"]);
            }
        }
        buttons_disable();
        $(element).on('input', ".answer-input", function () {
            buttons_disable();
            clean_bottom_notification($('.dsp-notification', element));
            if (highlight_correct) {
                $(this).removeClass("dsp-incorrect-input");
                $(this).removeClass("dsp-correct-input");
            }
        });
        $("textarea.array-input", element).each(function (i) {
            $(this).change(function () {
                process_array_input(this);
            });
        });


    });

}