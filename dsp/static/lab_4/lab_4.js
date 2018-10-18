/* Javascript for DSPXBlock. */
function DSPXBlock(runtime, element) {



    $(function ($) {
        $("textarea.array-input", element).each(function (i) {
            $(this).change(function () {
                process_array_input(this);
            });
        });
    });
}
