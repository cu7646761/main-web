/*
 |--------------------------------------------------------------------------
 | Shards Dashboards: Blog Add New Post Template
 |--------------------------------------------------------------------------
 */

'use strict';
var test = new Object();
(function ($) {
    $(document).ready(function () {
        var toolbarOptions = [
            [{'header': [1, 2, 3, 4, 5, false]}],
            ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
            ['blockquote', 'code-block'],
            [{'header': 1}, {'header': 2}],               // custom button values
            [{'list': 'ordered'}, {'list': 'bullet'}],
            [{'script': 'sub'}, {'script': 'super'}],      // superscript/subscript
            [{'indent': '-1'}, {'indent': '+1'}],          // outdent/indent         // remove formatting button
            ['image', 'link'],
        ];

        var IMGUR_CLIENT_ID = 'bcab3ce060640ba';
        // var IMGUR_API_URL = 'https://api.imgur.com/3/image';
        var IMGUR_API_URL = 'http://127.0.0.1:5000/admin/store/images/';


        // Init the Quill RTE
        var quill = new Quill('#editor-container', {
            modules: {
                // imageResize: {
                //     displaySize: true
                // },
                toolbar: toolbarOptions,
            },
            placeholder: 'Viết thêm mô tả cho cửa hàng ...',
            theme: 'snow',
        });

        let postContent = $('#editor-container').data("postId");

        // quill.setText(postContent);
        quill.clipboard.dangerouslyPasteHTML(0, postContent);


        Object.assign(test, quill)

        quill.getModule('toolbar').addHandler('image', (quill) => {
            console.log("huhu0")
            selectLocalImage(quill);
        });

        function selectLocalImage() {
            console.log("huhu")
            const input = document.createElement('input');
            input.setAttribute('type', 'file');
            input.click();

            // Listen upload local image and save to server
            input.onchange = () => {
                const file = input.files[0];
                // file type is only image.
                if (/^image\//.test(file.type)) {
                    imageHandler(file, insertToEditor);
                } else {
                    console.warn('You could only upload images.');
                }
            };
        }

        function insertToEditor(url) {

            // push image url to rich editor.
            const range = quill.getSelection();
            console.log("%%%")
            quill.insertEmbed(range.index, 'image', url);
        }

        var imageHandler = (image, callback) => {
            var data = new FormData();
            data.append('image', image);
            var xhr = new XMLHttpRequest();
            xhr.open('POST', IMGUR_API_URL, true);
            // xhr.setRequestHeader('Authorization', 'Client-ID ' + IMGUR_CLIENT_ID);
            // xhr.setRequestHeader('Content-Type', 'multipart/form-data');
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4) {
                    var response = JSON.parse(xhr.responseText);
                    // if (response.status === 200 && response.success) {
                    if ("image_url" in response) {
                        callback(response.image_url);
                    } else {
                        var reader = new FileReader();
                        reader.onload = function (e) {
                            callback(e.target.result);
                        };
                        reader.readAsDataURL(image);
                    }
                }
            }
            xhr.send(data);
        }

        let thumbnailPost = $('#thumbnail-post').data("thumbnailPost");
        if (thumbnailPost !== "") {
            $('.image-upload-wrap').hide();

            $('.file-upload-image').attr('src', thumbnailPost);
            $('.file-upload-content').show();

            $('.image-title').html("thumbnail.jpg");
        }

    });
})(jQuery);

var IMGUR_API_URL = 'http://127.0.0.1:5000/admin/store/images/';

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            // $('.image-upload-wrap').hide();

            // $('.file-upload-image').attr('src', e.target.result);
            // $('.file-upload-content').show();

            $('.image-title').html(input.files[0].name);
        };

        reader.readAsDataURL(input.files[0]);


        let thumbnail = input.files[0]

        var data = new FormData();
        data.append('image', thumbnail);
        var xhr = new XMLHttpRequest();
        xhr.open('POST', IMGUR_API_URL, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                var response = JSON.parse(xhr.responseText);
                console.log(response)
                // if (response.status === 200 && response.success) {
                if ("image_url" in response) {
                    $('.image-upload-wrap').hide();
                    $('.file-upload-image').attr('src', response.image_url);
                    $('.file-upload-content').show();
                } else {
                    var reader = new FileReader();
                    reader.onload = function (e) {
                        $('.image-upload-wrap').hide();
                        $('.file-upload-image').attr('src', e.target.result);
                        $('.file-upload-content').show();
                    };
                    reader.readAsDataURL(image);
                }
            }
        }
        xhr.send(data);

    } else {
        removeUpload();
    }
}

