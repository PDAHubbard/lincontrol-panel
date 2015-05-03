#!/bin/bash
#
# 01/05/15: Authored by Peter Hubbard - peterhjr@gmail.com
#
# Changelog: 
# 00001 - remove default choice from radio buttons to prevent automatic submission.
# 00002 - Move live log viewer into main page and create divs for 2 sections
#
#####################################################################################
#
#
###############
#CONFIGURATION#
###############
# Enter the full path to the configuration file to edit here
# The file must be writable by the www-data user/group
CONFIG_FILE=/home/fargo/dev/scripts/lincontrol/file.conf

# Enter the name of the service to be controlled by the panel
# 
SERVICE_NAME=atd

#####################################################################################
#
#
################
# HTML HEADERS #
################
echo "Content-type: text/html"
# Blank line required between content type and html
# We use an empty echo as bash does not recognise \n as a newline.
echo

echo "<html>"
echo "<head><title>Linux Control Panel</title>"

echo "<script type=text/javascript src=/ajax-logtail.js> </script>"
echo "</head>"
echo "<body>"


#####################################################################################
#
#
#############
# FUNCTIONS #
#############
# This code for getting code from post data is from http://oinkzwurgl.org/bash_cgi and 
# was written by Phillippe Kehi <phkehi@gmx.net> and flipflip industries
# (internal) routine to store POST data
function cgi_get_POST_vars()
{
	# check content type
	# FIXME: not sure if we could handle uploads with this..
	# FIXME: Removed this warning as it was still happening even with the content type set.
#	[ "${CONTENT_TYPE}" != "application/x-www-form-urlencoded" ] && \
#		echo "bash.cgi warning: you should probably use MIME type "\
#		"application/x-www-form-urlencoded!" 1>&2
	# save POST variables (only first time this is called)
	[ -z "$QUERY_STRING_POST" \
		-a "$REQUEST_METHOD" = "POST" -a ! -z "$CONTENT_LENGTH" ] && \
		read -n $CONTENT_LENGTH QUERY_STRING_POST
	# prevent shell execution
	local t
	t=${QUERY_STRING_POST//%60//} # %60 = `
	t=${t//\`//}
	t=${t//\$(//}
	t=${t//%24%28//} # %24 = $, %28 = (
	QUERY_STRING_POST=${t}
	return
}

# (internal) routine to decode urlencoded strings
function cgi_decodevar()
{
	[ $# -ne 1 ] && return
	local v t h
	# replace all + with whitespace and append %%
	t="${1//+/ }%%"
	while [ ${#t} -gt 0 -a "${t}" != "%" ]; do
		v="${v}${t%%\%*}" # digest up to the first %
		t="${t#*%}"       # remove digested part
		# decode if there is anything to decode and if not at end of string
		if [ ${#t} -gt 0 -a "${t}" != "%" ]; then
			h=${t:0:2} # save first two chars
			t="${t:2}" # remove these
			v="${v}"`echo -e \\\\x${h}` # convert hex to special char
		fi
	done
	# return decoded string
	echo "${v}"
	return
}

# routine to get variables from http requests
# usage: cgi_getvars method varname1 [.. varnameN]
# method is either GET or POST or BOTH
# the magic varible name ALL gets everything
function cgi_getvars()
{
	[ $# -lt 2 ] && return
	local q p k v s
	# prevent shell execution
	t=${QUERY_STRING//%60//} # %60 = `
	t=${t//\`//}
	t=${t//\$(//}
	t=${t//%24%28//} # %24 = $, %28 = (
	QUERY_STRING=${t}
	# get query
	case $1 in
		GET)
			[ ! -z "${QUERY_STRING}" ] && q="${QUERY_STRING}&"
			;;
		POST)
			cgi_get_POST_vars
			[ ! -z "${QUERY_STRING_POST}" ] && q="${QUERY_STRING_POST}&"
			;;
		BOTH)
			[ ! -z "${QUERY_STRING}" ] && q="${QUERY_STRING}&"
			cgi_get_POST_vars
			[ ! -z "${QUERY_STRING_POST}" ] && q="${q}${QUERY_STRING_POST}&"
			;;
	esac
	shift
	s=" $* "
	# parse the query data
	while [ ! -z "$q" ]; do
		p="${q%%&*}"  # get first part of query string
		k="${p%%=*}"  # get the key (variable name) from it
		v="${p#*=}"   # get the value from it
		q="${q#$p&*}" # strip first part from query string
		# decode and evaluate var if requested
		[ "$1" = "ALL" -o "${s/ $k /}" != "$s" ] && \
			eval "$k=\"`cgi_decodevar \"$v\"`\""
	done
	return
}



# register all GET and POST variables
cgi_getvars BOTH ALL

#####################################################################################
#
#
########################
# STATUS messages here #
########################

# test for POSTDATA - if present then write changes to the file
if [[ $configdata ]]
then
	#Strip the ^M (return) character
	echo $configdata | sed -e "s/\r/\n/g" > $CONFIG_FILE 
	echo "<font color=red>File $CONFIG_FILE saved.</font><br>"
fi
# POSTDATA


# test if any parameters were passed
if [ $CMD ]
then
	case "$CMD" in
		startservice)
			echo "Starting $SERVICE_NAME :<pre>"
# Add command to START the service
			echo "</pre>"
			;;

		stopservice)
			echo "Stopping $SERVICE_NAME :<pre>"
# Add command to STOP the service
			echo "</pre>"
			;;
		
		restartservice)
			echo "Restarting $SERVICE_NAME :<pre>"
# Add command top RESTART the service
			echo "</pre>"
			;;

		*)
			echo "Unknown command $CMD<br>"
			;;
	esac
fi

# print out the form

# page header
cat <<EOF
<p>
<center>
<h2>Linux Control Panel</h2>
</center>
<p>
<p>
        <div id="controls" style="border:solid 1px #dddddd; width:500px; margin-left:25px; font-size:14px; font-family:san-serif,tahoma,arial;
	        padding-left:15px; padding-right:15px; padding-top:10px; padding-bottom:20px;
		        margin-top:20px; margin-bottom:10px; text-align:left;">

Current contents of $CONFIG_FILE
<form name=configform method=post enctype=application/x-www-form-urlencoded>

<textarea name=configdata rows=4 cols=50>
EOF

cat $CONFIG_FILE

cat <<EOF
</textarea><br>
<button type=submit>Save Changes</button><br>
</form>

<form method=post>
<input type=radio name=CMD value=startservice>START Service  <br>
<input type=radio name=CMD value=stopservice>STOP Service<br>
<input type=radio name=CMD value=restartservice>RESTART Service<br>
<input type=submit>
</form>
</div>

<div id="logcontrols" style="width:490px; margin-left:575px; margin-top:-300px; height:30px; overflow:auto;">
                <button onclick="getLog('start');">Start Viewer</button>
                <button onclick="stopTail();">Stop Viewer</button>
        </div>

        <div id="log" style="border:solid 1px #dddddd; width:490px; margin-left:575px; margin-top:20px; font-size:11px;
	        padding-left:5px; padding-right:10px; padding-top:10px; padding-bottom:20px;
		        margin-bottom:10px; text-align:left; height: 150px; overflow:auto;">

		<p>Logs will appear here.</p>
</div>

<div id="bashlogger" style="width:509px; margin-left:575px; margin-top:20px; overflow:auto;">
<iframe src="/cgi-bin/logviewer.cgi" width=490 height=300>
</iframe>
</div>

</body>
</html>
EOF

