function DSPXBlock(runtime, element, data) {

    var student_submit = runtime.handlerUrl(element, 'student_submit');
    var get_graphics = runtime.handlerUrl(element, 'get_graphics');
    var highlight_correct = true;

    function build_graphics() {
        $("#graphic_1", element).html(""); //<div style='background: #f3f3f2;width: 100%;height:330px;'></div>
        $("#graphic_2", element).html("");
        $.ajax({
            type: "POST",
            url: get_graphics,
            data: JSON.stringify(generateAnswer()),
            success: function (result) {
                $("#graphic_1", element).html(result["graphics"][0]["html"]);
                $("#graphic_2", element).html(result["graphics"][1]["html"]);
            },
            error: function (jqXHR, exception) {
                show_graphic_error($('#graphic_1'));
                show_graphic_error($('#graphic_2'));
                log_ajax_error(jqXHR, exception);
            },
            contentType: 'application/json; charset=utf-8'
        });
    }

    $('#check_answer', element).click(function (event) {
        $.ajax({
            type: "POST",
            url: student_submit,
            data: JSON.stringify(generateAnswer()),
            success: function (result) {
                $(element).find('me-span.points').html(result.score);
                $(element).find('.weight').html('Набрано баллов: <me-span class="points"></span>');
                $('.points', element).text(result.score + ' из ' + data.maximum_score);
                if (highlight_correct) highlight_correctness(result.correctness);
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
        student_data.student_signal = parseTextSignal($("#input_student_signal", element).val()).signal;
        student_data.student_filter = parseTextSignal($("#input_student_filter", element).val()).signal;
        student_data.student_a = $("#input_student_a", element).val();
        //student_data.student_window = $('input[name=input_student_window]:checked', element).val();
        student_data.student_ubl = $("#input_student_ubl", element).val();
        student_data.student_p = $("#input_student_p", element).val();
        return student_data;
    }

    function build_lab_state(data) {
        $("textarea#input_student_signal", element).val(data.answer.student_signal);
        $("textarea#input_student_filter", element).val(data.answer.student_filter);
        $("#input_student_a", element).val(data.answer.student_a);
        //$('input:radio[name="input_student_window"]', element).filter('[value="' + data.answer.student_window + '"]').attr('checked', true);
        $("#input_student_ubl", element).val(data.answer.student_ubl);
        $("#input_student_p", element).val(data.answer.student_p);
        build_graphics();
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
        if (highlight_correct) {
            $(document).on('input', ".answer-input", function () {
                $(this).removeClass("dsp-incorrect-input");
                $(this).removeClass("dsp-correct-input");
            });
        }

        $("textarea.array-input", element).each(function (i) {
            $(this).change(function () {
                console.log(this);
                process_array_input(this);
            });
        });


    });

}