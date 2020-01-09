//Created by lx on 2016/11/15.
var oCHCK = function () {
    var oChuser = false;
    var chxm = false;

    var chpassword = false;

    var oCheck = document.getElementById('ocheck');    //父级IDIdName  oChxm
    var nowTime = new Date();
    var yearTime = nowTime.getFullYear() + 1 + "-" + (nowTime.getMonth() + 1) + "-" + nowTime.getDate();

    console.log(yearTime);
    var oChxmObject = getByClass(oCheck, 'oChxm')[0];
    var oChpassObject = getByClass(oCheck, 'oChpass')[0];
    var ostopTimeObject = getByClass(oCheck, 'ostopTime')[0];
    var oChuserObject = getByClass(oCheck, 'oChuser')[0]

    function getByClass(o, s)//获取Class;
    {
        var aEle = document.getElementsByTagName('*');
        // console.log(aEle)
        var arr = [];
        for (var i = 0; i < aEle.length; i++) {
            if (aEle[i].id == s) {
                arr.push(aEle[i])
            }

        }

        return arr;
    }

//姓名校验
    //ClassName  oChxm
    function oChxm() {


        var reQQ = /[\u4E00-\u9FA5]/g;
        oChxmObject.onkeyup = function () {
            // if (this.value.length > 20) {
            //     this.value = this.value.substr(0, 20)
            // }
            if (reQQ.test(this.value)) {
                this.nextSibling.nextSibling.innerHTML = '输入正确';
                this.nextSibling.nextSibling.className = 'ingreen';
                chxm = true;

                return;
            } else {

                this.nextSibling.nextSibling.innerHTML = '请输入正确的姓名';
                this.nextSibling.nextSibling.className = 'inred';
                chxm = false;
                return;
            }
        }

    }

    oChxm();
// 密码校验
    //ClassName  oChphone
    function oChpassword() {

        var reQQ = new RegExp('(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[^a-zA-Z0-9]).{8,30}');
        ;
        oChpassObject.onkeyup = function () {

            if (reQQ.test(this.value)) {
                this.nextSibling.nextSibling.innerHTML = '输入正确';
                this.nextSibling.nextSibling.className = 'ingreen';
                chpassword = true;
                return;
            } else {
                this.nextSibling.nextSibling.innerHTML = '请输入正确的密码';
                this.nextSibling.nextSibling.className = 'inred';
                chpassword = false;
                return;
            }
        }
    }

    oChpassword();
// QQ校验
    //ClassName  oChQQ
    // function oChQQ() {
    //     var oChQQ = getByClass(oCheck, 'oChQQ')[0];
    //     var reQQ = /^[1-9]\d{5,12}$/;
    //     oChQQ.onkeyup = function () {
    //         if (this.value.length >= 14) {
    //             this.value = this.value.substr(0, 14)
    //         }
    //         if (reQQ.test(this.value)) {
    //             this.nextSibling.innerHTML = '输入正确';
    //             this.nextSibling.className = '';
    //             this.nextSibling.className = 'ingreen';
    //             chQQ = true;
    //             return;
    //         } else {
    //             this.nextSibling.innerHTML = '请输入正确的QQ号码';
    //             this.nextSibling.className = '';
    //             this.nextSibling.className = 'inred';
    //             chQQ = false;
    //             return;
    //         }
    //     }
    // }

    // oChQQ();
//邮箱校验
//     function oChmail() {
//         var oChmail = getByClass(oCheck, 'oChmail')[0];
//         var reMail = /^\w+@[a-z0-9]+\.[a-z]+$/i;
//         oChmail.onkeyup = function () {
//             if (this.value.length >= 30) {
//                 this.value = this.value.substr(0, 30)
//             }
//             if (reMail.test(this.value)) {
//                 this.nextSibling.innerHTML = '输入正确';
//                 this.nextSibling.className = '';
//                 this.nextSibling.className = 'ingreen';
//                 chMail = true;
//                 return;
//             } else {
//                 this.nextSibling.innerHTML = '请输入正确的邮箱';
//                 this.nextSibling.className = '';
//                 this.nextSibling.className = 'inred';
//                 chMail = false;
//                 return;
//             }
//
//         }
//     }

    // // oChmail();
    var oCheckSbumit = getByClass(window, 'btn')[0];

    oCheckSbumit.onclick = function () {
        oCheckSbumit1();
    };

    function oCheckSbumit1() {
        var chckevalue = true;
        console.log(oChuserObject.value)
        if (oChuserObject.value == "") {
            oChuserObject.nextSibling.nextSibling.innerHTML = "用户名不允许为空";
            oChuserObject.nextSibling.nextSibling.className = 'inred';

        }
        if (chxm != true) {
            oChxmObject.nextSibling.nextSibling.innerHTML = '请输入正确的姓名';

            oChxmObject.nextSibling.nextSibling.className = 'inred';
            chckevalue = false;

        }
        if (chpassword != true) {
            oChpassObject.nextSibling.nextSibling.innerHTML = '请输入正确的姓名';
            oChpassObject.nextSibling.nextSibling.className = 'inred';
            chckevalue = false;

        }
        if (ostopTimeObject.value == "") {
            ostopTimeObject.value = yearTime
        }
        if (chckevalue == true) {
            document.getElementById("form").submit()
        } else {
            console.log(ostopTimeObject.value)
            return false
        }

    }

    // window.onkeyup = function () {
    //     console.log('检查是否通过验证:\n' + '姓名' + chxm + '\n' + '手机' + chphone + '\n' + 'QQ' + chQQ + '\n' + '邮箱' + chMail)
    // }
};
oCHCK();