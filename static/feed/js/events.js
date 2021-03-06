function comment(event){
	event.preventDefault();
	var url = $(this).attr('action');
	$.ajax({
		url: url,
		type: "POST",
		data: $(this).serialize(),
		success: function(data){
			console.log(data);
			var edit;
			if(data.username === data.current_user){
				edit = `<form method="get" action="/feeds/get_comment/`+data.id+`/" class="new-comment-form-active">
							{% csrf_token %}
							<button style="float: right;" type="submit">...</button>
						</form>`;
			}

			$('.insertComment'+data.post_id).prepend(`
				<div id='comment_id-`+data.id+`'>
					<form action="/feeds/delete_comment/`+data.id+`/" method="post" class="new-delete-comment">
					{% csrf_token %}
					<button style="float: right;" type="submit">x</button>
					</form>`
					+edit+
					`
					<div class="padding-comments">
						<span class="comment-user" id="comment-user">
							<a href="#" style="color: black;">`
							+data.username+ `|
							</a> 
						</span>
						<span class="comment">`
						+data.comment+
						`</span>
						<div id='comment-up-`+data.id+`' class="edit-comment-form" style="display: none;">
							<form action="/feeds/edit_comment/`+data.id+`/" method="post" class="edit-comment">
								{% csrf_token %}
								{{ comment_form.comment|add_class:'text-box'|attr:"style:width:620px;"|attr:'id:comment-edit'|attr:"placeholder:Edit Comment Here" }}
								
							
							<button style="float: right;" type="submit">Edit</button>
							</form>
							<button style="float: right;" id="cancel-edit-comment-`+data.id+`">Cancel</button>
						</div>
						<br>
						 <h4 style="font-size: 12px;">
						 	Commented on:` +data.commented_at+
						`</h4>
					</div>
				</div>`);

			$('.text-box').val('');
			$('.new-comment-form-active').submit(comment_active);
			$('.new-delete-comment').submit(delete_comment);
			$('.edit-comment').submit(edit_comment);
		}
	});
}

function like(event){
	event.preventDefault();
	console.log('liked');
	var url = $(this).attr('action');
	$.ajax({
		url: url,
		type: "POST",
		data: $(this).serialize(),
		success: function(data){
			$('#like-no'+data.id).replaceWith(`
				<h4 class='post' id='like-no`+data.id+`' style="margin-right: 100px;">`+
					data.likes+` Likes
				</h4>`
				);
		}
	});
}

function likers(event){
	event.preventDefault();
	var url = $(this).attr('action')
	$('#popup1').addClass('active');
	
	$.ajax({
		url:url,
		data: $(this).serialize(),
		success: function(data){
			console.log(data);
			var prof_pic;
			for(var i = 0; i < data['data'].length; i++){
				if(data['data'][i].prof_pic === ""){
					prof_pic = `<img src="/static/user_profile/img/blank_picture.png" style="border-radius:50%;width:15%;margin-right:10px;">`;
				}
				else{
					prof_pic = `<img src="/media/`+data['data'][i].prof_pic+`" style="border-radius:50%;width:15%;margin-right:10px;">`;
				}

				$('.content').append(`
					<span style="font-size:20px;">`
						+prof_pic+
						data['data'][i].user__username+
					`</span>
					<br><br>`);
			}
		}
	});

	$('.close').on('click',function(event){
		$('#popup1').removeClass('active');
		$('.content').empty();
	});
}

