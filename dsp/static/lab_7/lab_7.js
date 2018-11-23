
/* Javascript for DSPXBlock. */
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







    $(function ($) {
        console.log(data);
        // if (data.student_state.answer) {
        //     build_lab_state(data["student_state"]);
        //     $("textarea.array-input", element).each(function (i) {
        //         process_array_input(this);
        //     });
        //     if (data.student_state.correctness && highlight_correct) {
        //         highlight_correctness(data["student_state"]["correctness"]);
        //     }
        // }
        // buttons_disable();

        $(element).on('input', ".answer-input", function () {
            // buttons_disable();
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
