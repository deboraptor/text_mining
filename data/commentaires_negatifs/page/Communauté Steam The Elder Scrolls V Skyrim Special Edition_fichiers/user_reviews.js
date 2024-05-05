
function UserReview_Award( bLoggedIn, loginURL, recommendationID, callbackFunc, selectedAward )
{
	if ( bLoggedIn )
	{
		fnLoyalty_ShowAwardModal( recommendationID, 1, callbackFunc, undefined, selectedAward );
	}
	else
	{
		var dialog = ShowConfirmDialog( 'Erreur', 'Vous devez être connecté(e) pour effectuer cette action.', 'Connexion' );
		dialog.done( function() {
			top.location.href = loginURL;
		} );
	}
}

function UserReview_ShowMoreAwards( elem )
{
	elem = $J( elem );
	var container = elem.closest( ".review_award_ctn" );
	container.addClass( "show_all_awards" );
}

function UserReview_Rate( recommendationID, bRateUp, baseURL, callback )
{
	$J.post( baseURL + '/userreviews/rate/' + recommendationID,{
				'rateup' : bRateUp,
				'sessionid' : g_sessionID
	}).done( function( results ) {
		if ( results.success == 1 )
		{
			callback( results );
		}
		else if ( results.success == 21 )
		{
			ShowAlertDialog( 'Erreur', 'Vous devez être connecté(e) pour effectuer cette action.' );
		}
		else if ( results.success == 15 )
		{
			ShowAlertDialog( 'Erreur', 'Votre compte ne possède pas les privilèges nécessaires pour effectuer cette action.' );
		}
		else if ( results.success == 24 )
		{
			ShowAlertDialog( 'Erreur', 'Votre compte ne répond pas aux exigences pour utiliser cette fonctionnalité. <a class="whiteLink" href="https://help.steampowered.com/fr/wizard/HelpWithLimitedAccount" target="_blank" rel="noreferrer">Visitez le site du Support Steam</a> pour plus d\'informations.' );
		}
		else
		{
			ShowAlertDialog( 'Erreur', 'Une erreur est survenue lors du traitement de votre demande :' + results.success );
		}
	} );
}

function UserReview_VoteTag( recommendationID, tagID, bRateUp, baseURL, callback )
{
	$J.post( baseURL + '/userreviews/votetag/' + recommendationID,{
		'tagid' : tagID,
		'rateup' : bRateUp,
		'sessionid' : g_sessionID
	}).done( function( results ) {
		if ( results.success == 1 )
		{
			callback( results );
		}
		else if ( results.success == 21 )
		{
			ShowAlertDialog( 'Erreur', 'Vous devez être connecté(e) pour effectuer cette action.' );
		}
		else if ( results.success == 15 )
		{
			ShowAlertDialog( 'Erreur', 'Votre compte ne possède pas les privilèges nécessaires pour effectuer cette action.' );
		}
		else if ( results.success == 24 )
		{
			ShowAlertDialog( 'Erreur', 'Votre compte ne répond pas aux exigences pour utiliser cette fonctionnalité. <a class="whiteLink" href="https://help.steampowered.com/fr/wizard/HelpWithLimitedAccount" target="_blank" rel="noreferrer">Visitez le site du Support Steam</a> pour plus d\'informations.' );
		}
		else
		{
			ShowAlertDialog( 'Erreur', 'Une erreur est survenue lors du traitement de votre demande :' + results.success );
		}
	} );
}

