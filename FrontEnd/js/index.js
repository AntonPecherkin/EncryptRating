function encrypt_number (val) {
    let valA = parseInt(val);
    let keys = paillier.generateKeyFromString(public_key);
    let enc = keys.pub.encrypt(nbv(valA));

    return enc;
}
var rating1 = '';
var rating2 = '';
var rating3 = '';
var rating4 = '';
var rating5 = '';
function rate(rating, position) {
    switch (position) {
        case 1: rating1 = encrypt_number(rating).toString();
            break;
        case 2: rating2 = encrypt_number(rating).toString();
            break;
        case 3: rating3 = encrypt_number(rating).toString();
            break;
        case 4: rating4 = encrypt_number(rating).toString();
            break;
        case 5: rating5 = encrypt_number(rating).toString();
            break;
    }
}

function submit() {

    let json = '{\n' +
        '"1": "' + rating1 + '",\n' +
        '"2": "' + rating2 + '",\n' +
        '"3": "' + rating3 + '",\n' +
        '"4": "' + rating4 + '",\n' +
        '"5": "' + rating5 + '"\n' +
        '}';
    console.log("POST");
    //fetch('http://localhost:8080/set',
    fetch(ip+'/set',
        {
            headers: {
                'Content-Type': 'application/json',
            },
            method: 'POST',
            body: json
        })
        .then((res1) => {
            console.log('res1.token', res1.json()
                .then((res2)=>{
                }));

        });
    location = window.location.href.slice(0,window.location.href.lastIndexOf('/'))+'/prompage.html';
}

function getResults() {
    //fetch('http://localhost:8080/getRes',
    fetch(ip+'/getRes',
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

                    let resList = res2;
                    for (let i = 0; i < resList.length; i++) {

                    }

                }));

        });
}