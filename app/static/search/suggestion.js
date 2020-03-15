$('#user_input').on('input', function (e) {

    var user_input = $('#user_input').val();

    console.log(user_input);

    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "/search/suggestion",
        "method": "POST",
        "headers": {
            "cache-control": "no-cache",
            "Content-Type": "application/json"
        },
        "processData": false,
        data: "q=" + user_input
    }


    $.ajax(settings).done(function (response) {
        console.log(response);
        var data = response.data;
        console.log(data.length);

        titles = [];
        for (var i = 0; i < data.length; i++) {
            field_name = data[i]["_source"]["name"] || data[i]["_source"]["detail"] || data[i]["_source"]["value"] || data[i]["_source"]["store_name"] || data[i]["_source"]["price"];
            titles.push(field_name);
        }
        console.log(titles);


        $('#user_input').autocomplete(
            {
                source: titles,
                delay: 300,
                open: function () {
                    $('.ui-autocomplete').width('50%');
                    $('.ui-widget-content').css('background', '#fff');
                    $('.ui-menu-item a').css('color', '#000');
                    $('.ui-menu-item').css('margin-bottom', '1rem');
                    $('.ui-menu-item a:hover').css('color', 'red !important');
                    $('.ui-menu').css('border-bottom-left-radius', '30px');
                    $('.ui-menu').css('border-bottom-right-radius', '30px');
                    $('.ui-menu').css('box-shadow', '0 3px 8px 0 rgba(0,0,0,0.2), 0 0 0 1px rgba(0,0,0,0.08)');
                    $('.ui-menu').css('list-style', 'none');
                    $('.ui-menu-item a').removeClass('ui-corner-all');
                },
                select: function (event, ui) {
                    if (ui.item) {
                        var settings_get_store = {
                            "async": true,
                            "crossDomain": true,
                            "url": "/store",
                            "method": "POST",
                            "headers": {
                                "cache-control": "no-cache",
                                "Content-Type": "application/json"
                            },
                            "processData": false,
                            data: "name=" + ui.item.value
                        }
                        $.ajax(settings_get_store).done(function (data) {
                            window.location.href = "/stores/" + data.id;
                        })
                    }
                }

            }
        ).data("ui-autocomplete")._renderItem = function (ul, item) {
            return $("<li>")
                .append("<a>" + item.label + "</a>")
                .appendTo(ul);
        };

    });
});