function create_post(event){
	event.preventDefault();
	console.log('clicked');
	var url = $(this).attr('action');
	var data = new FormData(this);
	console.log(data);
	$.ajax({
		url: url,
		type: 'POST',
		data: data,
		cache: false,
		contentType: false,
		processData: false,
		success: function(data){
			console.log(data);
			var current_user = "{{ current_user.username }}";
			var prof_pic;
			var edit;
			if(current_user === data.username){

				edit = `<div id="right">
							<form action="/feeds/archive/`+data.id+`" method="post" class="new-archive_post" style="float: right;margin-right: 10px;">
								{% csrf_token %}
								<button type="submit">✖</button>
							</form>
							<form action="" method="get" class="new-get-edit-forms">
								<button id="edit-btn" style="float: right;margin-right: 10px;" type="submit">...</button>
							</form>
						</div>`;
			}

			
			if(data.prof_pic === undefined){
				prof_pic = "/static/user_profile/img/blank_picture.png"
			}
			else{
				prof_pic = data.prof_pic;
			}
			$('#new-post').prepend(`
			<div id="post-id-`+data.id+`">
				<div id="nav-container">
					<div id="navbar">
						<div id="left">
							<a href="/profile/`+data.username+`">
								<img src=`+prof_pic+` class="feed-prof-pic" >
							</a>
							<h4 class="post" id='feed-prof-username'>
								<a href="/profile/`+data.username+`">`
								+data.username+
								`</a>
							</h4>	
						</div>`+edit+`
						<br><br>
						<div class="padding">
							<h4 class="caption" id="feed-caption">`
							+data.caption+
							`</h4>
						</div>
						<div id='center'>
							<a href="#"><img src="`+data.image+`" width="700px" height="500px"></a>
						</div>
						<br><br>
						<div id="left">
							<form method="post" action="/feeds/like/`+data.id+`/" class="new-like">
								{% csrf_token %}
								<button id="like-btn" class="btn btn-primary btn-lg btn-block register-button" type="submit">Like</button>
							</form>
							<h4 class="post" id="like-no`+data.id+`" style="margin-right: 100px;">
								`+data.likes+` Likes
							</h4>
							<form method="get" action="/feeds/like/`+data.id+`" class="new-likers">
								<button style="margin-right: 10px;">View who liked this...</button>
							</form>	
						</div>
						<br><br><br><br><br><br>
						<div class="comments">
						<div class="insertComment`+data.id+`" ></div>
						</div>
						<form method="post" action="/feeds/comment/`+data.id+`/" class='new-comment-form'>
							{% csrf_token %}
							{{ comment_form.comment|add_class:'text-box' }}
							<input id='create-comment' class="btn btn-primary btn-lg btn-block login-button" type="submit" value="Comment" />
						</form>
					</div>
				</div>
			</div>
			`);

			$('#create-caption-field').val("");	
			$('#id_image').val("");
			$('.new-comment-form').submit(comment);
			$('.new-like').submit(like);
			$('.new-likers').on('click',likers);
			$('.new-archive_post').submit(archive_post);	
		}

	}).done();
	
}

function search(event){
	event.preventDefault();	
	var url = $(this).attr('action');
	$.ajax({
		url:url,
		data: $(this).serialize(),
		success: function(data){
			var prof_pic;
			if($('#search-field').val() === ""){
				$('#search-results').replaceWith(`<div id="search-results"></div>`);
			}
			
			else if(data['data'][0] === undefined){
				$('#search-results').replaceWith(`
					<div id="search-results">
					<div id="myDropdown" class="dropdown-content show" style="width:300px;"> No results found </div>
					</div>`);	
			}
			else{
				$('#search-results').replaceWith(`
					<div id="search-results">
						<div id="myDropdown" class="dropdown-content show">
							
						</div>
					</div>`);	

				for(var i = 0; i < data['data'].length;i++){
					if(data['data'][i].prof_pic === ""){
						prof_pic = "/static/user_profile/img/blank_picture.png";
					}
					else{
						prof_pic = "/media/"+data['data'][i].prof_pic;
					}
					$('#myDropdown').append(`
						<a href="/profile/`+data['data'][i].user__username+`">
							<img src="`+prof_pic+`" style="border-radius:50%;width:15%;margin-right:10px;">`+data['data'][i].user__username+`
						</a>
						
					`);
						
				}
				
			}
		}
	});
	
}

