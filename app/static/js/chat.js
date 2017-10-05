 $(function() {
 $("#chatheader").click(function(){
	$("#chatContainer").slideToggle();
	$.get( "http://localhost:8080/querychatbot/"+"hi",    //initialize conversation by saying hi
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
	 $.get( "http://localhost:8080/querychatbot/"+message,    //using localhost since app is not yet deployed
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