function UserReview_Report( recommendationID, baseURL, callback )
{
	var dialog = ShowPromptWithTextAreaDialog( 'Signaler une évaluation', '', null, null, 1000 );
	var explanation = $J('<div/>', { 'class': 'user_review_report_dialog_explanation' } );
	explanation.html( 'Veuillez indiquer la raison pour laquelle vous signalez cette évaluation pour violation de l\'Accord de souscription Steam et des Règles de conduite en ligne Steam. Cette action est irréversible.' );

	var textArea = dialog.m_$Content.find( 'textarea' );
	textArea.addClass( "user_review_report_dialog_text_area" );
	textArea.parent().before( explanation );

	dialog.done( function( note ) {
		if ( !note )
		{
			return;
		}
		note = v_trim( note );
		if ( note.length < 1 )
		{
			return;
		}
		$J.post( baseURL + '/userreviews/report/' + recommendationID, {
					'reportnote' : note,
					'sessionid' : g_sessionID
		}).done( function( results ) {
			if ( results.success == 1 )
			{
				callback( results );
			}
			else if ( results.success == 21 )
			{
				ShowAlertDialog( 'Erreur', '##UserReviews_Error_NotLoggedIn_Text' );
			}
			else
			{
				ShowAlertDialog( 'Erreur', 'Une erreur est survenue lors du traitement de votre demande :' + results.success );
			}
		} );
	} );
}

function UserReview_ShowUpdateReviewDialog( recommendationID, existingText, baseURL )
{
	var dialog = ShowPromptWithTextAreaDialog( 'Mettre à jour l\'évaluation', existingText, null, null, 4096 );

	dialog.done( function( note ) {
		if ( !note )
		{
			return;
		}
		note = v_trim( note );
		if ( note.length < 1 )
		{
			return;
		}
		UserReview_Update_Text( recommendationID, note, baseURL, function( results ) { top.location.reload(); } );
	} );
}

function UserReview_Update( recommendationID, params, baseURL, callback )
{
	params['sessionid'] = g_sessionID;
	$J.post( baseURL + '/userreviews/update/' + recommendationID, params )
	.done( function( results ) {
		if ( results.success == 1 )
		{
			if ( callback )
			{
				callback( results );
			}
		}
		else
		{
			ShowAlertDialog( 'Erreur', 'Une erreur est survenue lors du traitement de votre demande :' + results.success );
		}
	} );
}

function UserReview_Update_Visibility( recommendationID, is_public, baseURL, callback )
{
	UserReview_Update( recommendationID, { 'is_public' : is_public }, baseURL, callback );
}

function UserReview_Update_Language( recommendationID, language, baseURL, callback )
{
	UserReview_Update( recommendationID, { 'language' : language }, baseURL, callback );
}

function UserReview_Update_CommentStatus( recommendationID, bCommentsDisabled, baseURL, callback )
{
	UserReview_Update( recommendationID, { 'comments_disabled' : bCommentsDisabled }, baseURL, callback );
}

function UserReview_Moderate( recommendationID, params, baseURL, callback )
{
	params['sessionid'] = g_sessionID;
	$J.post( baseURL + '/userreviews/moderate/' + recommendationID, params )
		.done( function( results ) {
			if ( results.success != 1 )
			{
				var dialog = ShowAlertDialog( 'Erreur', 'Une erreur est survenue lors du traitement de votre demande :' + results.success );
				dialog.done( function() {
					if ( callback )
					{
						callback( results );
					}
				} );
			}
			else
			{
				if ( callback )
				{
					callback( results );
				}
			}
		} );
}

function UserReview_ClearDeveloperFlag( recommendationID, baseURL, callback )
{
	var dialog = ShowConfirmDialog( 'Effacer la raison du signalement de l\'équipe de développement', 'Cette évaluation a été signalée par l\'équipe de développement. Voulez-vous vraiment effacer ce statut ?' );
	dialog.done( function() {
		$J.post( baseURL + '/userreviews/cleardeveloperflag/' + recommendationID, {'sessionid' : g_sessionID} )
		.done( function( results ) {
			if ( results.success == 1 )
			{
				if ( callback )
				{
					callback( results );
				}
			}
			else
			{
				ShowAlertDialog( 'Erreur', 'Une erreur est survenue lors du traitement de votre demande :' + results.success );
			}
		} );
	});
}