function follow(event){
	event.preventDefault();
	console.log('clicked');
	var url = $(this).attr('action');
	$.ajax({
		url: url,
		type: 'POST',
		data: $(this).serialize(),
		success: function(data){
			if(data.follow === false){
				$('#follow-btn').replaceWith(`
					<button id='follow-btn' class="btn btn-primary btn-lg btn-block register-button" type="submit" style="width: 100px;margin-left: 45px;">
					Follow
					</button>
				`);
			}
			else{
				$('#follow-btn').replaceWith(`
					<button id='follow-btn' class="btn btn-primary btn-lg btn-block register-button" type="submit" style="width: 100px;margin-left: 45px;">
					Following
					</button>
				`);
			}

			$('#no-followers').replaceWith(`
				<div id='no-followers' class="post" style="text-align: left;font-size: 20px;display: inline; float: left;">
					  Followers `+ data.followers+`&nbsp&nbsp&nbsp&nbsp&nbsp 
				</div>
				`);

		
		}
	});
}

function edit_profile(event){
	event.preventDefault();
	console.log('click');
	var url = $(this).attr('action');
	var data = new FormData(this);
	$.ajax({
		url: url,
		type: 'POST',
		data: data,
		cache: false,
		contentType: false,
		processData: false,
		success: function(data){
			console.log(data);

			if (data.errors){

				$('#edit_prof_notif').replaceWith(`
					<div id="edit_prof_notif"></div>
				`);

				for(var i = 0;i < data.errors.username.length;i++){
					$('#errors').append(`
						<h4>`+ data.errors.username[i]+`</h4> 
					`);	
				}
			}

			else{
				
				$('#display_pic').replaceWith(`
					<img src="`+data.prof_account.prof_pic+`" style="border-radius: 50%; margin-top: 40px; width: 150px;" id='display_pic'>
				`);

				$('#errors').replaceWith(`
					<div id="errors"></div>
				`);

				$('#edit_prof_notif').replaceWith(`
					<div id="edit_prof_notif">
						<h4> Profile edited </h4>				
					</div>
				`);

				$('#id_first_name').replaceWith(`
					<input type="text" name="first_name" value="`+ data.profile.first_name +`" placeholder="Enter your First Name" maxlength="255" class="form-control" required="" id="id_first_name">
				`);
				
				$('#id_last_name').replaceWith(`
					<input type="text" name="last_name" value="`+ data.profile.last_name +`" placeholder="Enter your Last Name" maxlength="255" class="form-control" required="" id="id_last_name">
				`);

				$('#id_username').replaceWith(`
					<input type="text" name="username" value="`+ data.profile.username +`" placeholder="Enter your Username" maxlength="255" class="form-control" required="" id="id_username">
				`);

				$('#id_email').replaceWith(`
					<input type="text" name="email" value="`+ data.profile.email +`" placeholder="Enter your Email Address" class="form-control" required="" id="id_email">
				`);
			}



		}

	});
}


function archive_post(event){
	console.log('click');
	event.preventDefault();
	var url = $(this).attr('action');

	$.ajax({
		url:url,
		type: 'POST',
		data: $(this).serialize(),
		success: function(data){
			$('#post-id-'+data.id).replaceWith(`
				<div id='post-id-{{ feed.id }}'>
				
			`);
		}
	});
}


function delete_restore_archive(event){
	console.log('click')
	event.preventDefault()
	var url = $(this).attr('action')
	$.ajax({
		url:url,
		type: 'POST',
		data: $(this).serialize(),
		success: function(data){
			console.log(data);
			console.log($('#archive-id-'+data.data.id));
			$('#archive-id-'+data.data.id).replaceWith(`<div id='archive-id-`+data.id+`'></div`);
		}	
	});
}

function edit_post(event){
	event.preventDefault();
	console.log('clicked');
	var data = new FormData(this);
	var url = $(this).attr('action');
	$.ajax({
		url:url,
		data:data,
		type: 'POST',
		cache: false,
		contentType: false,
		processData: false,
		success: function(data){
			console.log(data);
			 $('#post-edit-'+data.id).replaceWith(`
				<div class="padding">
						<h4 class="caption" id="feed-caption">
							`+data.caption+`
						</h4>
					</div>
					<div id='center'>
						<a href="#"><img src="`+data.image+`" width="700px" height="500px"></a>
					</div>
			 `);

			 $('#popup2').removeClass('active');
		}
	});
}

