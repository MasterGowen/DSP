function DSPXBlock(runtime, element, data) {

    var student_submit = runtime.handlerUrl(element, 'student_submit');
    var get_graphic_1 = runtime.handlerUrl(element, 'lab_3_get_graphic_1');
    var get_graphic_2 = runtime.handlerUrl(element, 'lab_3_get_graphic_2');
    var get_graphic_3 = runtime.handlerUrl(element, 'lab_3_get_graphic_3');
    var highlight_correct = true;

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

                });

                 if (result["student_state"]["state"]["Ku_done"]){
                     $("#graphic-2-controls", element).css("display", "none");
                 }
                    enable($('#calculate_graphic_2_there_is_signal', element));
                    enable($('#calculate_graphic_2_there_is_no_signal', element));
                    enable($('#calculate_graphic_2', element));
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

    // $('#check_answer', element).click(function (event) {
    //     console.info("Начали проверку");
    //     $.ajax({
    //         type: "POST",
    //         url: student_submit,
    //         data: JSON.stringify(generateAnswer()),
    //         success: function (result) {
    //             $(element).find('me-span.points').html(result.score);
    //             $(element).find('.weight').html('Набрано баллов: <me-span class="points"></span>');
    //             $('.points', element).text(result.score + ' из ' + data.maximum_score);
    //             if (highlight_correct) highlight_correctness(result.correctness);
    //             console.info("Закончили проверку");
    //         },
    //         contentType: 'application/json; charset=utf-8'
    //     });
    // });

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
            if (parseFloat(student_data.student_B) && student_data.student_s.every(elem => elem.toString().replace(/\s/g, "") != "")) {
                enable($("#check_answer", element));
            }
            else {
                disable( $("#check_answer", element));
            }
        }
        else {
            disable($("#calculate_graphic_1", element));
            disable($("#check_answer", element));
        }
    }

    $(function ($) {
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