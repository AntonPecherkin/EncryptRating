function encrypt_number (val) {
    let public_key = localStorage.getItem('public_key');
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
var final_position_1 = 0;
var final_position_2 = 0;
var final_position_3 = 0;
var final_position_4 = 0;
var final_position_5 = 0;

function rate(rating, position) {
    switch (position) {
        case 1: rating1 = rating;//encrypt_number(rating).toString();
            break;
        case 2: rating2 = rating;//encrypt_number(rating).toString();
            break;
        case 3: rating3 = rating;//encrypt_number(rating).toString();
            break;
        case 4: rating4 = rating;//encrypt_number(rating).toString();
            break;
        case 5: rating5 = rating;//encrypt_number(rating).toString();
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
    console.log()
    console.log("POST");,
    fetch(ip+'/phe_votes',
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
                    console.log(res2);
                }));

        });
    location = window.location.href.slice(0,window.location.href.lastIndexOf('/'))+'/prompage.html';
}

function getResults() {

    console.log('Start')
    fetch(ip+'/sorted_votes',
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
                    let map = new Map();
                    map.set("0",resList[0]);
                    map.set("1",resList[1]);
                    map.set("2",resList[2]);
                    map.set("3",resList[3]);
                    map.set("4",resList[4]);
                    map = new Map([...map.entries()].sort((a, b) => a[1] - b[1]));
                    relevantList(map);
                }));

        });
}

function createElementFromHTML(htmlString) {
    var div = document.createElement('div');
    div.innerHTML = htmlString.trim();
    // Change this to div.childNodes to support multiple top-level nodes
    return div.firstChild;
}

function relevantList(map) {
    let first = '1st Place';
    let second = '2nd Place';
    let third = '3rd Place';
    let fourth = '4th Place';
    let fifth = '5th Place';
    map.forEach(function(value, key){
        switch (key) {
            case "0" : {
                let parent = document.getElementById('friend-list');
                let child = createElementFromHTML(James);
                parent.appendChild(child);
                switch (value) {
                    case 0 :
                        document.getElementById('0').innerText = first;
                        break
                    case 1 :
                        document.getElementById('0').innerText = second;
                        break
                    case 2 :
                        document.getElementById('0').innerText = third;
                        break
                    case 3 :
                        document.getElementById('0').innerText = fourth;
                        break
                    case 4 :
                        document.getElementById('0').innerText = fifth;
                        break
                }
            } break
            case "1" : {
                let parent = document.getElementById('friend-list');
                let child = createElementFromHTML(Joseph);
                parent.appendChild(child);
                switch (value) {
                    case 0 :
                        document.getElementById('1').innerText = first;
                        break
                    case 1 :
                        document.getElementById('1').innerText = second;
                        break
                    case 2 :
                        document.getElementById('1').innerText = third;
                        break
                    case 3 :
                        document.getElementById('1').innerText = fourth;
                        break
                    case 4 :
                        document.getElementById('1').innerText = fifth;
                        break
                }
            } break;

            case "2" : {
                let parent = document.getElementById('friend-list');
                let child = createElementFromHTML(Linda);
                parent.appendChild(child);
                switch (value) {
                    case 0 :
                        document.getElementById('2').innerText = first;
                        break
                    case 1 :
                        document.getElementById('2').innerText = second;
                        break
                    case 2 :
                        document.getElementById('2').innerText = third;
                        break
                    case 3 :
                        document.getElementById('2').innerText = fourth;
                        break
                    case 4 :
                        document.getElementById('2').innerText = fifth;
                        break
                }
            } break;

            case "3" : {
                let parent = document.getElementById('friend-list');
                let child = createElementFromHTML(Daniel);
                parent.appendChild(child);
                switch (value) {
                    case 0 :
                        document.getElementById('3').innerText = first;
                        break
                    case 1 :
                        document.getElementById('3').innerText = second;
                        break
                    case 2 :
                        document.getElementById('3').innerText = third;
                        break
                    case 3 :
                        document.getElementById('3').innerText = fourth;
                        break
                    case 4 :
                        document.getElementById('3').innerText = fifth;
                        break
                }
            } break;

            case "4" : {
                let parent = document.getElementById('friend-list');
                let child = createElementFromHTML(Lisa);
                parent.appendChild(child);
                switch (value) {
                    case 0 :
                        document.getElementById('4').innerText = first;
                        break
                    case 1 :
                        document.getElementById('4').innerText = second;
                        break
                    case 2 :
                        document.getElementById('4').innerText = third;
                        break
                    case 3 :
                        document.getElementById('4').innerText = fourth;
                        break
                    case 4 :
                        document.getElementById('4').innerText = fifth;
                        break
                }
            } break;
        }
    })
    let waiter = document.getElementById('waiter');
    waiter.setAttribute('style','display:none');

}