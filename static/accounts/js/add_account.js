// let json_accounts = [];


// try{
// 	let tmp_accounts = JSON.parse(localStorage.getItem("json_accounts"));

// 	tmp_accounts.map((account)=>{
// 		console.log(account);
// 		json_accounts.push(account);
// 	});
// 	for(let i=0;i<tmp_accounts.length;i++){
// 		let account = {
// 			name: tmp_accounts[i].name,
// 			email: tmp_accounts[i].email,
// 			username: tmp_accounts[i].username,
// 			password: tmp_accounts[i].password,
// 			confirm: tmp_accounts[i].confirm			
// 		}
// 		json_accounts.push(account);
// 	}
// }
// catch(TypeError){
// 	localStorage.setItem('json_accounts',JSON.stringify(json_accounts));
// }


function createUser(){

	let name = document.querySelector('#name').value;
	let email = document.querySelector('#email').value;
	let username = document.querySelector('#username').value;
	let password = document.querySelector('#password').value;
	let confirm = document.querySelector('#confirm').value;
	let newAccount = {
		name: name,
		email: email,
		username: username,
		password: password,
		confirm: confirm
	}

	const MongoClient = require('mongodb').MongoClient;
	const MONGO_URL = 'mongodb://localhost:27017/data';

	MongoClient.connect(MONGO_URL, (err, db) => {  
	  if (err) {
	    return console.log(err);
	  }

		   db.collection('signup_storage').insertOne(
	    {
	      	name: name,
			email: email,
			username: username,
			password: password,
			confirm: confirm
	    },
	    function (err, res) {
	      if (err) {
	        db.close();
	        return console.log(err);
	      }
	      // Success
	      db.close();
	    }
	  )
	});
}
		


	// json_accounts.push(newAccount);



	// console.log(json_accounts);
	// localStorage.setItem('json_accounts',JSON.stringify(json_accounts));

	// let jns_retrieve = localStorage.getItem('json_accounts');
	// console.log(jns_retrieve);

	// let jns_parse = JSON.parse(localStorage.getItem('json_accounts'));
	// console.log(jns_parse);

	// //Display in console inside of json array
	// console.log("Name is " + jns_parse[0].name);
	// console.log("Email is " + jns_parse[0].email);