function UserReview_SetDeveloperResponse( recommendationID, recommendation, baseURL, callback )
{
	var dialog = ShowPromptWithTextAreaDialog( 'Rédiger une réponse', recommendation.developer_response, null, null, 8000 );
	var explanation = $J('<div/>', { 'class': 'user_review_report_dialog_explanation' } );
	explanation.html( 'Vous pouvez choisir de répondre à cette évaluation à titre officiel. Cette réponse sera visible par toute personne pouvant voir cette évaluation et sera marquée comme venant de l\'équipe de développement.' );

	var textArea = dialog.m_$Content.find( 'textarea' );
	textArea.addClass( "user_review_report_dialog_text_area" );
	textArea.parent().before( explanation );

	dialog.done( function( note ) {
		$J.post( baseURL + '/userreviews/setdeveloperresponse/' + recommendationID,{
					'developer_response' : note,
					'sessionid' : g_sessionID
		}).done( function( results ) {
			if ( results.success == 1 )
			{
				callback( results );
			}
			else
			{
				ShowAlertDialog( 'Erreur', 'Une erreur est survenue lors du traitement de votre demande :' + results.success );
			}
		} );
	} );
}

function UserReview_ShowReportsDialog( recommendationID, baseURL )
{
	$J.post( baseURL + '/userreviews/ajaxgetreports/' + recommendationID,{ 'sessionid' : g_sessionID } )
	.done( function( results ) {
		if ( results.success == 1 )
		{
			var container = $J('<div/>', {'class': 'review_reports' } );
			var reports = results.reports;

			{
				var reportDiv = $J('<div/>', {'class': 'review_report header' } );
				var divReporter = $J('<div/>', {'class': 'review_report_data' } ).append( 'Reporter' );
				reportDiv.append( divReporter );
				var divDescription = $J('<div/>', {'class': 'review_report_data description' } ).append( 'Report Description' );
				reportDiv.append( divDescription );
				var divWeight = $J('<div/>', {'class': 'review_report_data' } ).append( 'Weight' );
				reportDiv.append( divWeight );
				var divWasReset = $J('<div/>', {'class': 'review_report_data' } ).append( 'Cleared?' );
				reportDiv.append( divWasReset );
				var divTime = $J('<div/>', {'class': 'review_report_data' } ).append( 'Date' );
				reportDiv.append( divTime );
				var divReviewText = $J('<div/>', {'class': 'review_report_data review_text' } ).append( 'Review Text At Report Time' );
				reportDiv.append( divReviewText );
				var divClear = $J('<div/>', {'style': 'clear: left' } );
				reportDiv.append( divClear );
				container.append( reportDiv );
			}

			for ( var i = 0; i < reports.length; ++i )
			{
				var report = reports[i];

				var reportDiv = $J('<div/>', {'class': 'review_report' } );
					var divReporter = $J('<div/>', {'class': 'review_report_data' } ).append( $J('<a/>', {'href': report.reporter_url, 'text': report.reporter, 'target': '_blank' } ) );
					reportDiv.append( divReporter );
					var divDescription = $J('<div/>', {'class': 'review_report_data description' } ).append( report.description );
					reportDiv.append( divDescription );
					var divWeight = $J('<div/>', {'class': 'review_report_data' } ).append( report.weight );
					reportDiv.append( divWeight );
					var divWasReset = $J('<div/>', {'class': 'review_report_data' } ).append( report.was_reset ? 'Yes' : 'No' );
					reportDiv.append( divWasReset );
					var divTime = $J('<div/>', {'class': 'review_report_data' } ).append( report.time_string );
					reportDiv.append( divTime );
					var divReviewText = $J('<div/>', {'class': 'review_report_data review_text' } ).append( report.review_text );
					reportDiv.append( divReviewText );
					var divClear = $J('<div/>', {'style': 'clear: left' } );
					reportDiv.append( divClear );
				container.append( reportDiv );
			}
			var dialog = ShowAlertDialog( 'Effacer les signalements', container );
		}
	} );
}