function get_post(event){
	event.preventDefault();
	console.log('clicked');
	$('#popup2').addClass('active');
	$('.close2').on('click',function(event){
		$('#popup2').removeClass('active');
	});

	var url = $(this).attr('action');
	$.ajax({
		url:url,
		data: $(this).serialize(),
		success: function(data){
			console.log(data);
			$('#info-feed').replaceWith(`
				<div id="info-feed">
					<div id="left">
						<h4 class="post">`+data.username+`</h4>
						<p align="left" style="margin-left: 45px;">`+data.caption+`</p>
					</div>	<br><br><br><br>
					
					<div id="center">
						<img src="`+data.image+`" width="500px" height="500px" style="margin-top: 10px;">
					</div>
				</div>`);
		}
	});
}

function delete_comment(event){
	event.preventDefault();
	console.log('delete click');
	var url = $(this).attr('action');
	$.ajax({
		url:url,
		data: $(this).serialize(),
		type: 'POST',
		success: function(data){
			$('#comment_id-'+data.id).empty();
		}
	});
}

function comment_active(event){
	event.preventDefault();
	console.log('clicked');
	var url = $(this).attr('action');

	$.ajax({
		url:url,
		data: $(this).serialize(),
		success: function(data){
			console.log(data);
			$('#comment-up-'+data.id).show();

			$('#cancel-edit-comment-'+data.id).on('click',function(){
				console.log('clicked')
				$('#comment-up-'+data.id).hide();
			});
			
		}
	});
}

function edit_comment(event){
	event.preventDefault();
	console.log('edit-comment');
	var url = $(this).attr('action');
	$.ajax({
		url:url,
		data: $(this).serialize(),
		type: 'POST',
		success: function(data){
			console.log(data);
			var buttons = 	``;
			if(data.username === data.current_user){
				buttons = 	`<form action="/feeds/delete_comment/`+data.id+`/" method="post" class="new-delete-comment">
								{% csrf_token %}
								<button style="float: right;" type="submit">x</button>
							</form>
							
							
							
							<form method='get' action="/feeds/get_comment/`+data.id+`/" class="new-comment-form-active">
								{% csrf_token %}
								<button style="float: right;" type="submit">...</button>
							</form>`;
			}

			$('#comment_id-'+data.id).replaceWith(`
				<div id="comment_id-`+data.id+`">
						`+buttons+`
						
							<div class="padding-comments">
								<span class="comment-user" id="comment-user">
									<a href="/profile/`+data.username+`/" style="color: black;float: left;">
										`+data.username+` |
									</a> 
								</span>
								<span class="comment">
									<p>`+data.comment+`<p>
								</span>
								
								<div id='comment-up-`+data.id+`' class="edit-comment-form" style="display: none;">
									<form action="/feeds/edit_comment/`+data.id+`/" method="post" class="new-edit-comment">
										{% csrf_token %}
										{{ comment_form.comment|add_class:'text-box'|attr:"style:width:620px;"|attr:'id:comment-edit'|attr:"placeholder:Edit Comment Here" }}
										
									
									<button style="float: right;" type="submit">Edit</button>
									</form>
									<button style="float: right;" id="cancel-edit-comment-`+data.id+`">Cancel</button>
								</div>
								
								<h4 style="font-size: 12px;">
									Commented on: `+data.commented_at+`
								</h4>
								
							</div>
						</div>
			`);
			$('.new-comment-form-active').submit(comment_active);
			$('.new-delete-comment').submit(delete_comment);
			$('.new-edit-comment').submit(edit_comment);
		}
	}).done();
	
}

$('.edit-comment').submit(edit_comment);
$('.comment-form-active').submit(comment_active);
$('.delete-comment').submit(delete_comment);
$('.edit').submit(get_post);
$('.edit-post').submit(edit_post);
$('.restore_post').submit(delete_restore_archive);
$('.delete_archive').submit(delete_restore_archive);
$('.archive_post').submit(archive_post);
$('.edit_profile').submit(edit_profile);
$('.comment-form').submit(comment);
$('.like').submit(like);
$('.likers').on('click',likers);
$('.create-post').submit(create_post);
$('.search').submit(search);
$('.follow').submit(follow);