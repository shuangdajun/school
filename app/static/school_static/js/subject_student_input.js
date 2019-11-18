//  关于一些参数说明：
//  *bodycontent:要在窗口显示的内容，dom对象
//  *title:窗口标题，字符串类型
//  *removeable:窗口能否拖动，布尔类型
//  *注意：内容窗体的高度是height-30px，请计算好你要显示的内容的高度和宽度。弹出窗的id为"223238909"，所以你的页面不要再取值为"223238909"的id了，以防js执行出错*/
function createdialog(width, height, bodycontent, title, search, removeable, ) {
    if (document.getElementById("www_jb51_net") == null) {
        /*创建窗口的组成元素*/
        var dialog = document.createElement("div");
        var dialogtitlebar = document.createElement("div");
        var dialogbody = document.createElement("div");
        var dialogtitleimg = document.createElement("span");
        var dialogtitle = document.createElement("span");
        var dialogsearch = document.createElement("span");
        var dialogsearch_input = document.createElement("input")
        var dialogsearchbutton = document.createElement("button")
        var dialogclose = document.createElement("span");
        var closeaction = document.createElement("button");

        /*为窗口设置一个id，id如此怪异是为了尽量避免与其他用户取的id相同而出错*/
        dialog.id = "223238909";
        /*组装对话框标题栏,按从里到外的顺序组装*/
        dialogtitle.innerHTML = title;
        dialogsearch.innerHTML = search;
        //dialogtitlebar.appendChild(dialogtitleimg);
        dialogtitlebar.appendChild(dialogtitle);
        dialogtitlebar.appendChild(dialogsearch);
        dialogtitlebar.appendChild(dialogsearch_input);
        dialogtitlebar.appendChild(dialogsearchbutton)

        dialogtitlebar.appendChild(dialogclose);
        dialogclose.appendChild(closeaction);
        closeaction.innerHTML = "X"
        /*组装对话框主体内容*/
        if (bodycontent != null) {
            bodycontent.style.display = "block";
            dialogbody.appendChild(bodycontent);
        }
        /*组装成完整的对话框*/
        dialog.appendChild(dialogtitlebar);
        dialog.appendChild(dialogbody);
        /*设置窗口组成元素的样式*/
        var templeft, temptop, tempheight//窗口的位置（将窗口放在页面中间的辅助变量）
        var dialogcssText, dialogbodycssText;//拼出dialog和dialogbody的样式字符串
        templeft = (document.body.clientWidth - width) / 2;
        temptop = (document.body.clientHeight - height) / 2;
        tempheight = height - 30;
        dialogcssText = "position:absolute;padding:1px;border:4px;top:" + temptop + "px;left:" + templeft + "px;height:" + height + "px;width:" + width + "px;";
        dialogbodycssText = "width:100%;background:#ffffff;";

        dialog.style.cssText = dialogcssText;
        dialogtitlebar.style.cssText = "height:30px;width:100%;background:cornflowerblue;cursor:move;";
        dialogbody.style.cssText = dialogbodycssText;
        //dialogtitleimg.style.cssText = "float:left;height:20px;width:20px;background:url(images/40.gif);"+"display:block;margin:4px;line-height:20px;";
        dialogtitle.style.cssText = "font-size:16px;float:left;display:block;margin:4px;line-height:20px;margin-right:371px;";
        dialogsearch.style.cssText = "font-size:16px;float:left;display:block;margin:4px;line-height:20px;"
        dialogsearch_input.style.cssText = "font-size:16px;float:left;display:block;margin:2px;line-height:20px;"
        dialogsearch_input.id = "search_input"
        dialogsearch_input.type = "text"
        dialogsearchbutton.style.cssText = "font-size:16px;float:left;display:block;margin:2px;line-height:20px;"
        dialogsearchbutton.innerHTML = "确定"
        dialogsearchbutton.id = "search_button"
        dialogclose.style.cssText = "float:right;display:block;margin:4px;line-height:20px;";
        closeaction.style.cssText = "height:20px;width:24px;border-width:1px;" + "background-image:url(images/close.png);cursor:pointer;";
        closeaction.id = "close"
        /*为窗口元素注册事件*/
        var dialogleft = parseInt(dialog.style.left);
        var dialogtop = parseInt(dialog.style.top);
        var ismousedown = false;//标志鼠标是否按下
        /*关闭按钮的事件*/
        closeaction.onclick = function () {
            dialog.parentNode.removeChild(dialog);
            clickstudent.disabled = false;
        }

        dialogsearchbutton.onclick = function () {
            var input_search = document.getElementById("search_input").value;

            if (input_search != "" ) {
                $.ajax({
                    url: ajax_url,
                    type: "POST",
                    async: false,
                    data: {"search_student": input_search},
                    success: function (result) {
                        searchPage(result)
                    }
                })
            }
            else {

                firstPage()
            }

        }

        /*实现窗口的移动，这段代码很典型，网上很多类似的代码*/
        if (removeable == true) {
            var ismousedown = false;
            var dialogleft, dialogtop;
            var downX, downY;
            dialogleft = parseInt(dialog.style.left);
            dialogtop = parseInt(dialog.style.top);
            dialogtitle.onmousedown = function (e) {
                ismousedown = true;
                downX = e.clientX;
                downY = e.clientY;
            }
            document.onmousemove = function (e) {
                if (ismousedown) {
                    dialog.style.top = e.clientY - downY + dialogtop + "px";
                    dialog.style.left = e.clientX - downX + dialogleft + "px";
                }
            }
            /*松开鼠标时要重新计算当前窗口的位置*/
            document.onmouseup = function () {
                dialogleft = parseInt(dialog.style.left);
                dialogtop = parseInt(dialog.style.top);
                ismousedown = false;
            }

        }
        return dialog;
    }//end if(if的结束)
}
