function DSPXBlock(runtime, element, data) {

    var student_submit = runtime.handlerUrl(element, 'student_submit');
    var save_answer = runtime.handlerUrl(element, 'save_answer');
    var get_graphic_1 = runtime.handlerUrl(element, 'lab_3_get_graphic_1');
    var get_graphic_2 = runtime.handlerUrl(element, 'lab_3_get_graphic_2');
    var get_graphic_3 = runtime.handlerUrl(element, 'lab_3_get_graphic_3');
    var lab_3_reset_task_url = runtime.handlerUrl(element, 'lab_3_reset_task');
    var reset_task = runtime.handlerUrl(element, 'reset_task');
    var highlight_correct = true;
    
    function lab_3_reset_task() {
        var confirm_reset = confirm("Вы уверены, что хотите сбросить рассчитанные данные?");
        if (confirm_reset) {
            disable($('#lab_3_reset_task', element));
            disable($('#calculate_graphic_2_there_is_signal', element));
            disable($('#calculate_graphic_2_there_is_no_signal', element));
            disable($('#calculate_graphic_2', element));
            $.ajax({
                type: "GET",
                url: lab_3_reset_task_url,
                success: function (result) {
                    build_graphic_2(true);
                    enable($('#lab_3_reset_task', element));
                    enable($('#calculate_graphic_2_there_is_signal', element));
                    enable($('#calculate_graphic_2_there_is_no_signal', element));
                    enable($('#calculate_graphic_2', element));
                },
                error: function (jqXHR, exception) {
                    alert("При сбросе ответа возникла ошибка.");
                    enable($('#lab_3_reset_task', element));
                    enable($('#calculate_graphic_2_there_is_signal', element));
                    enable($('#calculate_graphic_2_there_is_no_signal', element));
                    enable($('#calculate_graphic_2', element));
                },
                contentType: 'application/json; charset=utf-8'
            });
        }
    }

    function build_graphic_1() {
        show_graphic_load($('#graphic_1', element));
        disable($('#calculate_graphic_1', element));
        $.ajax({
            type: "POST",
            url: get_graphic_1,
            data: JSON.stringify(generateAnswer()),
            success: function (result) {
                $("#graphic_1", element).html(result["graphic"]["html"]);
                enable($('#calculate_graphic_1', element));
            },
            error: function (jqXHR, exception) {
                show_graphic_error($('#graphic_1', element));
                log_ajax_error(jqXHR, exception);
                enable($('#calculate_graphic_1', element));
            },
            contentType: 'application/json; charset=utf-8'
        });
    }

    function build_graphic_2(reload, there_is_signal="") {
        show_graphic_load($('#graphic_2', element));
        disable($('#calculate_graphic_2_there_is_signal', element));
        disable($('#calculate_graphic_2_there_is_no_signal', element));
        disable($('#calculate_graphic_2', element));
        params = [];
        params_str = "";
        if (reload) {
            params.push("reload=true");
        }
        if (there_is_signal !== ""){
            params.push("is_signal="+there_is_signal)
        }
        if (params.length > 0){
            params_str = "?" + params.join("&")
        }
        $.ajax({
            type: "POST",
            url: get_graphic_2 + params_str,
            data: JSON.stringify(generateAnswer()),
            success: function (result) {
                 $(".graphic-2-not-first-build", element).css("display", "block");

                 $("#graphic_2", element).html(result["graphic"]["html"]);
                 $("#current_Ku_i", element).html(result["student_state"]["state"]["Ku_i"]);
                 $("#current_Ku_j", element).html(result["student_state"]["state"]["Ku_j"]);

                 $("#there-is-no-signal-count", element).html(result["student_state"]["state"]["there_is_no_signal_count"]);
                 $("#there-is-signal-count", element).html(result["student_state"]["state"]["there_is_signal_count"]);

                 result["student_state"]["state"]["there_is_signal_states"].forEach(function(state_value, idx) {
                    if (state_value.there_is_signal_count !== undefined ) {
                        $("#input_student_s .label-signal-count", element)[idx].innerHTML = state_value.there_is_signal_count;
                        $("#input_student_s .label-no-signal-count", element)[idx].innerHTML = state_value.there_is_no_signal_count;
                    }
                    else {
                        $("#input_student_s .label-signal-count", element)[idx].innerHTML = 0;
                        $("#input_student_s .label-no-signal-count", element)[idx].innerHTML = 0;
                    }

                });

                 data.student_state.state.Ku_j = result["student_state"]["state"]["Ku_j"];
                 data.student_state.state.Ku_i = result["student_state"]["state"]["Ku_i"];

                 if (result["student_state"]["state"]["Ku_done"]){
                     $("#graphic-2-controls", element).css("display", "none");
                 }
                 else{
                     $("#graphic-2-controls", element).css("display", "block");
                 }
                enable($('#calculate_graphic_2_there_is_signal', element));
                enable($('#calculate_graphic_2_there_is_no_signal', element));
                enable($('#calculate_graphic_2', element));
                buttons_disable();
            },
            error: function (jqXHR, exception) {
                show_graphic_error($('#graphic_2', element));
                log_ajax_error(jqXHR, exception);
                enable($('#calculate_graphic_2_there_is_signal', element));
                enable($('#calculate_graphic_2_there_is_no_signal', element));
                enable($('#calculate_graphic_2', element));
            },
            contentType: 'application/json; charset=utf-8'
        });
    }

    function build_graphic_3() {
        show_graphic_load($('#graphic_3', element));
        $.ajax({
            type: "POST",
            url: get_graphic_3,
            data: JSON.stringify(generateAnswer()),
            success: function (result) {
                $("#graphic_3", element).html(result["graphic"]["html"]);
            },
            error: function (jqXHR, exception) {
                show_graphic_error($('#graphic_3', element));
                log_ajax_error(jqXHR, exception);
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

    $('#calculate_graphic_1', element).click(function (event) {
        build_graphic_1();
    });
    $('#calculate_graphic_2', element).click(function (event) {
        build_graphic_2(true);
    });
    $('#calculate_graphic_2_there_is_signal', element).click(function (event) {
        build_graphic_2(false, "there_is_signal");
    });
    $('#calculate_graphic_2_there_is_no_signal', element).click(function (event) {
        build_graphic_2(false, "there_is_no_signal");
    });
    $('#lab_3_reset_task', element).click(function (event) {
        lab_3_reset_task();
    });

    function generateAnswer() {
        var student_data = {
            "student_signal": [],
            "student_filter": [],
            "student_B": "",
            "student_s": [],
        };
        student_data.student_signal = parseTextSignal($("#input_student_signal", element)).signal;
        student_data.student_filter = parseTextSignal($("#input_student_filter", element)).signal;
        student_data.student_B = $("#input_student_B", element).val();
        $("input.s-input", element).each(function(){
            student_data.student_s.push($(this).val());
        });
        return student_data;
    }

    function build_lab_state(data) {
        $("textarea#input_student_signal", element).val(data.answer.student_signal);
        $("textarea#input_student_filter", element).val(data.answer.student_filter);
        $("#input_student_B", element).val(data.answer.student_B);
        data.answer.student_s.forEach(function(s_value, idx) {
            $("input.s-input", element)[idx].value = s_value;
        });
        build_graphic_1();
        build_graphic_2(true);
        build_graphic_3();
    }

    function buttons_disable() {
        var student_data = generateAnswer();
        if (student_data.student_filter.length > 0 && student_data.student_signal.length > 0) {
            enable($("#calculate_graphic_1", element));
            enable($("#calculate_graphic_2", element));
            enable($("#reset_task", element));
            if (parseFloat(student_data.student_B) && student_data.student_s.every(elem => elem.toString().replace(/\s/g, "") != "")) {
                if(data.answer_opportunity) {
                    // if(data.student)
                    console.log(data.student_state.state.Ku_i, data.student_state.state.Ku_j);
                    if (data.student_state.state.Ku_i != 1 || data.student_state.state.Ku_j != 1){
                        enable($("#check_answer", element));
                    }
                    else {
                        disable($("#check_answer", element));
                    }
                }
            }
            else {
                disable( $("#check_answer", element));
            }
        }
        else {
            disable($("#calculate_graphic_1", element));
            disable($("#calculate_graphic_2", element));
            disable($("#reset_task", element));
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
            // if (data.student_state.correctness && highlight_correct) {
            //     highlight_correctness(data["student_state"]["correctness"]);
            // }
        }
        buttons_disable();

        $(element).on('input', ".answer-input", function () {
            buttons_disable();
            clean_bottom_notification($('.dsp-notification', element));
            // if (highlight_correct) {
            //     $(this).removeClass("dsp-incorrect-input");
            //     $(this).removeClass("dsp-correct-input");
            // }
        });


        $("textarea.array-input", element).each(function (i) {
            $(this).change(function () {
                process_array_input(this);
            });
        });

        $("input.s-input", element).each(function (i) {
            $(this).change(function () {
                build_graphic_3();
            });
        })


    });

}