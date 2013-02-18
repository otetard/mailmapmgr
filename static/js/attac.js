$(function() {
    $("fieldset#block_search").hide();
});

// @TODO: améliorer cette merde. Le texte initial doit apparaitre lors
// du lancement, être vidé lorsque l'utilisateur clique dedans, et
// remis si rien n'a été renseigné.
// $(function() {
//     $("fieldset.add_new_alias textarea").click(
// 	function() {
// 	    text = $(this).text();
// 	    if(text == "") {
// 		$(this).text("Une entrée par ligne"); 
// 	    }
// 	    else if(text == "Une entrée par ligne") {
// 		$(this).text("");
// 	    }
// 	}
//     );
// });