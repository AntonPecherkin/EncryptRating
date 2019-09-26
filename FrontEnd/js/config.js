let config_bits = 1024;

$("#li").click(function() {
    $("#li").addClass("active");
});

let ip_pk = 'http://presumo.serveo.net';
let ip = 'http://cedo.serveo.net';

function getPublicKey() {
    fetch(ip_pk+'/phe_public_key',
        {
            headers: {
                'Content-Type': 'application/json',
            },
            method: 'GET'
        })
        .then((res1) => {
            console.log('res1.token', res1.json()
                .then((res2)=>{
                    console.log('res2',res2);
                    localStorage.setItem('public_key', res2.phe_pk);
                }));
        });
}

let James = '<li class="item">\n' +
    '                <div class="row">\n' +
    '\n' +
    '                    <div class="col s2">\n' +
    '                        <img src="css/images/1.jpg" alt="" class="circle ava">\n' +
    '                    </div>\n' +
    '                    <div class="col s6">\n' +
    '                        <h4 class="text-left">James Taylor</h4>\n' +
    '                        <h6 class="position">Chief Technical Officer</h6>\n' +
    '                    </div>\n' +
    '                    <div class="col s1">\n' +
    '                    </div>\n' +
    '                    <div class="col s3 marging">\n' +
    '                        <h4 class="text-left" id="0"></h4>\n' +
    '                    </div>\n' +
    '                </div>\n' +
    '            </li>';
let Joseph = '<li class="item">\n' +
    '                <div class="row">\n' +
    '\n' +
    '                    <div class="col s2">\n' +
    '                        <img src="css/images/2.jpg" alt="" class="circle ava">\n' +
    '                    </div>\n' +
    '                    <div class="col s6">\n' +
    '                        <h4 class="text-left">Joseph Walsh</h4>\n' +
    '                        <h6 class="position">Purchasing Manager</h6>\n' +
    '                    </div>\n' +
    '                    <div class="col s1">\n' +
    '                    </div>\n' +
    '                    <div class="col s3 marging">\n' +
    '                        <h4 class="text-left" id="1"></h4>\n' +
    '                    </div>\n' +
    '                </div>\n' +
    '            </li>';
let Linda = '<li class="item">\n' +
    '                <div class="row">\n' +
    '\n' +
    '                    <div class="col s2">\n' +
    '                        <img src="css/images/3.jpg" alt="" class="circle ava">\n' +
    '                    </div>\n' +
    '                    <div class="col s6">\n' +
    '                        <h4 class="text-left">Linda Walker</h4>\n' +
    '                        <h6 class="position">Sales Manager</h6>\n' +
    '                    </div>\n' +
    '                    <div class="col s1">\n' +
    '                    </div>\n' +
    '                    <div class="col s3 marging">\n' +
    '                        <h4 class="text-left" id="2"></h4>\n' +
    '                    </div>\n' +
    '                </div>\n' +
    '            </li>';
let Daniel = '<li class="item">\n' +
    '                <div class="row">\n' +
    '\n' +
    '                    <div class="col s2">\n' +
    '                        <img src="css/images/4.jpg" alt="" class="circle ava">\n' +
    '                    </div>\n' +
    '                    <div class="col s6">\n' +
    '                        <h4 class="text-left">Daniel Li</h4>\n' +
    '                        <h6 class="position">PR Manager</h6>\n' +
    '                    </div>\n' +
    '                    <div class="col s1">\n' +
    '                    </div>\n' +
    '                    <div class="col s3 marging">\n' +
    '                        <h4 class="text-left" id="3"></h4>\n' +
    '                    </div>\n' +
    '                </div>\n' +
    '            </li>';
let Lisa = '<li class="item">\n' +
    '                <div class="row">\n' +
    '\n' +
    '                    <div class="col s2">\n' +
    '                        <img src="css/images/5.jpg" alt="" class="circle ava">\n' +
    '                    </div>\n' +
    '                    <div class="col s6">\n' +
    '                        <h4 class="text-left">Lisa Turner</h4>\n' +
    '                        <h6 class="position">Chief Accounting Officer</h6>\n' +
    '                    </div>\n' +
    '                    <div class="col s1">\n' +
    '                    </div>\n' +
    '                    <div class="col s3 marging">\n' +
    '                        <h4 class="text-left" id="4"></h4>\n' +
    '                    </div>\n' +
    '                </div>\n' +
    '            </li>';
