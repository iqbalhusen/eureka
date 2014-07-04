$(document).ready(function()
{
	//For Like and unlike category
	$('#likes').click(function()
	{
		var catid, userid;
		catid = $(this).attr("data-catid");
		userid = $(this).attr("data-userid");
		$.get('/eureka/like_category/', {category_id: catid, user_id: userid}, function(data)
		{
			$('#like_count_cat').html(data);
			$('#likes').hide();
			$('#just_liked').show();
		});
	});
	
	$('#unlike').click(function()
			{
				var catid, userid;
				catid = $(this).attr("data-catid");
				userid = $(this).attr("data-userid");
				$.get('/eureka/unlike_category/', {category_id: catid, user_id: userid}, function(data)
				{
					$('#like_count').html(data);
					$('#you_unliked').hide();
					$('#just_unliked').show();
				});
			});
			
	//To like or unlike an article
	$('#like_article').click(function()
	{
		var articleid, userid;
		articleid = $(this).attr("data-articleid");
		userid = $(this).attr("data-userid");
		$.get('/eureka/like_article/', {article_id: articleid, user_id: userid}, function(data)
		{
			$('#like_count').html(data);
			$('#like_article').hide();
			$('#just_liked_article').show();
		});
	});
	
	$('#unlike_article').click(function()
	{
		var articleid, userid;
		articleid = $(this).attr("data-articleid");
		userid = $(this).attr("data-userid");
		$.get('/eureka/unlike_article/', {article_id: articleid, user_id: userid}, function(data)
		{
			$('#like_count').html(data);
			$('#unliked_article').hide();
			$('#just_unliked_article').show();
		});
	});
	
	//Restrict search article form
	$("#search_article_form").bind("submit", function()
	{
		var query = $('#search_key').val();
		if (query == '')
			return false;
		
	});
	
	//Restricting advanced search form value
	$("#adv_search_form").bind("submit", function()
	{
		var query = $('#adv_search_key').val();
		var cat = $('#cat').val();
		if (query == '')
			return false;
		else if (cat == '')
			return false;
	});
	
	
	// restricting manuscript submit
	$("#article_form").bind("submit", function()
	{
		var ext = $('#id_pdf').val().split('.').pop().toLowerCase();
		if (ext != 'pdf') 
		{
			$("#file_error").html("<small>Unsupported file format!</small>");
		    return false;
		}
		
		else
		{
			var filesize = $("#id_pdf")[0].files[0].size;
			if (filesize > 10485760)
			{
				$("#file_error").html("<small>File size exceeds 10 MiB!</small>");
			    return false;
			}
		}
	});
	
	//Article Tabs
	$('.tabs .tab-links a').on('click', function(e)  
	{
		var currentAttrValue = $(this).attr('href');
	 
	        // Show/Hide Tabs
	        $('.tabs ' + currentAttrValue).show().siblings().hide();
	 
	        // Change/remove current tab to active
	        $(this).parent('li').addClass('active').siblings().removeClass('active');
	 
	        e.preventDefault();
	});
	
	
});


//Registration Page
function myFunction()
{
	if ($("#exact_prof").text() == "What is your profession?")
	{
		$("#ins_prof").show();
		
		$("#ins_stud-alum_ugpg").hide();
		$("#ins_stud-alum-lec_depts").hide();
		$("#ins_stud-lec-lib-as-ms_id").hide();
		$("#ins_alum_year").hide();
		$("#out-ins_alum-lib-as-ms-others_exact_prof").hide();
		$("#ins_alum-out_place").hide();
		
		$("#exact_prof").text("Mention exact designation");
	}
	
	else
	{
		$("#out-ins_alum-lib-as-ms-others_exact_prof").show();
		$("#ins_alum-out_place").show();
		
		$("#ins_prof").hide();
		$("#ins_stud-lec-lib-as-ms_id").hide();
		$("#ins_stud-alum-lec_depts").hide();
		$("#ins_stud-alum_ugpg").hide();
		$("#ins_alum_year").hide();
		
		$("#exact_prof").text("What is your profession?");
	}
}


function myFunction1()
{
	var a = $("#id_profession").val();
	
	if (a == '')
	{
		$("#ins_stud-alum_ugpg").hide();
		$("#ins_stud-alum-lec_depts").hide();	
		$("#ins_stud-lec-lib-as-ms_id").hide();
		$("#ins_alum_year").hide();
		$("#out-ins_alum-lib-as-ms-others_exact_prof").hide();
		$("#ins_alum-out_place").hide();
	}	
	
	else if (a == 'ST')
	{
		$("#ins_stud-lec-lib-as-ms_id").show();
		$("#ins_stud-alum_ugpg").show();
		$("#ins_stud-alum-lec_depts").show();
		
		$("#ins_alum_year").hide();
		$("#out-ins_alum-lib-as-ms-others_exact_prof").hide();
		$("#ins_alum-out_place").hide();
		
		$("#idnum").text("Enter your roll number");
	}	
		
	else if (a == 'AL')
	{
		$("#ins_stud-alum_ugpg").show();
		$("#ins_stud-alum-lec_depts").show();
		$("#ins_alum_year").show();
		$("#out-ins_alum-lib-as-ms-others_exact_prof").show();
		$("#ins_alum-out_place").show();
		
		$("#ins_stud-lec-lib-as-ms_id").hide();
		
		$("#exact_prof").text("What do you do now?");
	}
	
	else if (a == 'LC')
	{
	
		$("#ins_stud-lec-lib-as-ms_id").show();
		$("#ins_stud-alum-lec_depts").show();
		
		$("#ins_stud-alum_ugpg").hide();
		$("#ins_alum_year").hide();
		$("#out-ins_alum-lib-as-ms-others_exact_prof").hide();
		$("#ins_alum-out_place").hide();
		
		$("#idnum").text("Enter your ID number");
	}
	
	else if (a == 'LS' || a == 'AS')
	{
		$("#ins_stud-lec-lib-as-ms_id").show();
		$("#out-ins_alum-lib-as-ms-others_exact_prof").show();
		
		$("#ins_stud-alum-lec_depts").hide();
		$("#ins_stud-alum_ugpg").hide();
		$("#ins_alum_year").hide();
		$("#ins_alum-out_place").hide();
		
		$("#idnum").text("Enter your ID number");
		$("#exact_prof").text("Mention exact designation");
	}
	
	else if (a == 'MS' || a == 'OT')
	{
		$("#out-ins_alum-lib-as-ms-others_exact_prof").show();
		
		$("#ins_stud-lec-lib-as-ms_id").hide();
		$("#ins_stud-alum-lec_depts").hide();
		$("#ins_stud-alum_ugpg").hide();
		$("#ins_alum_year").hide();
		$("#ins_alum-out_place").hide();
		
		$("#exact_prof").text("Mention exact designation");
	}	
}