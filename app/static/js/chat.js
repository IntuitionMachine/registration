 $(function() {
 $("#chatheader").click(function(){
	$("#chatContainer").slideToggle();
	$.get("http://chat.intuitionfabric/querychatbot/"+"hi",		
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
        $.get("http://chat.intuitionfabric.com/querychatbot/" + message,
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
