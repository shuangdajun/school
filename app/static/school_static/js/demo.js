$(function () {


    var tag_data_stu;
    var tag_data_tea;
    var tag_data_sub;
    $.ajax({
        url: "comboSelectStu",
        type: "POST",
        async: false,
        success: function (result) {
            tag_data_stu = result
        }
    });

    $.ajax({
        url: "comboSelectTea",
        type: "POST",
        async: false,
        success: function (result) {
            tag_data_tea = result
        }
    });
    console.log(tag_data_tea)
    $.ajax({
        url: "comboSelectSub",
        type: "POST",
        async: false,
        success: function (result) {
            tag_data_sub = result
        }
    });
    console.log(tag_data_sub)
    $('#comboSelectStudent').bComboSelect({
        showField: 'name',
        keyField: 'id',
        data: tag_data_stu
    });
    $('#comboSelectTeacher').bComboSelect({
        showField: 'name',
        keyField: 'id',
        data: tag_data_tea
    });
    $('#comboSelectSubject').bComboSelect({
        showField: 'name',
        keyField: 'id',
        data: tag_data_sub
    });

});