function UserReview_ShowContentCheckResultsDialog( recommendationID, baseURL )
{
	$J.get( baseURL + '/userreviews/ajaxgetcontentcheckresults/' + recommendationID )
	.done( function( data ) {
		if ( data.success == 1 )
		{
			var container = $J('<div/>', {'class': 'review_reports' } );

			{
				var reportDiv = $J('<div/>', {'class': 'review_report header' } );
					var divProvider = $J('<div/>', {'class': 'review_report_data' } ).append( 'Provider' );
					reportDiv.append( divProvider );
					var divResult = $J('<div/>', {'class': 'review_report_data' } ).append( 'Result' );
					reportDiv.append( divResult );
					var divScore = $J('<div/>', {'class': 'review_report_data' } ).append( 'Score' );
					reportDiv.append( divScore );
					var divProviderResponse = $J('<div/>', {'class': 'review_report_data description' } ).append( 'Provider Response' );
					reportDiv.append( divProviderResponse );
					var divReviewText = $J('<div/>', {'class': 'review_report_data review_text' } ).append( 'Review Text At Eval Time' );
					reportDiv.append( divReviewText );
					var divTime = $J('<div/>', {'class': 'review_report_data' } ).append( 'Date' );
					reportDiv.append( divTime );
					var divClear = $J('<div/>', {'style': 'clear: left' } );
					reportDiv.append( divClear );
				container.append( reportDiv );
			}

			for ( var i = 0; i < data.results.length; ++i )
			{
				var r = data.results[i];
				var reportDiv = $J('<div/>', {'class': 'review_report' } );
					var divProvider = $J('<div/>', {'class': 'review_report_data' } ).append( r.provider == 1 || r.provider == 4 ? 'Google' : 'Unknown' );
					reportDiv.append( divProvider );
					var divResult = $J('<div/>', {'class': 'review_report_data' } ).append( r.ban_check_result_string );
					reportDiv.append( divResult );
					var divScore = $J('<div/>', {'class': 'review_report_data' } ).append( r.score );
					reportDiv.append( divScore );
					var divProviderResponse = $J('<div/>', {'class': 'review_report_data description' } ).append( r.provider_response );
					reportDiv.append( divProviderResponse );
					var divReviewText = $J('<div/>', {'class': 'review_report_data review_text' } ).append( r.review_text );
					reportDiv.append( divReviewText );
			var divTime = $J('<div/>', {'class': 'review_report_data' } ).append( r.timestamp_evaluated_string );
			reportDiv.append( divTime );
					var divClear = $J('<div/>', {'style': 'clear: left' } );
					reportDiv.append( divClear );
				container.append( reportDiv );
			}
			var dialog = ShowAlertDialog( 'Résultats de la vérification du contenu suspect', container );
		}
	} );
}

function UserReview_ShowClearReportsDialog( recommendationID, baseURL, callback )
{
	var dialog = ShowConfirmDialog( 'Effacer les signalements', 'Voulez-vous vraiment supprimer tous les signalements ? Cette action est irréversible !' );
	dialog.done( function() {
		UserReview_Moderate( recommendationID, { 'clear_reports' : 1 }, baseURL, callback);
	});
}

function UserReview_ShowVoteBanUsersDialog( recommendationID, baseURL, callback )
{
	var dialog = ShowConfirmDialog( 'Interdire à des comptes de voter pour du contenu', 'Voulez-vous vraiment interdire aux comptes qui ont réagi positivement à cette évaluation de voter pour du contenu ? Cette action est irréversible !<br><br>N\'utilisez cette option que si cette évaluation contient bien du contenu suspect.' );
	dialog.done( function() {
		UserReview_Moderate_VoteBanUsers( recommendationID, baseURL, callback);
	});
}

function UserReview_Moderate_SetBanStatus( recommendationID, force_hidden, baseURL, callback, strModerationNote )
{
	UserReview_Moderate( recommendationID, { 'force_hidden' : force_hidden, 'moderation_note' : strModerationNote }, baseURL, callback );
}

function UserReview_Moderate_SetDeveloperFlag( recommendationID, flagged_by_developer, baseURL, callback )
{
	UserReview_Moderate( recommendationID, { 'flagged_by_developer' : flagged_by_developer }, baseURL, callback );
}

function UserReview_Moderate_SetQualities( recommendationID, qualities, baseURL, callback )
{
	UserReview_Moderate( recommendationID, { 'review_qualities' : qualities, 'update_review_qualities' : 1 }, baseURL, callback );
}

function UserReview_Moderate_VoteBanUsers( recommendationID, baseURL, callback )
{
	UserReview_Moderate( recommendationID, { 'vote_ban_users' : 1 }, baseURL, callback );
}
