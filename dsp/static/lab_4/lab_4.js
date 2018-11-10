function DSPXBlock(runtime, element, data) {

    var student_submit = runtime.handlerUrl(element, 'student_submit');
    var get_graphics = runtime.handlerUrl(element, 'lab_4_get_graphics');
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
                enable($('#check_answer'), element);
            },
            error: function (jqXHR){
                check_error_bottom_notification(jqXHR, $('.dsp-notification', element));
                enable($('#check_answer'), element);
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
            $("#calculate_graphics", element).removeAttr("disabled");
            if (parseFloat(student_data.student_F) && parseFloat(student_data.student_Dp)) {
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
        // console.log(data);
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
            $(this).change(function () {
                process_array_input(this);
            });
        });


    });

}