function removeUpload() {
    // delete_img
    let origin_img = $('#thumbnail-post').attr('data-thumbnail-post');
    $('#delete_img').val(origin_img);
    console.log($('#delete_img').val());
    $('.file-upload-input').replaceWith($('.file-upload-input').clone());
    $('.file-upload-content').hide();
    $('.image-upload-wrap').show();
}

$('.image-upload-wrap').bind('dragover', function () {
    $('.image-upload-wrap').addClass('image-dropping');
});
$('.image-upload-wrap').bind('dragleave', function () {
    $('.image-upload-wrap').removeClass('image-dropping');
});

function onTypeTitle() {
    var title = document.getElementById("post-title").value;
}

function remove_accents(strAccents) {
    var strAccents = strAccents.split('');
    var strAccentsOut = new Array();
    var strAccentsLen = strAccents.length;
    var accents = "ÀÁÂÃÄÅàáâãäåÒÓÔÕÕÖØòóôõöøÈÉÊËèéêëðÇçÐđÌÍÎÏìíîïÙÚÛÜùúûüÑñŠšŸÿýŽž";
    var accentsOut = "AAAAAAaaaaaaOOOOOOOooooooEEEEeeeeeCcDdIIIIiiiiUUUUuuuuNnSsYyyZz";
    for (var y = 0; y < strAccentsLen; y++) {
        if (accents.indexOf(strAccents[y]) != -1) {
            strAccentsOut[y] = accentsOut.substr(accents.indexOf(strAccents[y]), 1);
        } else
            strAccentsOut[y] = strAccents[y];
    }
    strAccentsOut = strAccentsOut.join('');

    return strAccentsOut;
}

function getAttrFromString(str, node, attr) {
    var regex = new RegExp('<' + node + ' .*?' + attr + '="(.*?)"', "gi"), result, res = [];
    while ((result = regex.exec(str))) {
        res.push(result[1]);
    }
    return res;
}

document.getElementById("update-post-btn").addEventListener("click", () => {
    let store_id = $('#store_id').val()
    let title = $('#post-title').val()
    let content = $('.ql-editor').html()
    let thumbnail = $('.file-upload-image').attr('src')
    // let categories = [$('#love_cate').val()]
    let address_detail = $('#result-address').val()
    let categories = []
    console.log(categories)
    $('input[type=checkbox]').each(function () {
        if (this.checked){
            categories.push($(this).val()) ;
            console.log("hehe")
            console.log(categories)
        }
    });
    let delete_img = $('#delete_img').val();
    
    if ((title === "") || (content === "") || (thumbnail === "#") || (address_detail === "") || (categories.length == 0)) {
        alert("Bạn nên điền đầy đủ các thông tin về cửa hàng");
        return;
    }

    let address_district = address_detail.split(",")[1].trim()


    var http = new XMLHttpRequest();

    console.log(store_id)
    var url = 'http://127.0.0.1:5000/admin/store/edit/' + store_id;
    var params = {
        "description": content,
        "name": title,
        "image": thumbnail,
        "categories": categories,
        "address_detail": address_detail,
        "address_district": address_district,
        "image_list": getAttrFromString(content, 'img', 'src'),
        "delete_img": delete_img
    };
    http.open('POST', url, true);

    //Send the proper header information along with the request
    http.setRequestHeader('Content-type', 'application/json');

    http.onreadystatechange = function () {
        if (http.readyState == 4 && http.status == 200) {
            console.log("Send ok")
            location.replace("http://127.0.0.1:5000/admin/store/edit/" + store_id);
        }
    }
    http.send(JSON.stringify(params));

});




