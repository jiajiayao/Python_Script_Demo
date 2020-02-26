
$('.subject_describe').length

let t = $('.subject_type')[0]

$(t).html('<h1>答案：233423452345245245234234235235</h1>')




//取得问题
function getProblem() {

    //获取题目
    let t = $('.subject_describe');

    let len = t.length;

   
    problems = [];
    
    for (let i = 0; i < len; i++){
        problems.push($(t)[i].textContent);
    }


    

    //console.log(problems);

    sendProblem(problems)

}


//发送问题
function sendProblem(problems) {
    problems=JSON.stringify(problems)
    $.ajax({
        type: "get",
        async: true,
        url: "http://127.0.0.1:8080/getAnswer?problem="+problems,
        dataType: "jsonp",
        jsonp:"jsonpCallback",
        jsonpCallback:"success_jsonpCallback",
        success: function(json){
            console.log(json);

            data = json

            for (let i = 0; i < json.length; i++){
                $($('.subject_type')[i]).html('<h1>答案：'+data[i].answer+'</h1>')
            }
        },
    });
}

getProblem()