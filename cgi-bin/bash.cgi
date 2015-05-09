#!/bin/bash
#
# 01/05/15: Authored by Peter Hubbard - peterhjr@gmail.com
#
# Changelog: 
# 0.0001 - remove default choice from radio buttons to prevent automatic submission.
# 0.0002 - Move live log viewer into main page and create divs for 2 sections
# 0.0003 - Remove Ajax log viewer.
# 0.0004 - Add logout link
# 0.0005 - Add bootstrap CSS
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

PROGRAMPATH=/home/fargo/dev/scripts/lincontrol/program

LOGFILE=lincontrol_activity.log

# Get the name of the service to be controlled by the panel
# 
SERVICE_NAME=`basename $PROGRAMPATH`

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

cat <<EOF
<html><head><title>Lincontrol admin panel</title></head></html><body>

<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<link href="/css/bootstrap.min.css" rel="stylesheet">
<!--[if lt IE 9]>
<script src="//html5shim.googlecode.com/svn/trunk/html5.js"></script>
<![endif]-->
<link href="/css/styles.css" rel="stylesheet">

<div id="top-nav" class="navbar navbar-inverse navbar-static-top">
<div class="container-fluid">
<div class="navbar-header">
<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
<span class="icon-bar"></span>
<span class="icon-bar"></span>
<span class="icon-bar"></span>
</button>
<a class="navbar-brand" href="#">Main Dashboard</a>
</div>
<div class="navbar-collapse collapse">
<ul class="nav navbar-nav navbar-right">
<li class="dropdown">
<a class="dropdown-toggle" role="button" data-toggle="dropdown" href="#"><i class="glyphicon glyphicon-user"></i>$REMOTE_USER<span class="caret"></span></a>
</li>
<li><a href="/index.html#logout"><i class="glyphicon glyphicon-lock"></i> Logout</a></li>
</ul>
</div>
</div>
<!-- /container -->
</div>
EOF

#####################################################################################
#
#
#############
# FUNCTIONS #
#############
#
# This functions writes an entry to the log file
# First parameter is the action
function logentry()
{
	TIME=`date`

	echo "$TIME / $REMOTE_HOST / $REMOTE_USER / $1 / " >> $LOGFILE

}



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
	#Log this change
	logentry "Changed file $CONFIG_FILE"
	#Strip the ^M (return) character
	echo $configdata | sed -e "s/\r/\n/g" > $CONFIG_FILE 
	echo "<pre><font color=red>File $CONFIG_FILE saved.</font><br></pre>"
fi
# POSTDATA


# test if any parameters were passed
if [ $CMD ]
then
	case "$CMD" in
		startservice)
			echo "<pre>Starting $SERVICE_NAME :"
			$PROGRAMPATH/start.sh
			echo "</pre>"
			;;

		stopservice)
			echo "<pre>Stopping $SERVICE_NAME :"
			$PROGRAMPATH/stop.sh
			echo "</pre>"
			;;

		reloadservice)
			echo "<pre>Reloading $SERVICE_NAME :"
			$PROGRAMPATH/reload.sh
			echo "</pre>"
			;;

		*)
			echo "Unknown command $CMD<br>"
			;;
	esac
fi

# print out the form

cat <<EOF
<div class="col-md-6">
<div class="panel panel-default">
<div class="panel-heading">
<h4>Current contents of $CONFIG_FILE</h4></div>
<div class="panel-body">

<form name=configform method=post enctype=application/x-www-form-urlencoded>

<textarea name=configdata rows=8 cols=70>
EOF

cat $CONFIG_FILE

cat <<EOF
</textarea><br>
<button type=submit>Save Changes</button><br>
</form>

<form id="servicecontrol" method=post>
<div class="btn-group btn-group-justified">
<a href="#" class="btn btn-primary col-sm-3" onClick="document.getElementById('CMD').value='startservice'; document.forms['servicecontrol'].submit(); return false;">
<i class="glyphicon glyphicon-play"></i>
<br> START $SERVICE_NAME
</a>
<a href="#" class="btn btn-primary col-sm-3" onClick="document.getElementById('CMD').value='stopservice'; document.forms['servicecontrol'].submit(); return false;">
<i class="glyphicon glyphicon-stop"></i>
<br> STOP $SERVICE_NAME
</a>
<a href="#" class="btn btn-primary col-sm-3" onClick="document.getElementById('CMD').value='reloadservice'; document.forms['servicecontrol'].submit(); return false;">
<i class="glyphicon glyphicon-refresh"></i>
<br> RELOAD $SERVICE_NAME
</a>
</div>


<input type=hidden id=CMD name=CMD value='' />
</form>
EOF

echo "<pre>Program $SERVICE_NAME has status "
$PROGRAMPATH/status.sh

cat <<EOF
</pre>
</div>
</div>
</div>
</div>

<div class="col-md-6">
<div class="panel panel-default">
<div class="panel-heading">
<h4>Live log</h4></div>
<div class="panel-body">
<iframe src="/cgi-bin/logviewer.cgi" width=610 height=315>
</iframe>
</div>
</div>
</div>
</div>

</body>
</html>
EOF

