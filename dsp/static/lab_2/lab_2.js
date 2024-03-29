function DSPXBlock(runtime, element, data) {
    var student_submit = runtime.handlerUrl(element, 'student_submit');
    var save_answer = runtime.handlerUrl(element, 'save_answer');
    var reset_task = runtime.handlerUrl(element, 'reset_task');
    var get_graphics_1 = runtime.handlerUrl(element, 'lab_2_get_graphics_1');
    var get_graphics_2 = runtime.handlerUrl(element, 'lab_2_get_graphics_2');
    var get_graphics_3 = runtime.handlerUrl(element, 'lab_2_get_graphics_3');

    var highlight_correct = true;

    function build_graphics_1() {
        show_graphic_load($('#graphic_1_1', element));
        show_graphic_load($('#graphic_1_2', element));
        $.ajax({
            type: "GET",
            url: get_graphics_1,
            success: function (result) {
                $("#graphic_1_1", element).html(result["graphics"][0]["html"]);
                $("#graphic_1_2", element).html(result["graphics"][1]["html"]);
            },
            error: function (jqXHR, exception) {
                show_graphic_error($('#graphic_1_1', element));
                show_graphic_error($('#graphic_1_2', element));
                log_ajax_error(jqXHR, exception);
            },
            contentType: 'application/json; charset=utf-8'
        });
    }

    function build_graphics_2() {
        show_graphic_load($('#graphic_2_1', element));
        show_graphic_load($('#graphic_2_2', element));
        $.ajax({
            type: "GET",
            url: get_graphics_2,
            success: function (result) {
                $("#graphic_2_1", element).html(result["graphics"][0]["html"]);
                $("#graphic_2_2", element).html(result["graphics"][1]["html"]);
            },
            error: function (jqXHR, exception) {
                show_graphic_error($('#graphic_2_1', element));
                show_graphic_error($('#graphic_2_2', element));
                log_ajax_error(jqXHR, exception);
            },
            contentType: 'application/json; charset=utf-8'
        });
    }

    function build_graphics_3() {
        show_graphic_load($('#graphic_3_1', element));
        show_graphic_load($('#graphic_3_2', element));
        $.ajax({
            type: "GET",
            url: get_graphics_3,
            success: function (result) {
                $("#graphic_3_1", element).html(result["graphics"][0]["html"]);
                $("#graphic_3_2", element).html(result["graphics"][1]["html"]);
            },
            error: function (jqXHR, exception) {
                show_graphic_error($('#graphic_3_1', element));
                show_graphic_error($('#graphic_3_2', element));
                log_ajax_error(jqXHR, exception);
            },
            contentType: 'application/json; charset=utf-8'
        });
    }


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

    function buttons_disable() {
        var student_data = generateAnswer();

        if (parseFloat(student_data.student_K1) && parseFloat(student_data.student_ns0) && parseFloat(student_data.student_ns1)) {
            if (parseFloat(student_data.student_K2)) {
                if (student_data.student_f.length > 0) {
                    if (data.answer_opportunity) {
                        enable($("#check_answer", element));
                    }
                } else {
                    disable($("#check_answer", element));
                }
            } else {
                disable($("#check_answer", element));
            }
        } else {
            disable($("#check_answer", element));
        }
    }

    function generateAnswer() {
        var student_data = {};
        student_data.student_K1 = $("#input_student_K1", element).val();
        student_data.student_ns0 = $("#input_student_ns0", element).val();
        student_data.student_ns1 = $("#input_student_ns1", element).val();
        student_data.student_K2 = $("#input_student_K2", element).val();

        student_data.student_f = parseTextSignal($("#input_student_f", element)).signal;

        return student_data;
    }

    function build_lab_state(data) {
        $("#input_student_K1", element).val(data.answer.student_K1);
        $("#input_student_ns0", element).val(data.answer.student_ns0);
        $("#input_student_ns1", element).val(data.answer.student_ns1);
        $("#input_student_K2", element).val(data.answer.student_K2);
        $("textarea#input_student_f", element).val(data.answer.student_f);
    }

    $(function ($) {
        console.log(data);
        build_graphics_1();
        build_graphics_2();
        build_graphics_3();
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
            this.addEventListener('input', function (e) {
                process_array_input(this);
            }, false);
        });

    });


}
