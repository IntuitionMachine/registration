 $(function() {
 $("#chatheader").click(function(){
	$("#chatContainer").slideToggle();
	//$.get("http://chat.intuitionfabric/querychatbot/"+"hi",		
    //  $.get("http://128.199.246.202:5000/queryrasabot/"+"hi",
	//$.get("https://chat-intuitionfabric.herokuapp.com/querychatbot/"+"hi",
	//$.get("https://chat-intuitionfabric.herokuapp.com/queryrasabot/"+"hi",
	$.get("http://127.0.0.1/queryrasabot"+"hi",
	function(data) {
		var botdiv = document.createElement('div')
		botdiv.setAttribute('class', 'chat bot');
		botdiv.innerHTML = '<div class='+'bot-photo'+'></div>' +'<p class='+ 'chat-message'+'>'+data+'</p>';
	   $("#chatlogs").append(botdiv);
	   console.log(botdiv);
	}
	);
});

$("#send").click(function(){
   message= $('#message').val();
   var div = document.createElement('div')
   div.setAttribute('class', 'chat self');
   div.innerHTML = '<div class='+'user-photo'+'></div>' +'<p class='+ 'chat-message'+'>'+ message+'</p>';
   $("#chatlogs").append(div);
        //$.get("http://chat.intuitionfabric.com/querychatbot/" + message,
	//$.get("http://128.199.246.202:5000/queryrasabot/"+message,
	$.get("http://127.0.0.1/queryrasabot"+message,
	//$.get("https://chat-intuitionfabric.herokuapp.com/querychatbot/" + message,
	//$.get("https://chat-intuitionfabric.herokuapp.com/queryrasabot"+message,
	function(data) {
		var botdiv = document.createElement('div')
		botdiv.setAttribute('class', 'chat bot');
		botdiv.innerHTML = '<div class='+'bot-photo'+'></div>' +'<p class='+ 'chat-message'+'>'+data+'</p>';
	   $("#chatlogs").append(botdiv);
	   console.log(botdiv);
	}
 );

});
});

//MyFiddle https://jsfiddle.net/sqd2e8y2/13/ for checking and editing
