function DSPXBlock(runtime, element, data) {

    var student_submit = runtime.handlerUrl(element, 'student_submit');
    var save_answer = runtime.handlerUrl(element, 'save_answer');
    var get_graphics = runtime.handlerUrl(element, 'lab_4_get_graphics');
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
            error: function (jqXHR) {
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
                $('.points', element).text(result.score + ' из ' + data.weight);
                if (highlight_correct) highlight_correctness(result.correctness);
                is_success_bottom_notification(result.is_success, result.score, result.weight, $('.dsp-notification', element));
                $('.attempts', element).text(result.attempts);
                if (result.max_attempts && result.max_attempts <= result.attempts) {
                    data.answer_opportunity = false;
                } else {
                    enable($('#check_answer'), element);
                }
            },
            error: function (jqXHR) {
                check_error_bottom_notification(jqXHR, $('.dsp-notification', element));
                enable($('#check_answer'), element);
            },
            contentType: 'application/json; charset=utf-8'
        });
    });

    $('#reset_task', element).click(function (event) {
        disable($('#reset_task button'), element);
        var confirm_reset = confirm("Вы уверены, что хотите сбросить задание? При сбросе задания набранные баллы и ответ не сохраняются.");
        if (confirm_reset) {
            $.ajax({
                type: "GET",
                url: reset_task,
                success: function (result) {
                    // actions_bottom_notification("save", $('.dsp-notification', element));
                    enable($('#reset_task button'), element);
                    window.location.reload(true);
                },
                error: function (jqXHR) {
                    error_bottom_notification(jqXHR, "При сбросе задания произошла ошибка", $('.dsp-notification', element));
                    enable($('#reset_task button'), element);
                },
                contentType: 'application/json; charset=utf-8'
            });
        }
    });

    $('#calculate_graphics', element).click(function (event) {
        build_graphics();
    });

    function generateAnswer() {
        var student_data = {
            "student_signal": [],
            "student_filter": [],
            "student_b": "",
            "student_F": "",
            "student_Dp": "",
            "student_filterstable": "stable",
        };
        student_data.student_signal = parseTextSignal($("#input_student_signal", element)).signal;
        student_data.student_filter = parseTextSignal($("#input_student_filter", element)).signal;
        student_data.student_b = $("#input_student_b", element).val();
        student_data.student_F = $("#input_student_F", element).val();
        student_data.student_Dp = $("#input_student_Dp", element).val();
        student_data.student_filterstable = $('input[name=input_student_filterstable]:checked', element).val();

        console.log(student_data);
        return student_data;
    }

    function build_lab_state(data) {
        $("textarea#input_student_signal", element).val(data.answer.student_signal);
        $("textarea#input_student_filter", element).val(data.answer.student_filter);
        $("#input_student_b", element).val(data.answer.student_b);
        $("#input_student_F", element).val(data.answer.student_F);
        $("#input_student_Dp", element).val(data.answer.student_Dp);
        $('input:radio[name="input_student_filterstable"]', element).filter('[value="' + data.answer.student_filterstable + '"]').attr('checked', true);
        build_graphics();
    }

    function buttons_disable() {
        var student_data = generateAnswer();
        if (student_data.student_filter.length > 0 && student_data.student_signal.length > 0 && parseFloat(student_data.student_b)) {
            enable($("#calculate_graphics", element));
            if (parseFloat(student_data.student_F) && parseFloat(student_data.student_Dp)) {
                if (data.answer_opportunity) {
                    enable($("#check_answer", element));
                }
            } else {
                disable($("#check_answer", element));
            }
        } else {
            disable($("#calculate_graphics", element));
            disable($("#check_answer", element));
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

        $("#input_student_filterstable input[type=radio]", element).change(function () {
            if (highlight_correct) {
                $(this).closest("#input_student_filterstable").removeClass("dsp-incorrect-input");
                $(this).closest("#input_student_filterstable").removeClass("dsp-correct-input");
            }
        });

        $("textarea.array-input", element).each(function (i) {
            this.addEventListener('input', function (e) {
                process_array_input(this);
            }, false);
        });


    });

}