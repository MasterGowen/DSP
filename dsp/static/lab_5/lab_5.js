function DSPXBlock(runtime, element, data) {

    var student_submit = runtime.handlerUrl(element, 'student_submit');
    var save_answer = runtime.handlerUrl(element, 'save_answer');
    var get_graphic_1 = runtime.handlerUrl(element, 'lab_5_get_graphic_1');
    var get_graphic_2 = runtime.handlerUrl(element, 'lab_5_get_graphic_2');

    var highlight_correct = true;

    function build_graphic_1() {
        disable($('#calculate_graphic_1', element));
        show_graphic_load($('#graphic_1', element));
        show_graphic_load($('#graphic_2', element));
        $.ajax({
            type: "POST",
            url: get_graphic_1,
            data: JSON.stringify(generateAnswer()),
            success: function (result) {
                $("#graphic_1", element).html(result["graphics"][0]["html"]);
                $("#graphic_2", element).html(result["graphics"][1]["html"]);
                enable($('#calculate_graphic_1', element));
            },
            error: function (jqXHR, exception) {
                show_graphic_error($('#graphic_1', element));
                show_graphic_error($('#graphic_2', element));
                log_ajax_error(jqXHR, exception);
                enable($('#calculate_graphic_1', element));
            },
            contentType: 'application/json; charset=utf-8'
        });
    }
    function build_graphic_2() {
        disable($('#calculate_graphic_2', element));
        show_graphic_load($('#graphic_3', element));
        show_graphic_load($('#graphic_4', element));
        show_graphic_load($('#graphic_5', element));
        show_graphic_load($('#graphic_6', element));
        $.ajax({
            type: "POST",
            url: get_graphic_2,
            data: JSON.stringify(generateAnswer()),
            success: function (result) {
                $("#graphic_3", element).html(result["graphics"][0]["html"]);
                $("#graphic_4", element).html(result["graphics"][1]["html"]);
                $("#graphic_5", element).html(result["graphics"][2]["html"]);
                $("#graphic_6", element).html(result["graphics"][3]["html"]);
                enable($('#calculate_graphic_2', element));
            },
            error: function (jqXHR, exception) {
                show_graphic_error($('#graphic_3', element));
                show_graphic_error($('#graphic_4', element));
                show_graphic_error($('#graphic_5', element));
                show_graphic_error($('#graphic_6', element));
                log_ajax_error(jqXHR, exception);
                enable($('#calculate_graphic_2', element));
            },
            contentType: 'application/json; charset=utf-8'
        });
    }

    $('#save_answer', element).click(function (event) {
        disable($('#save_answer'), element);
        $.ajax({
            type: "POST",
            url: save_answer,
            data: JSON.stringify(generateAnswer()),
            success: function (result) {
                actions_bottom_notification("save", $('.dsp-notification', element));
                enable($('#save_answer'), element);
            },
            error: function (jqXHR){
                console.log("Ошибка при сохранении ответа");
                alert("Ошибка при сохранении ответа");
                enable($('#save_answer'), element);
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
                enable($('#check_answer'), element);
            },
            error: function (jqXHR){
                check_error_bottom_notification(jqXHR, $('.dsp-notification', element));
                enable($('#check_answer'), element);
            },
            contentType: 'application/json; charset=utf-8'
        });
    });

    $('#calculate_graphic_1', element).click(function (event) {
        build_graphic_1();
    });

    $('#calculate_graphic_2', element).click(function (event) {
        build_graphic_2();
    });


    function generateAnswer() {
        var student_data = {};
        student_data.student_s = parseTextSignal($("#input_student_s", element)).signal;
        student_data.student_s1 = parseTextSignal($("#input_student_s1", element)).signal;
        student_data.student_fn = $("#input_student_fn", element).val();

        student_data.student_sl = parseTextSignal($("#input_student_sl", element)).signal;
        student_data.student_slc = parseTextSignal($("#input_student_slc", element)).signal;
        student_data.student_Np = $("#input_student_Np", element).val();

        student_data.student_K1 = $("#input_student_K1", element).val();
        student_data.student_K2 = $("#input_student_K2", element).val();
        student_data.student_K3 = $("#input_student_K3", element).val();
        student_data.student_K4 = $("#input_student_K4", element).val();

        return student_data;
    }

    function build_lab_state(data) {
        $("textarea#input_student_s", element).val(data.answer.student_s);
        $("textarea#input_student_s1", element).val(data.answer.student_s1);
        $("#input_student_fn", element).val(data.answer.student_fn);

        $("textarea#input_student_sl", element).val(data.answer.student_sl);
        $("textarea#input_student_slc", element).val(data.answer.student_slc);
        $("#input_student_Np", element).val(data.answer.student_Np);

        $("#input_student_K1", element).val(data.answer.student_K1);
        $("#input_student_K2", element).val(data.answer.student_K2);
        $("#input_student_K3", element).val(data.answer.student_K3);
        $("#input_student_K4", element).val(data.answer.student_K4);
        if (data.answer.student_s.length > 0 && data.answer.student_s1.length > 0){
            build_graphic_1();
        }
        if (data.answer.student_sl.length > 0 && data.answer.student_slc.length > 0) {
            build_graphic_2();
        }
    }

    function buttons_disable() {
        var student_data = generateAnswer();
        if (student_data.student_s.length > 0 && student_data.student_s1.length > 0) {
            enable($("#calculate_graphic_1", element));
        }
        else {
            disable($("#calculate_graphic_1", element));
        }
        if (student_data.student_sl.length > 0 && student_data.student_slc.length > 0) {
            enable($("#calculate_graphic_2", element));
        }
        else{
            disable($("#calculate_graphic_2", element));
        }
        if (student_data.student_s.length > 0 && student_data.student_s1.length > 0 && student_data.student_sl.length > 0 && student_data.student_slc.length > 0){
            if (parseFloat(student_data.student_fn) && parseFloat(student_data.student_Np)){
                if (parseFloat(student_data.student_K1) && parseFloat(student_data.student_K2) && parseFloat(student_data.student_K3) && parseFloat(student_data.student_K4)){
                    enable($("#check_answer", element));
                }
                else{
                    disable($("#check_answer", element));
                }
            }
            else{
                disable($("#check_answer", element));
             }
        }
        else{
            disable($("#check_answer", element));
        }
    }

    function clearSelection()
    {
     if (window.getSelection) {window.getSelection().removeAllRanges();}
     else if (document.selection) {document.selection.empty();}
    }

    $('.copy_to_clipboard', element).click(function (event) {
        var id = this.id.split("_")[this.id.split("_").length-1];
        var textarea = $('#display_signal_'+id, element);
        textarea.select();
        document.execCommand("copy");
        var tooltip = $('#copy_to_clipboard_'+id+" .copy-to-clipboard-tooltiptext", element)[0];
        tooltip.innerHTML = "Сигнал скопирован в буфер обмена!";
        $(textarea).blur();
        clearSelection();
    });

     $('.copy_to_clipboard', element).mouseout(function() {
        var id = this.id.split("_")[this.id.split("_").length-1];
        var tooltip = $('#copy_to_clipboard_'+id+" .copy-to-clipboard-tooltiptext", element)[0];
        tooltip.innerHTML = "Скопировать сигнал в буфер обмена";
      });


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
            clean_bottom_notification($('.dsp-notification', element);
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