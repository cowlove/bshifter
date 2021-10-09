//
// This iMacro script interactively takes the BlueCard online 50-hour class
// 
// Run from within the iMacro sidebar
// Requires downgrade to iMacro 8.9.7, as 9.0.3 gives a "s not defined"
// error in iimPlayCode()

// iMacro 8.9.7 won't run on modern firefox >= 60, known to work on 55.0.3
// Older versions than 55 seemed to have intermittent playback hang on chiefs input vids

// Old versions of firefox and imacro:
// https://sourceforge.net/projects/ubuntuzilla/files/mozilla/apt/pool/main/f/firefox-mozilla-build/
// http://download.imacros.net/imacros_for_firefox-8.9.7-fx.xpi



while(1) { 
	// 1) Pick first 3 answers for any "pick three" question on the page, if present
	playCode("TAG POS=1 TYPE=SCRIPT ATTR=TYPE:text/javascript EXTRACT=HTM");
	js = iimGetLastExtract();


	// 2) Pick the answer for any multiple choice question on the page, if present
	re = new RegExp('"Name":"1[.] .*"Name":"([^"]*)"');
	res = re.exec(js);
	if (res != null && res.length > 1) { 
		//alert(res[1]);
	}

	
	pickThree = false		
	for(a = 1; a < 10; a++) { 
		//re = new RegExp('"studentAnswer' + a + '","answerOption":"[^"]*","isCorrect":true')
		//if (js.search(re) > 0) {
		//	playCode("TAG POS=1 TYPE=INPUT:CHECKBOX ATTR=ID:studentAnswer" + a + " CONTENT=YES");
		//	pickThree = true;
		//}
		re = new RegExp('"studentAnswer' + a + '"[^}]*"isCorrect":true')
		if (js.search(re) > 0) {
			playCode("TAG POS=1 TYPE=INPUT:CHECKBOX ATTR=ID:studentAnswer" + a + " CONTENT=YES");
			pickThree = true;
		}
	}
	if (pickThree) {
		playCode("TAG POS=1 TYPE=BUTTON ATTR=ID:SaSubmitBtn");
	}

	// 2) Pick the answer for any multiple choice question on the page, if present
	re = new RegExp('"Name":"([A-Z])"');
	res = re.exec(js);
	if (res != null && res.length > 1) { 
		a = res[1].charCodeAt(0) - 64;
		//alert(a);
		playCode("TAG POS=" + a + " TYPE=SPAN ATTR=CLASS:fv-answerOptionText");
	}


	playCode("TAG POS=1 TYPE=LABEL ATTR=ID:rfc-ansOption");
	if (playCode("POS=1 TYPE=INPUT:CHECKBOX ATTR=ID:studentAnswer1 CONTENT=YES") >= 0) { 
		playCode("TAG POS=1 TYPE=BUTTON ATTR=ID:SaSubmitBtn");
	}
	

	if (playCode("TAG POS=1 TYPE=SELECT ATTR=ID:studentAnswer1 CONTENT=%2") >= 0 ||
		playCode("TAG POS=1 TYPE=SELECT ATTR=ID:studentAnswer2 CONTENT=%2") >= 0 ||
		playCode("TAG POS=1 TYPE=SELECT ATTR=ID:studentAnswer3 CONTENT=%2") >= 0) {
		for(n = 2; n < 25; n++) {
			playCode("TAG POS=1 TYPE=SELECT ATTR=ID:studentAnswer" + n + " CONTENT=%1");
		}
		playCode("TAG POS=1 TYPE=SELECT ATTR=ID:studentAnswer3 CONTENT=%4");
		playCode("TAG POS=1 TYPE=SELECT ATTR=ID:studentAnswer4 CONTENT=%4");
		playCode("TAG POS=1 TYPE=SELECT ATTR=ID:studentAnswer6 CONTENT=%4");
		playCode("TAG POS=1 TYPE=SELECT ATTR=ID:studentAnswer7 CONTENT=%2");
		playCode("TAG POS=1 TYPE=SELECT ATTR=ID:studentAnswer8 CONTENT=%1");
		playCode("TAG POS=1 TYPE=SELECT ATTR=ID:studentAnswer10 CONTENT=%3");
		playCode("TAG POS=1 TYPE=SELECT ATTR=ID:studentAnswer11 CONTENT=%4");
		playCode("TAG POS=1 TYPE=SELECT ATTR=ID:studentAnswer14 CONTENT=%2");
		playCode("TAG POS=1 TYPE=SELECT ATTR=ID:studentAnswer15 CONTENT=%2");
		playCode("TAG POS=1 TYPE=SELECT ATTR=ID:studentAnswer16 CONTENT=%3");
		playCode("TAG POS=1 TYPE=SELECT ATTR=ID:studentAnswer19 CONTENT=%1");
		playCode("TAG POS=1 TYPE=SELECT ATTR=ID:studentAnswer20 CONTENT=%1");
		playCode("TAG POS=1 TYPE=SELECT ATTR=ID:studentAnswer21 CONTENT=%3");
		playCode("TAG POS=1 TYPE=INPUT:BUTTON ATTR=ID:MfSubmitBtn");
	}

	// 3) Click on and wait for required videos on this page
	watchVideo("radiobtnIncomplete");
	watchVideo("chiefBtnIncomplete");

	// 4) Wait for the NEXT button to enable, then click it 
	i = 1;
	while(i > 0) { 
		i = playCode("TAG POS=1 TYPE=LI ATTR=ID:NextLinkNavItem EXTRACT=HTM")
		s = iimGetLastExtract();
		//alert(s)
		if (s.search("class=\"disabled\"") < 0) { 
			break;
		} 
		delay(15);
	}
	playCode("SET !TIMEOUT_PAGE 300\nTAG POS=1 TYPE=SPAN ATTR=TXT:Next");
	delay(1);
}



function watchVideo(n) { 
	var i = playCode("TAG POS=1 TYPE=DIV ATTR=ID:" + n );
	while (i > 0) {
		delay(10);
		i = playCode("TAG POS=1 TYPE=DIV ATTR=ID:" + n + " EXTRACT=HTM")
		if (i < 0) {
			break;
		}
		var s = iimGetLastExtract();
		//alert(s);
		if (s.search("display: block") < 0) { 
			break;
		}
	} 
}

function playCode(st) { 
	return iimPlayCode("SET !TIMEOUT_STEP 1\n" + st);
}

function delay(st) { 
	playCode("WAIT SECONDS=" + st);
}
		
