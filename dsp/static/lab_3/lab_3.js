function DSPXBlock(runtime, element, data) {

    var student_submit = runtime.handlerUrl(element, 'student_submit');
    var get_graphic_1 = runtime.handlerUrl(element, 'lab_3_get_graphic_1');
    var get_graphic_2 = runtime.handlerUrl(element, 'lab_3_get_graphic_2');
    var highlight_correct = true;

    function build_graphic_1() {
        show_graphic_load($('#graphic_1', element));
        $.ajax({
            type: "POST",
            url: get_graphic_1,
            data: JSON.stringify(generateAnswer()),
            success: function (result) {
                $("#graphic_1", element).html(result["graphic"]["html"]);
            },
            error: function (jqXHR, exception) {
                show_graphic_error($('#graphic_1', element));
                log_ajax_error(jqXHR, exception);
            },
            contentType: 'application/json; charset=utf-8'
        });
    }

    function build_graphic_2() {
        show_graphic_load($('#graphic_2', element));
        $.ajax({
            type: "POST",
            url: get_graphic_2 + "?lol=kek",
            data: JSON.stringify(generateAnswer()),
            success: function (result) {
                $("#graphic_2", element).html(result["graphic"]["html"]);
                 $("#current_Ku_i", element).html(result["state"]["state"]["Ku_i"]);
                 $("#current_Ku_j", element).html(result["state"]["state"]["Ku_j"]);
            },
            error: function (jqXHR, exception) {
                show_graphic_error($('#graphic_2', element));
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
        build_graphic_2();
    });

    function generateAnswer() {
        var student_data = {
            "student_signal": [],
            "student_filter": [],
            "student_B": "",
            // "student_F": "",
            // "student_Dp": "",
            // "student_filterstable": "stable",
        };
        student_data.student_signal = parseTextSignal($("#input_student_signal", element)).signal;
        student_data.student_filter = parseTextSignal($("#input_student_filter", element)).signal;
        student_data.student_B = $("#input_student_B", element).val();
        // student_data.student_F = $("#input_student_F", element).val();
        // student_data.student_Dp = $("#input_student_Dp", element).val();
        // student_data.student_filterstable = $('input[name=input_student_filterstable]:checked', element).val();

        console.log(student_data);
        return student_data;
    }

    function build_lab_state(data) {
        $("textarea#input_student_signal", element).val(data.answer.student_signal);
        $("textarea#input_student_filter", element).val(data.answer.student_filter);
        $("#input_student_B", element).val(data.answer.student_B);
        // $("#input_student_F", element).val(data.answer.student_F);
        // $("#input_student_Dp", element).val(data.answer.student_Dp);
        // $('input:radio[name="input_student_filterstable"]', element).filter('[value="' + data.answer.student_filterstable + '"]').attr('checked', true);
        build_graphic_1();
        build_graphic_2();
    }

    // function buttons_disable() {
    //     var student_data = generateAnswer();
    //     if (student_data.student_filter.length > 0 && student_data.student_signal.length > 0 && parseFloat(student_data.student_b)) {
    //         $("#calculate_graphics", element).removeAttr("disabled");
    //         if (parseFloat(student_data.student_F) && parseFloat(student_data.student_Dp)) {
    //             $("#check_answer", element).removeAttr("disabled");
    //         }
    //         else {
    //             $("#check_answer", element).attr('disabled', 'disabled');
    //         }
    //     }
    //     else {
    //         $("#calculate_graphics", element).attr('disabled', 'disabled');
    //         $("#check_answer", element).attr('disabled', 'disabled');
    //     }
    // }

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
        // buttons_disable();

        // $(element).on('input', ".answer-input", function () {
        //     buttons_disable();
        //     if (highlight_correct) {
        //         $(this).removeClass("dsp-incorrect-input");
        //         $(this).removeClass("dsp-correct-input");
        //     }
        // });


        $("textarea.array-input", element).each(function (i) {
            $(this).change(function () {
                process_array_input(this);
            });
        });


    });

}