// вытаскиваем url странички и изменяем на тот, что требуется:
var url = window.location.href.split("?")[0] + "get_users/";

// запрос на сервер:
$.get(
    url,
    onAjaxSuccess
);

// действия после получения ответа от сервера:
function onAjaxSuccess(data) {
    var $button = $(".container-fluid")
    $button.empty().append(data);
}
