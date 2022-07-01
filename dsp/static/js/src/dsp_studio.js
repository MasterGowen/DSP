function DSPXBlock(runtime, element) {

    document.getElementsByClassName("editor-modes action-list action-modes")[0].innerHTML = "<li class=\"action-tabs is-active-tabs\" id=\"scenario-settings-tab\">Основные</li><li class=\"action-tabs\" id=\"advanced-settings-tab\">Расширенные</li>";

    document.querySelector("#scenario-settings-tab").onclick = function () {
        document.querySelector("#scenario-settings-tab").classList.add("is-active-tabs");
        document.querySelector("#advanced-settings-tab").classList.remove("is-active-tabs");
        document.querySelector("#scenario-settings").removeAttribute("hidden");
        document.querySelector("#advanced-settings").setAttribute("hidden", "true");
    };

    document.querySelector("#advanced-settings-tab").onclick = function () {
        document.querySelector("#scenario-settings-tab").classList.remove("is-active-tabs");
        document.querySelector("#advanced-settings-tab").classList.add("is-active-tabs");
        document.querySelector("#scenario-settings").setAttribute("hidden", "true");
        document.querySelector("#advanced-settings").removeAttribute("hidden");
    };

    $(document).ready(function () {
        let $selectLab = $('.select-lab'),
            $group = $('.group');
        $group.hide();
        $('#' + $selectLab.val()).show();
        $selectLab.change(function () {
            $group.hide();
            $('#' + $(this).val()).show();
        })
    });

    $(element).find(".save-button").bind("click", function () {

        let handlerUrl = runtime.handlerUrl(element, "studio_submit"),
            data = {
                "display_name": $(element).find("input[name=display_name]").val(),
                "current_lab": $(element).find("select[name=lab_scenario]").val(),
                "weight": $(element).find("input[name=weight]").val(),
                "max_attempts": $(element).find("input[name=max_attempts]").val(),
                "array_tolerance": $(element).find("input[name=array_tolerance]").val(),
                "number_tolerance": $(element).find("input[name=number_tolerance]").val(),
                "show_reset_button": $(element).find("select[name=show_reset_button]").val(),
            };

        $.post(handlerUrl, JSON.stringify(data)).done(function (response) {
            window.location.reload();
        });

    });


    $(element).find(".cancel-button").bind("click", function () {
        runtime.notify("cancel", {});
    });
}