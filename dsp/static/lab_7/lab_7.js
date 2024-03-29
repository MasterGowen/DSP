function DSPXBlock(runtime, element, data) {
    var student_submit = runtime.handlerUrl(element, 'student_submit');
    var save_answer = runtime.handlerUrl(element, 'save_answer');
    var reset_task = runtime.handlerUrl(element, 'reset_task');
    var get_graphic_1 = runtime.handlerUrl(element, 'lab_7_get_graphic_1');
    var get_graphic_2 = runtime.handlerUrl(element, 'lab_7_get_graphic_2');
    var get_graphic_3 = runtime.handlerUrl(element, 'lab_7_get_graphic_3');
    var get_graphic_4 = runtime.handlerUrl(element, 'lab_7_get_graphic_4');

    var highlight_correct = true;

    function build_graphic_1() {
        show_graphic_load($('#graphic_1_1', element));
        show_graphic_load($('#graphic_1_2', element));
        $.ajax({
            type: "GET",
            url: get_graphic_1,
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

    function build_graphic_2() {
        show_graphic_load($('#graphic_2', element));
        disable($('#calculate_graphic_2', element));
        $.ajax({
            type: "POST",
            url: get_graphic_2,
            data: JSON.stringify(generateAnswer()),
            success: function (result) {
                $("#graphic_2", element).html(result["graphics"]["html"]);
                enable($('#calculate_graphic_2', element));
            },
            error: function (jqXHR, exception) {
                show_graphic_error($('#graphic_2', element));
                log_ajax_error(jqXHR, exception);
                enable($('#calculate_graphic_2', element));
            },
            contentType: 'application/json; charset=utf-8'
        });
    }

    $('#calculate_graphic_2', element).click(function (event) {
        build_graphic_2();
    });

    function build_graphic_3() {
        show_graphic_load($('#graphic_3_1', element));
        show_graphic_load($('#graphic_3_2', element));
        $.ajax({
            type: "GET",
            url: get_graphic_3,
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

    function build_graphic_4() {
        show_graphic_load($('#graphic_4_1', element));
        // show_graphic_load($('#graphic_4_2', element));
        disable($('#calculate_graphic_2', element));
        $.ajax({
            type: "POST",
            url: get_graphic_4,
            data: JSON.stringify(generateAnswer()),
            success: function (result) {
                $("#graphic_4_1", element).html(result["graphics"][0]["html"]);
                // $("#graphic_4_2", element).html(result["graphics"][1]["html"]);
                enable($('#calculate_graphic_2', element));
            },
            error: function (jqXHR, exception) {
                show_graphic_error($('#graphic_4_1', element));
                // show_graphic_error($('#graphic_4_2', element));
                enable($('#calculate_graphic_2', element));
                log_ajax_error(jqXHR, exception);
            },
            contentType: 'application/json; charset=utf-8'
        });
    }

    $('#calculate_graphic_4', element).click(function (event) {
        build_graphic_4();
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
        if (student_data.student_Sm.length > 0) {
            enable($("#calculate_graphic_2", element));
        } else {
            disable($("#calculate_graphic_2", element));
        }
        if (student_data.student_a.length > 0 && student_data.student_b.length > 0) {
            enable($("#calculate_graphic_4", element));
        } else {
            disable($("#calculate_graphic_4", element));
        }

        if (parseFloat(student_data.student_f0) && parseFloat(student_data.student_fm) && parseFloat(student_data.student_m)) {
            if (student_data.student_a.length > 0 && student_data.student_b.length > 0 && student_data.student_Sm.length > 0) {
                if (student_data.student_soob.length > 0) {
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
        student_data.student_Sm = parseTextSignal($("#input_student_Sm", element)).signal;
        student_data.student_a = parseTextSignal($("#input_student_a", element)).signal;
        student_data.student_b = parseTextSignal($("#input_student_b", element)).signal;

        student_data.student_f0 = $("#input_student_f0", element).val();
        student_data.student_fm = $("#input_student_fm", element).val();
        student_data.student_m = $("#input_student_m", element).val();
        student_data.student_soob = $("#input_student_soob", element).val().split(' ').join('');

        return student_data;
    }

    function build_lab_state(data) {
        $("textarea#input_student_Sm", element).val(data.answer.student_Sm);
        $("textarea#input_student_a", element).val(data.answer.student_a);
        $("textarea#input_student_b", element).val(data.answer.student_b);

        $("#input_student_f0", element).val(data.answer.student_f0);
        $("#input_student_fm", element).val(data.answer.student_fm);
        $("#input_student_m", element).val(data.answer.student_m);
        $("#input_student_soob", element).val(data.answer.student_soob);

        if (data.answer.student_Sm.length > 0) {
            build_graphic_2();
        }
        if (data.answer.student_a.length > 0 && data.answer.student_b.length > 0) {
            build_graphic_4();
        }
    }


    $(function ($) {
        console.log(data);
        build_graphic_1();
        build_graphic_3();
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
