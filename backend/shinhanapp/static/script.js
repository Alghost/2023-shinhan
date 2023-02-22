$(document).ready(function () {
    $(".list-group-item-action").click(function () {
        let product_id = $(this).attr('id');
        $.get("http://127.0.0.1:8000/product/"+ product_id + "/")
            .then(function (result){
                $("#detailModalImage").attr("src", result.image);
                $("#detailModalUsername").text(result.username);
                $("#detailModalTitle").text(result.title);
                $("#detailModalLocation").text(result.location);
                $("#detailModalPrice").text(result.price);
                $("#detailModalContent").html(result.content);
                $("#detailModal").modal("show");
            });
    });
});
// 잘 작성한 것 같은데 반영이 안되는 것 같다면?
// Ctrl + Shift + R 로 페이지를 새로고침해보세요!